#!/usr/bin/env python3
"""nexys-sim — simulateur Nexys A7 : simule un projet Vivado (VHDL) avec Verilator ou GHDL.

Usage :
    python3 nexys_sim.py chemin/vers/projet.xpr
    python3 nexys_sim.py --src a.vhd b.vhd --xdc c.xdc --top Top
    python3 nexys_sim.py projet.xpr --headless --sw 0101 --ms 20

Le brochage (fichier .xdc) est lu tel quel : une erreur dans le .xdc
se voit donc aussi sur la carte virtuelle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pty
import re
import shutil
import subprocess
import sys
import threading
import time
import tty
import webbrowser
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

TOOL_DIR = Path(__file__).resolve().parent
BUILD_ROOT = TOOL_DIR / ".build"
WEB_DIR = TOOL_DIR / "web"

CLK_PERIOD_NS = 10  # 100 MHz
REAL_HZ = 1_000_000_000 // CLK_PERIOD_NS
TARGET_WINDOW_S = 1 / 30  # durée réelle visée pour une fenêtre de simulation
HOLD_NS = 50_000_000  # persistance rétinienne des afficheurs : 50 ms simulées
WATCH_PERIOD_S = 0.6  # surveillance des fichiers du projet
TRUTH_SETTLE_CYC = 100  # cycles laissés au design après chaque changement d'entrées
TRUTH_MAX_INPUTS = 12  # 4096 combinaisons au plus
TRUTH_MAX_WINDOW = 20_000_000  # 200 ms simulées par combinaison au plus

# --------------------------------------------------------------------------
# Brochage Nexys A7-100T (fichier maître Digilent)
# --------------------------------------------------------------------------
CLK_PIN = "E3"

IN_ELEMS = (
    [(f"SW{i}", p) for i, p in enumerate(
        "J15 L16 M13 R15 R17 T18 U18 R13 T8 U8 R16 T13 H6 U12 U11 V10".split())]
    + [("BTNC", "N17"), ("BTNU", "M18"), ("BTNL", "P17"), ("BTNR", "M17"),
       ("BTND", "P18"), ("CPU_RESETN", "C12")]
)
NB_IN = len(IN_ELEMS)  # 22

OUT_ELEMS = (
    [(f"LED{i}", p) for i, p in enumerate(
        "H17 K15 J13 N14 R18 V17 U17 U16 V16 T15 U14 T16 V15 V14 V12 V11".split())]
    + [("LED16_R", "N15"), ("LED16_G", "M16"), ("LED16_B", "R12"),
       ("LED17_R", "N16"), ("LED17_G", "R11"), ("LED17_B", "G14")]
    + [(n, p) for n, p in zip("CA CB CC CD CE CF CG DP".split(),
                              "T10 R10 K16 K13 P15 T11 L18 H15".split())]
    + [(f"AN{i}", p) for i, p in enumerate("J17 J18 T9 J14 P14 T14 K2 U13".split())]
)
NB_OUT = len(OUT_ELEMS)  # 38
SEG0, AN0 = 22, 30
# Niveau "actif" : LEDs actives à '1', segments et anodes actifs à '0'
OUT_ACTIVE = ["1"] * SEG0 + ["0"] * (NB_OUT - SEG0)
OUT_IDLE = ["0"] * SEG0 + ["1"] * (NB_OUT - SEG0)

BOARD_PINS = {"CLK100MHZ": CLK_PIN, **dict(IN_ELEMS), **dict(OUT_ELEMS)}
PIN_TO_IN = {p: i for i, (_, p) in enumerate(IN_ELEMS)}
PIN_TO_OUT = {p: i for i, (_, p) in enumerate(OUT_ELEMS)}


# --------------------------------------------------------------------------
# Langue des messages (fr / en) : --lang, sinon la variable LANG ; la page peut la changer.
# --------------------------------------------------------------------------
LANG = "fr"


def detect_lang() -> str:
    env = os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES") or os.environ.get("LANG") or ""
    return "fr" if env.lower().startswith("fr") else "en"


def set_lang(lang: str):
    global LANG
    LANG = "en" if lang == "en" else "fr"


def T(fr: str, en: str) -> str:
    """Message dans la langue courante."""
    return en if LANG == "en" else fr


def engine_label(engine: str) -> str:
    return {"verilator": T("Verilator (netlist issue de ghdl --synth, logique 2 états)",
                           "Verilator (netlist from ghdl --synth, 2-state logic)"),
            "ghdl": T("GHDL (simulation VHDL, logique 9 états)", "GHDL (VHDL simulation, 9-state logic)")}[engine]


class BuildError(Exception):
    pass


# --------------------------------------------------------------------------
# Lecture du projet
# --------------------------------------------------------------------------
@dataclass
class Project:
    name: str
    sources: list[Path]
    xdcs: list[Path]
    top: str
    key: str
    warnings: list[str] = field(default_factory=list)
    xpr: Path | None = None

    def files(self) -> list[Path]:
        """Fichiers dont la modification doit déclencher une recompilation."""
        return ([self.xpr] if self.xpr else []) + self.sources + self.xdcs

    def signature(self) -> tuple:
        return tuple(self.sources), tuple(self.xdcs), self.top


def mtimes(paths: list[Path]) -> dict[Path, int | None]:
    out: dict[Path, int | None] = {}
    for p in paths:
        try:
            out[p] = p.stat().st_mtime_ns
        except OSError:
            out[p] = None
    return out


def find_xpr(arg: Path) -> tuple[Path, str | None]:
    """Accepte un .xpr, un dossier ou un .bit ; retourne (xpr, note éventuelle)."""
    arg = arg.expanduser().resolve()
    if not arg.exists():
        raise BuildError(T(f"Introuvable : {arg}", f"Not found: {arg}"))
    if arg.is_dir():
        found = sorted(p for p in arg.rglob("*.xpr") if ".Xil" not in p.parts)
        if len(found) == 1:
            return found[0], T(f"Projet trouvé : {found[0]}", f"Project found: {found[0]}")
        if not found:
            raise BuildError(T(f"Aucun projet .xpr dans {arg}", f"No .xpr project in {arg}"))
        raise BuildError(T("Plusieurs projets .xpr dans ce dossier, choisis-en un :\n",
                           "Several .xpr projects in this folder, pick one:\n")
                         + "\n".join(f"  {p}" for p in found))
    suf = arg.suffix.lower()
    if suf == ".xpr":
        return arg, None
    if suf == ".bit":
        for parent in arg.parents:
            found = sorted(parent.glob("*.xpr"))
            if found:
                return found[0], T(f"Un bitstream ne peut pas être simulé : simulation du VHDL du projet {found[0]}",
                                   f"A bitstream cannot be simulated: simulating the VHDL of project {found[0]}")
        raise BuildError(T("Un bitstream ne peut pas être simulé, et aucun .xpr trouvé dans ses dossiers "
                           "parents. Donne le .xpr du projet.",
                           "A bitstream cannot be simulated, and no .xpr was found in its parent folders. "
                           "Give the project's .xpr."))
    raise BuildError(T(f"Attendu : un projet Vivado .xpr (reçu : {arg.name}). "
                       "Pour des fichiers isolés : --src … --xdc … --top …",
                       f"Expected a Vivado .xpr project (got: {arg.name}). "
                       "For loose files: --src … --xdc … --top …"))


def load_xpr(xpr: Path, top_override: str | None) -> Project:
    xpr = xpr.resolve()
    try:
        root = ET.parse(xpr).getroot()
    except ET.ParseError as e:
        raise BuildError(T(f"{xpr.name} n'est pas un projet Vivado lisible (XML invalide : {e}).",
                           f"{xpr.name} is not a readable Vivado project (invalid XML: {e})."))
    pprdir = xpr.parent
    psrcdir = pprdir / f"{xpr.stem}.srcs"
    sources: list[Path] = []
    xdcs: list[Path] = []
    warnings: list[str] = []
    top = None

    def resolve(p: str) -> Path:
        p = p.replace("$PPRDIR", str(pprdir)).replace("$PSRCDIR", str(psrcdir))
        return Path(os.path.normpath(p))

    for fs in root.iter("FileSet"):
        typ = fs.get("Type")
        if typ not in ("DesignSrcs", "Constrs"):
            continue
        for f in fs.findall("File"):
            attrs = [(a.get("Name"), a.get("Val")) for a in f.iter("Attr")]
            if ("AutoDisabled", "1") in attrs or ("IsEnabled", "0") in attrs:
                continue
            used = [v for n, v in attrs if n == "UsedIn"]
            if typ == "DesignSrcs" and used and "synthesis" not in used:
                continue
            path = resolve(f.get("Path", ""))
            suf = path.suffix.lower()
            if typ == "DesignSrcs":
                if suf in (".vhd", ".vhdl"):
                    sources.append(path)
                else:
                    warnings.append(T(f"Fichier ignoré (seul le VHDL est supporté) : {path.name}",
                                      f"File ignored (only VHDL is supported): {path.name}"))
            elif suf == ".xdc":
                xdcs.append(path)
        if typ == "DesignSrcs":
            opt = fs.find("Config/Option[@Name='TopModule']")
            if opt is not None:
                top = opt.get("Val")

    top = top_override or top
    if not top:
        raise BuildError(T("Module principal (top) introuvable dans le .xpr ; utilise --top.",
                           "Top module not found in the .xpr; use --top."))
    for p in sources + xdcs:
        if not p.exists():
            raise BuildError(T(f"Fichier introuvable : {p}", f"File not found: {p}"))
    return Project(xpr.stem, sources, xdcs, top, str(xpr), warnings, xpr)


def load_files(srcs: list[str], xdcs: list[str], top: str | None) -> Project:
    if not top:
        raise BuildError(T("--top est obligatoire avec --src.", "--top is required with --src."))
    sources = [Path(s).resolve() for s in srcs]
    x = [Path(s).resolve() for s in xdcs]
    for p in sources + x:
        if not p.exists():
            raise BuildError(T(f"Fichier introuvable : {p}", f"File not found: {p}"))
    return Project(top, sources, x, top, "|".join(map(str, sources + x)))


# --------------------------------------------------------------------------
# Recherche des projets (sélecteur de la page) et projets récents
# --------------------------------------------------------------------------
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "nexys-sim"
RECENTS_FILE = CONFIG_DIR / "recents.json"
MAX_RECENTS = 8
# Dossiers générés par Vivado : jamais de .xpr dedans, inutile d'y descendre
SCAN_SKIP_SUFFIXES = (".cache", ".runs", ".sim", ".hw", ".ip_user_files", ".gen", ".srcs")
SCAN_SKIP_NAMES = {"node_modules", "__pycache__", "venv", "site-packages"}


def tilde(p: Path) -> str:
    s, home = str(p), str(Path.home())
    return "~" + s[len(home):] if s == home or s.startswith(home + os.sep) else s


def scan_projects(root: Path, max_depth: int = 10, budget_s: float = 4.0) -> tuple[list[Path], bool]:
    """Cherche les .xpr sous root. Retourne (projets, recherche interrompue faute de temps)."""
    found: list[Path] = []
    stack = [(root, 0)]
    t0 = time.monotonic()
    while stack:
        if time.monotonic() - t0 > budget_s:
            return found, True
        d, depth = stack.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    name = e.name
                    if name.startswith(".") or name in SCAN_SKIP_NAMES:
                        continue
                    try:
                        if e.is_dir(follow_symlinks=False):
                            if depth < max_depth and not name.endswith(SCAN_SKIP_SUFFIXES):
                                stack.append((Path(e.path), depth + 1))
                        elif name.endswith(".xpr") and e.is_file():
                            found.append(Path(e.path))
                    except OSError:
                        pass
        except OSError:
            continue
    return found, False


def read_top(xpr: Path) -> str:
    """Module top déclaré dans le .xpr (lecture rapide, sans analyse XML complète)."""
    try:
        with open(xpr, errors="replace") as f:
            m = re.search(r'<Option Name="TopModule" Val="([^"]*)"', f.read(500_000))
        return m.group(1) if m else ""
    except OSError:
        return ""


def project_entry(xpr: Path, root: Path) -> dict:
    try:
        mtime = xpr.stat().st_mtime
    except OSError:
        mtime = 0
    try:
        rel = str(xpr.parent.relative_to(root))
        rel = tilde(root) if rel == "." else rel
    except ValueError:
        rel = tilde(xpr.parent)
    top = read_top(xpr)
    if top == "logisimTopLevelShell":  # même top pour tous les exports Logisim : peu informatif
        top = "export Logisim"
    return {"path": str(xpr), "name": project_label(xpr), "top": top, "rel": rel, "mtime": mtime}


def project_label(xpr: Path) -> str:
    """Nom affiché. Les projets exportés par Logisim s'appellent tous « vp »
    (…/Bin_7Seg/sandbox/vp/vp.xpr) : on prend alors le dossier situé avant « sandbox »."""
    parts = xpr.parent.parts
    if "sandbox" in parts:
        i = len(parts) - 1 - parts[::-1].index("sandbox")
        if i > 0:
            return parts[i - 1]
    return xpr.stem


def load_recents() -> list[str]:
    try:
        data = json.loads(RECENTS_FILE.read_text())
        return [p for p in data if isinstance(p, str)][:MAX_RECENTS]
    except (OSError, ValueError, TypeError):
        return []


def save_recent(xpr: Path):
    items = [str(xpr)] + [p for p in load_recents() if p != str(xpr)]
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        RECENTS_FILE.write_text(json.dumps(items[:MAX_RECENTS], indent=1, ensure_ascii=False))
    except OSError:
        pass


# --------------------------------------------------------------------------
# Analyse VHDL (entité top) et XDC
# --------------------------------------------------------------------------
@dataclass
class Port:
    name: str
    direction: str  # in / out / inout / buffer
    typ: str  # texte du type, tel que déclaré
    indices: list[int] | None  # None = scalaire
    is_bit: bool


def strip_comments(text: str) -> str:
    return re.sub(r"--[^\n]*", "", text)


def split_top_level(s: str, sep: str) -> list[str]:
    out, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def parse_top_ports(sources: list[Path], top: str) -> tuple[list[Port], Path]:
    pat = re.compile(rf"\bentity\s+{re.escape(top)}\s+is\b", re.I)
    for src in sources:
        text = strip_comments(src.read_text(errors="replace"))
        m = pat.search(text)
        if not m:
            continue
        rest = text[m.end():]
        end = re.search(r"\bend\b", rest, re.I)
        decl = rest[: end.start()] if end else rest
        pm = re.search(r"\bport\s*\(", decl, re.I)
        if not pm:
            raise BuildError(T(f"L'entité {top} n'a aucun port ({src.name}) : rien à relier à la carte.",
                               f"Entity {top} has no ports ({src.name}): nothing to connect to the board."))
        i, depth = pm.end(), 1
        while i < len(decl) and depth:
            depth += {"(": 1, ")": -1}.get(decl[i], 0)
            i += 1
        body = decl[pm.end(): i - 1]
        ports: list[Port] = []
        for item in split_top_level(body, ";"):
            if not item.strip():
                continue
            names, _, rest_item = item.partition(":")
            dm = re.match(r"\s*(in|out|inout|buffer)\s+(.*)$", rest_item, re.I | re.S)
            if not dm:
                raise BuildError(T(f"Port non compris dans {src.name} : {item.strip()}",
                                   f"Could not parse port in {src.name}: {item.strip()}"))
            direction = dm.group(1).lower()
            # retire une éventuelle valeur par défaut ":= ..."
            typ = " ".join(split_top_level(dm.group(2), ":")[0].split())
            tl = typ.lower()
            is_bit = tl.startswith("bit")
            if re.fullmatch(r"std_u?logic|bit", tl):
                indices = None
            else:
                vm = re.fullmatch(
                    r"(std_u?logic_vector|unsigned|signed|bit_vector)\s*\(\s*(\d+)\s+(downto|to)\s+(\d+)\s*\)",
                    tl)
                if not vm:
                    raise BuildError(T(f"Type de port non supporté : {typ} (bornes numériques requises)",
                                       f"Unsupported port type: {typ} (numeric bounds required)"))
                a, b = int(vm.group(2)), int(vm.group(4))
                indices = list(range(min(a, b), max(a, b) + 1))
            for n in names.split(","):
                n = n.strip()
                if n:
                    ports.append(Port(n, direction, typ, indices, is_bit))
        return ports, src
    raise BuildError(T(f"Entité « {top} » introuvable dans les sources.", f"Entity “{top}” not found in the sources."))


def parse_xdc(paths: list[Path]) -> tuple[dict[str, str], list[str]]:
    """Retourne {nom_de_port_minuscule (ex. 'sw[3]'): broche}."""
    mapping: dict[str, str] = {}
    warnings: list[str] = []
    get_ports = re.compile(r"get_ports\s+(?:\{\s*([^}]+?)\s*\}|\"([^\"]+)\"|([^\]\s]+))")
    for path in paths:
        for lineno, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
            line = raw.split("#", 1)[0]
            pm = re.search(r"PACKAGE_PIN\s+(\w+)", line, re.I)
            gm = get_ports.search(line)
            if not (pm and gm):
                continue
            port = next(g for g in gm.groups() if g).strip().lower().replace(" ", "")
            pin = pm.group(1).upper()
            if port in mapping and mapping[port] != pin:
                warnings.append(T(f"{path.name}:{lineno} : {port} redéfini ({mapping[port]} -> {pin})",
                                  f"{path.name}:{lineno}: {port} redefined ({mapping[port]} -> {pin})"))
            mapping[port] = pin
    return mapping, warnings


# --------------------------------------------------------------------------
# Génération du banc d'essai
# --------------------------------------------------------------------------
@dataclass
class Wiring:
    inputs: list[tuple[str, str]]  # (élément carte, nom de port)
    outputs: list[tuple[str, str]]
    warnings: list[str]
    # Connexions bit à bit, pour le banc C++ (moteur Verilator) :
    # (port, position du bit dans le vecteur Verilog ou None, source)
    # source : -1 = horloge, k >= 0 = entrée IN_ELEMS[k], None = '0'
    conn_in: list[tuple[str, int | None, int | None]] = field(default_factory=list)
    conn_out: list[tuple[str, int | None, int]] = field(default_factory=list)  # (port, bit, k)


def verilog_bit(p: Port, idx: int | None) -> int | None:
    """Position du bit VHDL idx dans le vecteur Verilog produit par ghdl --synth."""
    if idx is None:
        return None
    lo, hi = p.indices[0], p.indices[-1]
    return hi - idx if re.search(r"\bto\b", p.typ, re.I) and not re.search(r"\bdownto\b", p.typ, re.I) \
        else idx - lo


def make_wrapper(ports: list[Port], top: str, xdc: dict[str, str]) -> tuple[str, Wiring]:
    lines_sig, lines_in, lines_out = [], [], []
    w_in, w_out, warnings = [], [], []
    conn_in, conn_out = [], []
    out_driven: dict[int, str] = {}
    used_keys = set()

    for p in ports:
        sig = f"p_{p.name}"
        lines_sig.append(f"  signal {sig} : {p.typ};")
        bits = [(None, p.name.lower())] if p.indices is None else \
               [(i, f"{p.name.lower()}[{i}]") for i in p.indices]
        for idx, key in bits:
            used_keys.add(key)
            ref = sig if idx is None else f"{sig}({idx})"
            label = p.name if idx is None else f"{p.name}[{idx}]"
            pin = xdc.get(key)
            vbit = verilog_bit(p, idx)
            if p.direction == "in":
                if pin == CLK_PIN:
                    src = "clk"
                    w_in.append(("CLK100MHZ", label))
                    conn_in.append((p.name, vbit, -1))
                elif pin in PIN_TO_IN:
                    k = PIN_TO_IN[pin]
                    src = f"b_in({k})"
                    w_in.append((IN_ELEMS[k][0], label))
                    conn_in.append((p.name, vbit, k))
                else:
                    src = "'0'"
                    conn_in.append((p.name, vbit, None))
                    if pin is None:
                        warnings.append(T(f"Entrée {label} absente du .xdc : forcée à '0'",
                                          f"Input {label} missing from the .xdc: tied to '0'"))
                    else:
                        warnings.append(T(f"Entrée {label} sur la broche {pin}, non gérée : forcée à '0'",
                                          f"Input {label} on unsupported pin {pin}: tied to '0'"))
                if p.is_bit:
                    src = f"to_bit({src})"
                lines_in.append(f"  {ref} <= {src};")
            else:
                if p.direction == "inout":
                    warnings.append(T(f"Port inout {label} traité comme une sortie", f"Inout port {label} treated as an output"))
                if pin in PIN_TO_OUT:
                    k = PIN_TO_OUT[pin]
                    if k in out_driven:
                        warnings.append(T(f"Broche {pin} pilotée deux fois ({out_driven[k]} et {label})",
                                          f"Pin {pin} driven twice ({out_driven[k]} and {label})"))
                        continue
                    out_driven[k] = label
                    conn_out.append((p.name, vbit, k))
                    val = f"to_stdulogic({ref})" if p.is_bit else ref
                    lines_out.append(f"  b_out({k}) <= {val};")
                    w_out.append((OUT_ELEMS[k][0], label))
                elif pin is None:
                    warnings.append(T(f"Sortie {label} absente du .xdc : ignorée", f"Output {label} missing from the .xdc: ignored"))
                else:
                    warnings.append(T(f"Sortie {label} sur la broche {pin}, non gérée : ignorée",
                                      f"Output {label} on unsupported pin {pin}: ignored"))

    for key in xdc:
        if key not in used_keys:
            warnings.append(T(f"Le .xdc contraint « {key} », qui n'est pas un port de {top}",
                              f"The .xdc constrains “{key}”, which is not a port of {top}"))
    for k in range(NB_OUT):
        if k not in out_driven:
            lines_out.append(f"  b_out({k}) <= '{OUT_IDLE[k]}';")

    portmap = ",\n".join(f"      {p.name} => p_{p.name}" for p in ports)
    active = "".join(OUT_ACTIVE)
    vhdl = f"""-- Généré par nexys_sim.py : ne pas modifier.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

entity carte_tb is
end entity carte_tb;

architecture sim of carte_tb is
  constant NB_IN  : integer := {NB_IN};
  constant NB_OUT : integer := {NB_OUT};
  constant ACTIVE : string(1 to NB_OUT) := "{active}";
  type int_arr is array (natural range <>) of integer;
  signal clk   : std_logic := '0';
  signal b_in  : std_logic_vector(NB_IN - 1 downto 0) := (others => '0');
  signal b_out : std_logic_vector(NB_OUT - 1 downto 0);
{chr(10).join(lines_sig)}
begin
  clk <= not clk after {CLK_PERIOD_NS // 2} ns;

{chr(10).join(lines_in)}

{chr(10).join(lines_out)}

  dut : entity work.{top}
    port map (
{portmap}
    );

  -- Protocole : lit "<{NB_IN} bits d'entrée> <cycles>", simule, puis écrit
  -- "@@R <cycles> <temps actif par sortie (ns)...> <temps segment par afficheur...> <indéfinis>".
  monitor : process
    variable lin, lout : line;
    variable c         : character;
    variable ncyc      : integer;
    variable inv       : std_logic_vector(NB_IN - 1 downto 0);
    variable prev      : std_logic_vector(NB_OUT - 1 downto 0) := (others => 'U');
    variable act_t     : int_arr(0 to NB_OUT - 1);
    variable seg_t     : int_arr(0 to 63);
    variable undef     : string(1 to NB_OUT);
    variable t_last    : time := 0 ns;
    variable t_end     : time;
    variable dt        : integer;
  begin
    loop
      readline(input, lin);
      for i in 0 to NB_IN - 1 loop
        read(lin, c);
        if c = '1' then inv(i) := '1'; else inv(i) := '0'; end if;
      end loop;
      read(lin, ncyc);
      b_in <= inv;
      act_t := (others => 0);
      seg_t := (others => 0);
      undef := (others => '0');
      t_end := now + ncyc * {CLK_PERIOD_NS} ns;
      loop
        wait on b_out for t_end - now;
        dt := (now - t_last) / 1 ns;
        if dt > 0 then
          for i in 0 to NB_OUT - 1 loop
            if prev(i) = '1' and ACTIVE(i + 1) = '1' then act_t(i) := act_t(i) + dt; end if;
            if prev(i) = '0' and ACTIVE(i + 1) = '0' then act_t(i) := act_t(i) + dt; end if;
          end loop;
          for d in 0 to 7 loop
            if prev({AN0} + d) = '0' then
              for s in 0 to 7 loop
                if prev({SEG0} + s) = '0' then seg_t(d * 8 + s) := seg_t(d * 8 + s) + dt; end if;
              end loop;
            end if;
          end loop;
        end if;
        t_last := now;
        prev := b_out;
        for i in 0 to NB_OUT - 1 loop
          if b_out(i) /= '0' and b_out(i) /= '1' then undef(i + 1) := '1'; end if;
        end loop;
        exit when now >= t_end;
      end loop;
      write(lout, string'("@@R "));
      write(lout, ncyc);
      for i in 0 to NB_OUT - 1 loop write(lout, ' '); write(lout, act_t(i)); end loop;
      for i in 0 to 63 loop write(lout, ' '); write(lout, seg_t(i)); end loop;
      write(lout, ' ');
      write(lout, undef);
      writeline(output, lout);
    end loop;
  end process monitor;
end architecture sim;
"""
    return vhdl, Wiring(w_in, w_out, warnings, conn_in, conn_out)


INIT_SCALAR = re.compile(
    r"^(\s*(?:signal|variable)\s+[\w\s,]+?:\s*)(std_u?logic|bit)(\s*);", re.I | re.M)
INIT_VECTOR = re.compile(
    r"^(\s*(?:signal|variable)\s+[\w\s,]+?:\s*)"
    r"((?:std_u?logic_vector|unsigned|signed|bit_vector)\s*\([^;:]*\))(\s*);", re.I | re.M)
INIT_INT = re.compile(r"^(\s*(?:signal|variable)\s+[\w\s,]+?:\s*)(integer)(\s*);", re.I | re.M)


def init_like_fpga(text: str) -> str:
    """Ajoute une valeur initiale nulle aux signaux/variables qui n'en ont pas.

    Sur FPGA, les bascules démarrent à 0 au chargement du bitstream ; en
    simulation elles valent 'U'. Le nombre de lignes est conservé pour que
    les messages d'erreur pointent au bon endroit.
    """
    text = INIT_SCALAR.sub(lambda m: f"{m[1]}{m[2]} := '0'{m[3]};", text)
    text = INIT_VECTOR.sub(lambda m: f"{m[1]}{m[2]} := (others => '0'){m[3]};", text)
    text = INIT_INT.sub(lambda m: f"{m[1]}{m[2]} := 0{m[3]};", text)
    return text


@dataclass
class Build:
    exe: Path
    wiring: Wiring
    warnings: list[str]
    path_map: dict[str, str]
    engine: str = "ghdl"


# --------------------------------------------------------------------------
# Moteur Verilator : ghdl --synth (netlist Verilog) + Verilator (C++ compilé)
# --------------------------------------------------------------------------
HARNESS_CPP = r"""// Généré par nexys_sim.py : ne pas modifier.
// Même protocole que le banc VHDL : lit "<entrées> <cycles>", écrit "@@R ...".
#include "Vtop.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>

static const int NB_IN = @NB_IN@, NB_OUT = @NB_OUT@, SEG0 = @SEG0@, AN0 = @AN0@;
static const uint64_t ACTIVE_HIGH = @ACTIVE_HIGH@ULL;  // bit k = 1 : sortie k active à '1'
static Vtop* top;

static inline void drive(uint32_t in, int clk) {
@DRIVE@
}

static inline uint64_t pack() {
  uint64_t v = @IDLE@ULL;
@PACK@
  return v;
}

int main() {
  auto ctx = std::make_unique<VerilatedContext>();
  top = new Vtop{ctx.get()};
  drive(0, 0);
  top->eval();
  uint64_t prev = pack();
  static char line[512];
  while (fgets(line, sizeof line, stdin)) {
    uint32_t in = 0;
    for (int i = 0; i < NB_IN; i++) if (line[i] == '1') in |= 1u << i;
    long long ncyc = strtoll(line + NB_IN, nullptr, 10);
    long long act[NB_OUT] = {0}, seg[64] = {0};
    long long t_last = 0;
    auto account = [&](long long now) {
      long long dt = now - t_last;
      if (dt > 0) {
        uint64_t on = ~(prev ^ ACTIVE_HIGH);  // bit = 1 si la sortie est à son niveau actif
        for (int i = 0; i < NB_OUT; i++) if ((on >> i) & 1) act[i] += dt;
        for (int d = 0; d < 8; d++)
          if (!((prev >> (AN0 + d)) & 1))
            for (int s = 0; s < 8; s++)
              if (!((prev >> (SEG0 + s)) & 1)) seg[d * 8 + s] += dt;
      }
      t_last = now;
    };
    drive(in, 0);
    top->eval();
    prev = pack();
    if (@HAS_CLK@) {
      for (long long c = 0; c < ncyc; c++) {
        long long t0 = c * @PERIOD@;
        drive(in, 1); top->eval();
        uint64_t cur = pack();
        if (cur != prev) { account(t0 + @HALF@); prev = cur; }
        drive(in, 0); top->eval();
        cur = pack();
        if (cur != prev) { account(t0 + @PERIOD@); prev = cur; }
      }
    }
    account(ncyc * @PERIOD@);
    printf("@@R %lld", ncyc);
    for (int i = 0; i < NB_OUT; i++) printf(" %lld", act[i]);
    for (int i = 0; i < 64; i++) printf(" %lld", seg[i]);
    printf(" ");
    for (int i = 0; i < NB_OUT; i++) putchar('0');
    putchar('\n');
    fflush(stdout);
  }
  top->final();
  delete top;
  return 0;
}
"""


def make_harness(ports: list[Port], wiring: Wiring) -> str:
    by_port: dict[str, list] = {}
    for name, bit, src in wiring.conn_in:
        by_port.setdefault(name, []).append((bit, src))
    drive = []
    for name, conns in by_port.items():
        terms = []
        for bit, src in conns:
            if src is None:
                continue
            val = "(uint64_t)clk" if src == -1 else f"(uint64_t)((in >> {src}) & 1)"
            terms.append(val if bit is None else f"({val} << {bit})")
        drive.append(f"  top->{name} = {' | '.join(terms) or '0'};")
    idle = 0
    for k, c in enumerate(OUT_IDLE):
        if c == "1":
            idle |= 1 << k
    pack = []
    for name, bit, k in wiring.conn_out:
        idle &= ~(1 << k)
        val = f"(uint64_t)top->{name}" if bit is None else f"(((uint64_t)top->{name} >> {bit}) & 1)"
        pack.append(f"  v |= {val} << {k};")
    active_high = sum(1 << k for k, c in enumerate(OUT_ACTIVE) if c == "1")
    has_clk = any(src == -1 for _, _, src in wiring.conn_in)
    rep = {"@NB_IN@": NB_IN, "@NB_OUT@": NB_OUT, "@SEG0@": SEG0, "@AN0@": AN0,
           "@ACTIVE_HIGH@": active_high, "@IDLE@": idle, "@DRIVE@": "\n".join(drive),
           "@PACK@": "\n".join(pack), "@HAS_CLK@": "true" if has_clk else "false",
           "@PERIOD@": CLK_PERIOD_NS, "@HALF@": CLK_PERIOD_NS // 2}
    out = HARNESS_CPP
    for k, v in rep.items():
        out = out.replace(k, str(v))
    return out


ISIGNAL_INIT = re.compile(
    r"(  always @\*\n    (\\?\S+) = [^;]*; // \(isignal\)\n)  initial\n    \2 = [^;]*;\n")


def build_verilator(project: Project, ports: list[Port], wiring: Wiring, copies: list[Path],
                    bdir: Path, log, fix_paths) -> Path:
    """Retourne l'exécutable ; lève BuildError si le design n'est pas synthétisable."""
    for p in ports:
        if p.direction not in ("in", "out", "buffer"):
            raise BuildError(T(f"port {p.direction} {p.name} non géré par le moteur Verilator",
                               f"{p.direction} port {p.name} not supported by the Verilator engine"))
        if p.indices and len(p.indices) > 64:
            raise BuildError(T(f"port {p.name} de plus de 64 bits non géré par le moteur Verilator",
                               f"port {p.name} wider than 64 bits not supported by the Verilator engine"))
    vdir = bdir / "verilator"
    vdir.mkdir()
    netlist = vdir / "top.v"
    # Chemins relatifs : avec des chemins absolus, ghdl --elab-order ne liste rien.
    rel = {os.path.relpath(c, vdir): str(c) for c in copies}

    def fix(text: str) -> str:
        for r_, a in rel.items():
            text = text.replace(r_, a)
        return fix_paths(text)

    err = None
    for std in ("08", "93c"):
        work = vdir / f"work{std}"
        work.mkdir()
        common = [f"--std={std}", "-fsynopsys", "-frelaxed", "--work=xil_defaultlib", f"--workdir={work}"]
        log(T(f"Synthèse GHDL (VHDL-{std[:2]})…", f"GHDL synthesis (VHDL-{std[:2]})…"))
        # -i importe sans analyser ; --elab-order donne l'ordre des fichiers à analyser.
        r = subprocess.run(["ghdl", "-i", *common, *rel], cwd=vdir, capture_output=True, text=True)
        if r.returncode == 0:
            r = subprocess.run(["ghdl", "--elab-order", *common, project.top],
                               cwd=vdir, capture_output=True, text=True)
        if r.returncode == 0:
            order = [l.strip() for l in r.stdout.splitlines() if l.strip()]
            if not order:
                raise BuildError(T(f"ghdl --elab-order n'a trouvé aucun fichier pour {project.top}",
                                   f"ghdl --elab-order found no file for {project.top}"))
            with open(netlist, "w") as f:
                r = subprocess.run(["ghdl", "--synth", *common, "--out=verilog", *order, "-e", project.top],
                                   cwd=vdir, stdout=f, stderr=subprocess.PIPE, text=True)
        if r.returncode == 0:
            err = None
            break
        err = err or fix(((r.stdout or "") + r.stderr).strip())
    if err is not None:
        raise BuildError(T("synthèse impossible :\n", "synthesis failed:\n") + err)
    # ghdl --synth donne aux signaux combinatoires (« isignal ») un bloc initial en plus
    # de leur always @*. Verilator évalue alors ces signaux de façon incohérente
    # (sorties qui changent au front descendant). Ces valeurs initiales sont inutiles :
    # le always @* les impose. Celles des bascules (always @(posedge)) sont gardées.
    text = netlist.read_text()
    text = ISIGNAL_INIT.sub(r"\1", text)
    netlist.write_text(text)
    (vdir / "harness.cpp").write_text(make_harness(ports, wiring))
    log(T("Compilation Verilator…", "Verilator build…"))
    cmd = ["verilator", "--cc", "--exe", "--build", "-O3", "--top-module", project.top,
           "--prefix", "Vtop", "-Mdir", str(vdir / "obj"), "-o", "sim",
           "-Wno-fatal", "-Wno-lint", "-Wno-style", "-Wno-MULTIDRIVEN", "-Wno-UNOPTFLAT",
           "-MAKEFLAGS", "OPT_FAST=-O2 OPT_SLOW=-O1", "--build-jobs", "0",
           str(netlist), str(vdir / "harness.cpp")]
    r = subprocess.run(cmd, cwd=vdir, capture_output=True, text=True)
    exe = vdir / "obj" / "sim"
    if r.returncode != 0 or not exe.exists():
        lines = [l for l in (r.stdout + r.stderr).splitlines() if "%Error" in l or "error" in l.lower()]
        raise BuildError(T("Verilator a échoué :\n", "Verilator failed:\n") + "\n".join(lines[:15] or (r.stdout + r.stderr).splitlines()[-15:]))
    return exe


def build(project: Project, init_zero: bool, log, engine: str = "ghdl") -> Build:
    if shutil.which("ghdl") is None:
        raise BuildError(T("ghdl introuvable. Installe-le : sudo dnf install ghdl",
                           "ghdl not found. Install it: sudo dnf install ghdl"))
    key = hashlib.sha1(project.key.encode()).hexdigest()[:8]
    bdir = BUILD_ROOT / f"{project.name}-{key}"
    if bdir.exists():
        shutil.rmtree(bdir)
    srcdir = bdir / "src"
    srcdir.mkdir(parents=True)

    ports, _ = parse_top_ports(project.sources, project.top)
    xdc, xdc_warn = parse_xdc(project.xdcs)
    if not project.xdcs:
        xdc_warn.append(T("Aucun fichier .xdc : aucune broche ne sera connectée",
                          "No .xdc file: no pin will be connected"))
    wrapper, wiring = make_wrapper(ports, project.top, xdc)

    path_map: dict[str, str] = {}
    copies = []
    for n, src in enumerate(project.sources):
        dst = srcdir / f"{n:02d}_{src.name}"
        text = src.read_text(errors="replace")
        dst.write_text(init_like_fpga(text) if init_zero else text)
        path_map[str(dst)] = str(src)
        copies.append(dst)
    tb = srcdir / "carte_tb.vhd"
    tb.write_text(wrapper)

    def fix_paths(s: str) -> str:
        for k, v in path_map.items():
            s = s.replace(k, v)
        return s

    warnings = project.warnings + xdc_warn + wiring.warnings
    synth_err = None
    if engine in ("auto", "verilator"):
        try:
            if shutil.which("verilator") is None:
                raise BuildError(T("verilator introuvable (sudo dnf install verilator)",
                                   "verilator not found (sudo dnf install verilator)"))
            exe = build_verilator(project, ports, wiring, copies, bdir, log, fix_paths)
            return Build(exe, wiring, warnings, path_map, "verilator")
        except BuildError as e:
            if engine == "verilator":
                raise
            synth_err = str(e)
            log(T("Moteur Verilator indisponible, repli sur GHDL.", "Verilator engine unavailable, falling back to GHDL."), "warn")

    errors = None
    for std in ("08", "93c"):
        work = bdir / f"work{std}"
        work.mkdir()
        common = [f"--std={std}", "-O2", "-fsynopsys", "-frelaxed", "--work=xil_defaultlib",
                  f"--workdir={work}"]
        log(T(f"Compilation GHDL (VHDL-{std[:2]})…", f"GHDL build (VHDL-{std[:2]})…"))
        steps = [["ghdl", "-i", *common, *map(str, copies), str(tb)],
                 ["ghdl", "-m", *common, "-o", str(bdir / "sim"), "carte_tb"]]
        ok = True
        for cmd in steps:
            r = subprocess.run(cmd, cwd=bdir, capture_output=True, text=True)
            if r.returncode != 0:
                ok = False
                out = fix_paths((r.stdout + r.stderr).strip())
                errors = errors or out  # garde les erreurs du premier essai (VHDL-2008)
                break
        if ok:
            if synth_err:
                # Le VHDL compile mais ne se synthétise pas : à signaler, Vivado le refusera aussi.
                warnings = warnings + [T("Moteur Verilator : ", "Verilator engine: ") + synth_err]
            return Build(bdir / "sim", wiring, warnings, path_map, "ghdl")
        log(T(f"Échec en VHDL-{std[:2]}.", f"Failed as VHDL-{std[:2]}."))
    raise BuildError(T("Erreur de compilation :\n", "Compilation error:\n") + (errors or "?"))


# --------------------------------------------------------------------------
# Exécution de la simulation
# --------------------------------------------------------------------------
def encode_inputs(sw: int, btn: int) -> str:
    """Entrées au format du banc d'essai : SW0..SW15, BTNC U L R D, CPU_RESETN."""
    bits = [(sw >> i) & 1 for i in range(16)] + [(btn >> i) & 1 for i in range(5)]
    bits.append(0 if btn & 0x20 else 1)  # CPU_RESETN actif bas
    return "".join(map(str, bits))


def truth_row(sw: int, n: int, act: list[int], seg: list[int], undef: str) -> dict:
    """Une ligne de table de vérité, mesurée sur une fenêtre de n cycles."""
    n = max(n, 1)
    digits = []
    for d in range(8):
        an = act[AN0 + d]
        # -1 : anode jamais active ; sinon octet des segments allumés (bit 0 = a … bit 7 = DP)
        digits.append(-1 if an == 0 else sum(1 << s for s in range(8) if seg[d * 8 + s] / an > 0.5))
    return {"sw": sw,
            "leds": [round(act[i] / n, 3) for i in range(16)],
            "rgb": [round(act[16 + i] / n, 3) for i in range(6)],
            "seg": digits,
            "undef": [OUT_ELEMS[i][0] for i, c in enumerate(undef) if c == "1"]}


class Board:
    """État des entrées/sorties de la carte, partagé entre threads."""

    def __init__(self):
        self.lock = threading.Lock()
        self.sw = 0
        self.btn = 0  # bits : C U L R D RESET
        self.btn_latched = 0
        self.reset_state()

    def reset_state(self):
        self.sim_ns = 0
        self.leds = [0.0] * 16
        self.rgb = [0.0] * 6
        self.digits = [[0.0] * 8 for _ in range(8)]
        self.digit_seen = [-HOLD_NS - 1] * 8
        self.digit_pat = [[0.0] * 8 for _ in range(8)]
        self.undef: list[str] = []
        self.speed = 0.0

    def set_inputs(self, sw: int, btn: int):
        with self.lock:
            self.sw = sw & 0xFFFF
            self.btn = btn & 0x3F
            self.btn_latched |= self.btn

    def input_bits(self) -> str:
        with self.lock:
            btn = self.btn | self.btn_latched  # un clic bref dure au moins une fenêtre
            self.btn_latched = 0
            sw = self.sw
        return encode_inputs(sw, btn)

    def update(self, ncyc: int, act: list[int], seg: list[int], undef: str, speed: float):
        total = ncyc * CLK_PERIOD_NS
        with self.lock:
            self.sim_ns += total
            self.leds = [act[i] / total for i in range(16)]
            self.rgb = [act[16 + i] / total for i in range(6)]
            for d in range(8):
                an = act[AN0 + d]
                if an > 0:
                    self.digit_pat[d] = [seg[d * 8 + s] / an for s in range(8)]
                    self.digit_seen[d] = self.sim_ns
                visible = self.sim_ns - self.digit_seen[d] <= HOLD_NS
                self.digits[d] = self.digit_pat[d] if visible else [0.0] * 8
            self.undef = [OUT_ELEMS[i][0] for i, c in enumerate(undef) if c == "1"]
            self.speed = speed

    def snapshot(self) -> dict:
        with self.lock:
            return {"leds": self.leds, "rgb": self.rgb, "digits": self.digits,
                    "undef": self.undef, "speed": self.speed, "sim_ns": self.sim_ns,
                    "sw": self.sw, "btn": self.btn}


class Simulator:
    def __init__(self, exe: Path, board: Board, log):
        self.board = board
        self.log = log
        self.stop_evt = threading.Event()
        master, slave = pty.openpty()
        tty.setraw(slave)  # pty : GHDL vide sa sortie à chaque ligne
        self.proc = subprocess.Popen([str(exe), "--ieee-asserts=disable"],
                                     stdin=subprocess.PIPE, stdout=slave, stderr=slave,
                                     text=True, bufsize=1, cwd=exe.parent)
        os.close(slave)
        self.out = os.fdopen(master, "r", buffering=1, errors="replace")
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.error: str | None = None
        # Tenu pendant chaque échange avec le simulateur ; la table de vérité le garde
        # pendant tout le balayage, ce qui met la boucle temps réel en pause.
        self.io_lock = threading.Lock()

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_evt.set()
        if self.proc.poll() is None:
            self.proc.kill()
        self.thread.join(timeout=2)
        try:
            self.out.close()
        except OSError:
            pass

    def exchange(self, bits: str, ncyc: int) -> tuple[int, list[int], list[int], str]:
        """Applique les entrées et simule ncyc cycles.

        Retourne (cycles simulés, activité par sortie, activité par segment, sorties U/X)."""
        self.proc.stdin.write(f"{bits} {ncyc}\n")
        self.proc.stdin.flush()
        while True:
            line = self.out.readline()
            if not line:
                raise RuntimeError(T("la simulation s'est arrêtée", "the simulation stopped"))
            line = line.rstrip("\r\n")
            if line.startswith("@@R "):
                break
            if line.strip():
                self.log(line, "sim")
        f = line.split()
        n = int(f[1])
        act = list(map(int, f[2: 2 + NB_OUT]))
        seg = list(map(int, f[2 + NB_OUT: 2 + NB_OUT + 64]))
        undef = f[2 + NB_OUT + 64]
        return n, act, seg, undef

    def measure(self, bits: str, ncyc: int, chunk: int = 500_000) -> tuple[int, list[int], list[int], str]:
        """Comme exchange, en plusieurs morceaux si la fenêtre est longue (cumul des compteurs)."""
        total, act, seg, undef = 0, [0] * NB_OUT, [0] * 64, ["0"] * NB_OUT
        while total < ncyc:
            n, a, s, u = self.exchange(bits, min(chunk, ncyc - total))
            if n <= 0:
                break
            total += n
            act = [x + y for x, y in zip(act, a)]
            seg = [x + y for x, y in zip(seg, s)]
            undef = ["1" if "1" in (x, y) else "0" for x, y in zip(undef, u)]
        return total, act, seg, "".join(undef)

    def step(self, ncyc: int) -> float:
        """Simule ncyc cycles avec les entrées de la carte ; retourne la durée réelle (s)."""
        t0 = time.perf_counter()
        n, act, seg, undef = self.exchange(self.board.input_bits(), ncyc)
        el = time.perf_counter() - t0
        speed = n / REAL_HZ / max(el, 1e-6)
        self.board.update(n, act, seg, undef, speed)
        return el

    def _run(self):
        ncyc = 1000
        max_cyc = int(REAL_HZ * TARGET_WINDOW_S)  # jamais plus vite que le temps réel
        try:
            while not self.stop_evt.is_set():
                with self.io_lock:
                    if self.stop_evt.is_set():
                        break
                    el = self.step(ncyc)
                ratio = TARGET_WINDOW_S / max(el, 1e-6)
                ncyc = int(min(max_cyc, max(100, ncyc * min(2.0, max(0.5, ratio)))))
                if ncyc == max_cyc and el < TARGET_WINDOW_S:
                    time.sleep(TARGET_WINDOW_S - el)
        except Exception as e:  # noqa: BLE001
            if not self.stop_evt.is_set():
                rest = ""
                try:
                    rest = self.out.read(4000)
                except OSError:
                    pass
                self.error = (T("Simulation arrêtée : ", "Simulation stopped: ") + f"{e}\n{rest}").strip()
                self.log(self.error, "error")


# --------------------------------------------------------------------------
# Application (compilation + simulation + serveur web)
# --------------------------------------------------------------------------
class App:
    def __init__(self, args):
        self.args = args
        self.board = Board()
        self.sim: Simulator | None = None
        self.logs: deque = deque(maxlen=500)
        self.log_seq = 0
        self.status = "idle"
        self.wiring: Wiring | None = None
        self.project_name = ""
        self.project_info: dict = {}
        self.engine = ""
        self.cond = threading.Condition()
        self.building = False  # compilation en cours
        self.rebuild_pending = False  # recompilation demandée pendant une compilation
        self.last_error: str | None = None  # dernière erreur de compilation, affichée en bandeau
        # Sélecteur de projet
        self.root = Path(getattr(args, "racine", "~/Documents")).expanduser()
        self.project_path: str | None = None
        self.scan_cache: tuple | None = None  # (date, projets, interrompu, durée)
        self.scan_lock = threading.Lock()
        # Recompilation automatique
        self.watch_on = not getattr(args, "no_watch", False)
        self.watch_gen = 0
        self.watch_paths: list[Path] = []
        self.watch_snap: dict[Path, int | None] = {}
        self.project_sig: tuple | None = None
        # Table de vérité
        self.truth: dict = {"status": "idle"}
        self.truth_seq = 0
        self.truth_cancel = threading.Event()
        self.truth_lock = threading.Lock()

    def log(self, msg: str, kind: str = "info"):
        with self.cond:
            for line in msg.splitlines() or [""]:
                self.log_seq += 1
                self.logs.append((self.log_seq, kind, line))
            self.cond.notify_all()
        if self.args.headless or self.args.verbose:
            print(f"[{kind}] {msg}", file=sys.stderr)

    def set_status(self, s: str):
        with self.cond:
            self.status = s
            self.cond.notify_all()

    def load_project(self, quiet: bool = False) -> Project:
        a = self.args
        if a.xpr:
            xpr, note = find_xpr(Path(a.xpr))
            if note and not quiet:
                self.log(note, "warn")
            return load_xpr(xpr, a.top)
        return load_files(a.src or [], a.xdc or [], a.top)

    def has_project(self) -> bool:
        return bool(self.args.xpr or self.args.src)

    def rebuild(self):
        """Recompile ; une demande reçue pendant une compilation en relance une à la fin."""
        with self.cond:
            if self.building:
                self.rebuild_pending = True
                return
            self.building = True
        while True:
            self._rebuild_once()
            with self.cond:
                if not self.rebuild_pending:
                    self.building = False
                    return
                self.rebuild_pending = False

    def open_project(self, path: str):
        """Change de projet (sélecteur de la page). Lève BuildError si le chemin ne convient pas."""
        if not path.strip():
            raise BuildError(T("Chemin vide.", "Empty path."))
        p = Path(path.strip()).expanduser()
        if p.is_dir():
            found, _ = scan_projects(p.resolve(), max_depth=4, budget_s=2.0)
            if not found:
                raise BuildError(T(f"Aucun projet .xpr dans {p}", f"No .xpr project in {p}"))
            if len(found) > 1:
                names = ", ".join(project_label(f) for f in found[:6]) + (" …" if len(found) > 6 else "")
                raise BuildError(T(f"Plusieurs projets dans {p} : {names}. Choisis-en un dans la liste.",
                                   f"Several projects in {p}: {names}. Pick one from the list."))
            p = found[0]
        xpr, _ = find_xpr(p)
        self.args.xpr, self.args.src, self.args.xdc, self.args.top = str(xpr), None, None, None
        with self.cond:
            self.project_path = str(xpr)
            self.project_info = {"name": project_label(xpr), "top": read_top(xpr), "sources": [], "xdcs": []}
            self.wiring = None
            self.engine = ""
            self.last_error = None
        self.board.reset_state()
        self._set_truth({"status": "idle"})
        self.log(T("Projet : ", "Project: ") + str(xpr))
        threading.Thread(target=self.rebuild, daemon=True).start()

    def projects(self, refresh: bool) -> dict:
        """Projets récents et projets trouvés sous la racine (recherche mise en cache 60 s)."""
        with self.scan_lock:
            if refresh or not self.scan_cache or time.monotonic() - self.scan_cache[0] > 60:
                t0 = time.monotonic()
                found, truncated = scan_projects(self.root)
                self.scan_cache = (time.monotonic(), found, truncated, time.monotonic() - t0)
            _, found, truncated, dur = self.scan_cache
        recents = [Path(p) for p in load_recents()]
        return {
            "root": tilde(self.root),
            "truncated": truncated,
            "scan_s": round(dur, 2),
            "current": self.project_path,
            "recents": [project_entry(p, self.root) for p in recents if p.exists()],
            "found": sorted((project_entry(p, self.root) for p in found), key=lambda e: -e["mtime"]),
        }

    def _rebuild_once(self):
        try:
            self.truth_cancel.set()
            if self.sim:
                self.sim.stop()
                self.sim = None
            self.last_error = None
            if not self.has_project():
                self.set_status("idle")
                return
            self.set_status("compiling")
            project = self.load_project()
            if project.xpr:
                self.project_path = str(project.xpr)
                save_recent(project.xpr)
            self._watch_project(project)
            if self.truth.get("status") == "done":
                self._set_truth({**self.truth, "stale": True})
            self.project_name = f"{project.name} (top : {project.top})"
            self.project_info = {
                "name": project_label(project.xpr) if project.xpr else project.name, "top": project.top,
                "sources": [p.name for p in project.sources],
                "xdcs": [p.name for p in project.xdcs],
            }
            engine = self.args.moteur
            if engine == "auto" and self.args.no_init:
                engine = "ghdl"  # les 'U' n'existent qu'en simulation 9 états
            b = build(project, not self.args.no_init, self.log, engine)
            self.engine = b.engine
            self.log(T("Moteur : ", "Engine: ") + engine_label(b.engine), "info")
            self.wiring = b.wiring
            for w in b.warnings:
                self.log(w, "warn")
            self.board.reset_state()
            self.sim = Simulator(b.exe, self.board, self.log)
            self.sim.start()
            self.log(T("Simulation démarrée.", "Simulation started."), "ok")
            self.set_status("running")
        except BuildError as e:
            self.last_error = str(e)
            self.log(str(e), "error")
            self.set_status("error")
        except Exception as e:  # noqa: BLE001
            self.last_error = T("Erreur inattendue : ", "Unexpected error: ") + repr(e)
            self.log(self.last_error, "error")
            self.set_status("error")

    # ---------- Recompilation à la sauvegarde ----------
    def _watch_project(self, project: Project):
        """Mémorise les fichiers du projet et leur date, lues avant la compilation :
        une sauvegarde pendant la compilation déclenchera donc une nouvelle compilation."""
        paths = project.files()
        with self.cond:
            self.watch_paths = paths
            self.watch_snap = mtimes(paths)
            self.watch_gen += 1
            self.project_sig = project.signature()

    def _fileset_changed(self) -> bool:
        """Après une modification du .xpr seul : la liste des sources ou le top ont-ils changé ?
        (Vivado réécrit le .xpr pour bien d'autres raisons, ex. lancer une synthèse.)"""
        try:
            return self.load_project(quiet=True).signature() != self.project_sig
        except BuildError:
            return True  # .xpr illisible : recompiler pour afficher l'erreur

    def watch_loop(self):
        gen, seen, pending = -1, {}, None
        while True:
            time.sleep(WATCH_PERIOD_S)
            with self.cond:
                if self.watch_gen != gen:
                    gen, seen, pending = self.watch_gen, dict(self.watch_snap), None
                paths = list(self.watch_paths)
            if not paths or self.building:
                continue
            cur = mtimes(paths)
            if cur == seen:
                pending = None
                continue
            if cur != pending:  # attendre une période sans changement : sauvegarde terminée
                pending = cur
                continue
            changed = [p for p in paths if cur[p] != seen.get(p)]
            seen, pending = cur, None
            if not self.watch_on:
                continue
            xpr = paths[0] if paths[0].suffix.lower() == ".xpr" else None
            if changed == [xpr] and not self._fileset_changed():
                continue
            names = ", ".join(p.name for p in changed)
            self.log(T(f"Modification détectée ({names}) : recompilation.", f"Change detected ({names}): rebuilding."))
            self.rebuild()

    # ---------- Table de vérité ----------
    def _set_truth(self, d: dict):
        with self.cond:
            self.truth = d
            self.truth_seq += 1
            self.cond.notify_all()

    def start_truth(self, sws: list[int], window: int) -> bool:
        if not self.truth_lock.acquire(blocking=False):
            return False
        threading.Thread(target=self._truth, args=(sws, window), daemon=True).start()
        return True

    def _truth_cancelled(self, base: dict, done: int, total: int):
        # Après un changement de projet, la table est déjà remise à zéro : ne pas l'écraser.
        if self.truth.get("status") != "idle":
            self._set_truth({**base, "status": "cancelled", "done": done, "total": total})

    def _truth(self, sws: list[int], window: int):
        """Balaye les 2^n combinaisons des switches sws (les autres entrées gardent leur valeur).

        Pour chaque combinaison : TRUTH_SETTLE_CYC cycles pour laisser le design réagir, puis
        une fenêtre de mesure. Une LED vaut 1 si elle est active ≥ 50 % de la fenêtre ; un afficheur
        multiplexé n'apparaît que si son anode est activée pendant la fenêtre."""
        w = self.wiring
        base = {"sws": sws, "window": window,
                "inputs": dict(w.inputs) if w else {}, "outputs": dict(w.outputs) if w else {}}
        total = 1 << len(sws)
        rows: list[dict] = []
        try:
            sim = self.sim
            if not sim or sim.error or self.status != "running":
                self._set_truth({**base, "status": "error", "msg": T("Aucune simulation en cours.", "No simulation running.")})
                return
            self.truth_cancel.clear()
            with self.board.lock:
                sw0, btn = self.board.sw, self.board.btn
            sw0 &= ~sum(1 << s for s in sws)
            self._set_truth({**base, "status": "running", "done": 0, "total": total})
            t0 = last = time.perf_counter()
            with sim.io_lock:
                for k in range(total):
                    if self.truth_cancel.is_set():
                        break
                    sw = sw0
                    for j, s in enumerate(sws):
                        if (k >> j) & 1:
                            sw |= 1 << s
                    bits = encode_inputs(sw, btn)
                    sim.measure(bits, TRUTH_SETTLE_CYC)
                    rows.append(truth_row(sw, *sim.measure(bits, window)))
                    now = time.perf_counter()
                    if now - last > 0.15:
                        last = now
                        self._set_truth({**base, "status": "running", "done": k + 1, "total": total})
            el = time.perf_counter() - t0
            if self.truth_cancel.is_set():
                self._truth_cancelled(base, len(rows), total)
                return
            self._set_truth({**base, "status": "done", "total": total, "elapsed": el, "rows": rows})
            self.log(T(f"Table de vérité : {total} combinaisons en {el:.1f} s.",
                       f"Truth table: {total} combinations in {el:.1f} s."), "ok")
        except Exception as e:  # noqa: BLE001
            if self.truth_cancel.is_set():
                self._truth_cancelled(base, len(rows), total)
            else:
                self._set_truth({**base, "status": "error", "msg": T("Simulation interrompue : ", "Simulation interrupted: ") + str(e)})
        finally:
            self.truth_lock.release()

    def meta(self) -> dict:
        w = self.wiring
        err, err_kind = self.last_error, "build"
        if not err and self.sim and self.sim.error:
            err, err_kind = self.sim.error, "sim"
        return {
            "project": self.project_name,
            "has_project": self.has_project(),
            "project_path": self.project_path,
            "status": self.status if not (self.sim and self.sim.error) else "error",
            "error": err,
            "error_kind": err_kind,
            "watch": self.watch_on,
            "lang": LANG,
            "lang_cli": bool(getattr(self.args, "lang", None)),  # --lang explicite : la page la respecte
            "init_zero": not self.args.no_init,
            "inputs": dict(w.inputs) if w else {},
            "outputs": dict(w.outputs) if w else {},
            "info": self.project_info,
            "engine": self.engine,
            "pins": BOARD_PINS,
            "clk_mhz": REAL_HZ / 1e6,
        }


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code: int, body: bytes, ctype: str):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlsplit(self.path)
            if url.path in ("/", "/index.html"):
                self._send(200, (WEB_DIR / "index.html").read_bytes(), "text/html; charset=utf-8")
            elif url.path == "/events":
                self._events()
            elif url.path == "/projects":
                refresh = parse_qs(url.query).get("refresh") == ["1"]
                self._send(200, json.dumps(app.projects(refresh)).encode(), "application/json")
            else:
                self._send(404, b"introuvable", "text/plain")

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0) or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/input":
                app.board.set_inputs(int(data.get("sw", 0)), int(data.get("btn", 0)))
                self._send(204, b"", "text/plain")
            elif self.path == "/rebuild":
                threading.Thread(target=app.rebuild, daemon=True).start()
                self._send(204, b"", "text/plain")
            elif self.path == "/truth":
                sws = sorted({int(s) for s in data.get("sws", []) if 0 <= int(s) < 16})
                window = max(10, min(TRUTH_MAX_WINDOW, int(data.get("window", 1000))))
                if not 1 <= len(sws) <= TRUTH_MAX_INPUTS:
                    self._send(400, T(f"1 à {TRUTH_MAX_INPUTS} switches", f"1 to {TRUTH_MAX_INPUTS} switches").encode(),
                               "text/plain")
                elif app.start_truth(sws, window):
                    self._send(204, b"", "text/plain")
                else:
                    self._send(409, b"table de verite deja en cours", "text/plain")
            elif self.path == "/project":
                try:
                    app.open_project(str(data.get("path", "")))
                except BuildError as e:
                    self._send(400, json.dumps({"error": str(e)}).encode(), "application/json")
                else:
                    self._send(204, b"", "text/plain")
            elif self.path == "/truth/cancel":
                app.truth_cancel.set()
                self._send(204, b"", "text/plain")
            elif self.path == "/config":
                if "watch" in data:
                    app.watch_on = bool(data["watch"])
                    app.log(T("Recompilation à la sauvegarde activée.", "Rebuild on save enabled.") if app.watch_on
                            else T("Recompilation à la sauvegarde désactivée.", "Rebuild on save disabled."))
                if data.get("lang") in ("fr", "en") and data["lang"] != LANG:
                    set_lang(data["lang"])
                    with app.cond:
                        app.cond.notify_all()
                    if app.status == "error" or app.sim and app.sim.error:
                        threading.Thread(target=app.rebuild, daemon=True).start()  # message d'erreur dans la langue choisie
                self._send(204, b"", "text/plain")
            else:
                self._send(404, b"introuvable", "text/plain")

        def _events(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            sent_log = 0
            sent_truth = -1
            last_meta = None
            try:
                while True:
                    with app.cond:
                        app.cond.wait(timeout=1 / 30)
                        new_logs = [l for l in app.logs if l[0] > sent_log]
                        truth_seq, truth = app.truth_seq, app.truth
                    payload = {"state": app.board.snapshot()}
                    if truth_seq != sent_truth:
                        sent_truth = truth_seq
                        payload["truth"] = truth
                    meta = app.meta()
                    if meta != last_meta:
                        payload["meta"] = last_meta = meta
                    if new_logs:
                        sent_log = new_logs[-1][0]
                        payload["logs"] = [{"kind": k, "msg": m} for _, k, m in new_logs]
                    self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode())
                    self.wfile.flush()
                    time.sleep(1 / 30)
            except (BrokenPipeError, ConnectionResetError):
                pass

    return Handler


# --------------------------------------------------------------------------
# Mode sans interface (tests)
# --------------------------------------------------------------------------
SEG_CHARS = {
    "abcdef": "0", "bc": "1", "abdeg": "2", "abcdg": "3", "bcfg": "4", "acdfg": "5",
    "acdefg": "6", "abc": "7", "abcdefg": "8", "abcdfg": "9", "abcfg": "9",
    "abcefg": "A", "cdefg": "b", "adef": "C", "cdeg": "c", "bcdeg": "d", "adefg": "E",
    "aefg": "F", "g": "-", "": " ", "abfg": "°", "def": "L", "bcefg": "H",
}


def decode_digit(pat: list[float]) -> str:
    on = "".join(ch for ch, v in zip("abcdefg", pat) if v > 0.5)
    return SEG_CHARS.get(on, "?")


def headless(app: App) -> int:
    a = app.args
    app.rebuild()
    if app.status != "running":
        return 1
    sim = app.sim
    sim.stop_evt.set()  # on pilote nous-mêmes la simulation
    sim.thread.join(timeout=1)
    sw = int(a.sw, 2) if a.sw else 0  # "0101" = SW3..SW0
    btn = int(a.btn, 2) if a.btn else 0
    app.board.set_inputs(sw, btn)
    target = a.ms * 1_000_000
    t0 = time.perf_counter()
    while app.board.sim_ns < target:
        sim.step(min(500_000, (target - app.board.sim_ns) // CLK_PERIOD_NS or 1))
    el = time.perf_counter() - t0
    st = app.board.snapshot()
    sim.stop_evt.set()
    sim.proc.kill()
    ratio = st["sim_ns"] / 1e9 / el
    print(T(f"Simulé {st['sim_ns'] / 1e6:.1f} ms en {el:.2f} s (×{ratio:.4f} temps réel)",
            f"Simulated {st['sim_ns'] / 1e6:.1f} ms in {el:.2f} s (×{ratio:.4f} real time)"))
    print("SW15..0  :", format(sw, "016b"))
    print("LED15..0 :", "".join("●" if v > 0.5 else "·" for v in reversed(st["leds"])))
    print("AN7..0   :", "".join(decode_digit(p) for p in reversed(st["digits"])))
    if st["undef"]:
        print(T("Indéfinies (U/X) :", "Undefined (U/X):"), ", ".join(st["undef"]))
    return 0


def main() -> int:
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=("fr", "en"))
    set_lang(pre.parse_known_args()[0].lang or detect_lang())

    ap = argparse.ArgumentParser(description=T("nexys-sim : simulateur Nexys A7 (Verilator / GHDL)",
                                               "nexys-sim: Nexys A7 simulator (Verilator / GHDL)"))
    ap.add_argument("xpr", nargs="?",
                    help=T("projet Vivado .xpr ou son dossier (sinon : projet du dossier courant, "
                           "puis dernier projet ouvert ; on peut aussi le choisir dans la page)",
                           "Vivado .xpr project or its folder (otherwise: project in the current folder, "
                           "then last opened project; it can also be picked in the page)"))
    ap.add_argument("--src", nargs="+", help=T("fichiers VHDL (sans .xpr)", "VHDL files (without .xpr)"))
    ap.add_argument("--xdc", nargs="+", help=T("fichiers .xdc (sans .xpr)", ".xdc files (without .xpr)"))
    ap.add_argument("--top", help=T("entité principale (sinon lue dans le .xpr)", "top entity (otherwise read from the .xpr)"))
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true", help=T("ne pas ouvrir le navigateur", "do not open the browser"))
    ap.add_argument("--no-init", action="store_true",
                    help=T("ne pas initialiser les signaux à 0 (comportement de simulation pur)",
                           "do not initialise signals to 0 (pure simulation behaviour)"))
    ap.add_argument("--moteur", "--engine", dest="moteur", choices=("auto", "verilator", "ghdl"), default="auto",
                    help=T("auto (défaut) : Verilator si le design est synthétisable, sinon GHDL. "
                           "ghdl : simulation 9 états (détecte les U/X), environ 35× plus lente",
                           "auto (default): Verilator if the design synthesises, otherwise GHDL. "
                           "ghdl: 9-state simulation (detects U/X), about 35× slower"))
    ap.add_argument("--no-watch", action="store_true",
                    help=T("ne pas recompiler automatiquement quand un fichier du projet est sauvegardé",
                           "do not rebuild automatically when a project file is saved"))
    ap.add_argument("--racine", "--root", dest="racine", default="~/Documents",
                    help=T("dossier où le sélecteur de la page cherche les projets (défaut : ~/Documents)",
                           "folder where the page's project picker looks for projects (default: ~/Documents)"))
    ap.add_argument("--lang", choices=("fr", "en"),
                    help=T("langue des messages (défaut : selon la variable LANG ; modifiable dans la page)",
                           "message language (default: from the LANG variable; can be changed in the page)"))
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--headless", action="store_true", help=T("simule sans interface et affiche l'état", "simulate without UI and print the state"))
    ap.add_argument("--sw", help=T("mode headless : switches, SW0 à droite (ex. 0101)", "headless mode: switches, SW0 on the right (e.g. 0101)"))
    ap.add_argument("--btn", help=T("mode headless : boutons RDLUC en binaire", "headless mode: RDLUC buttons in binary"))
    ap.add_argument("--ms", type=float, default=20, help=T("mode headless : durée simulée (ms)", "headless mode: simulated time (ms)"))
    args = ap.parse_args()
    if args.headless and not args.xpr and not args.src:
        ap.error(T("le mode --headless demande un .xpr ou --src", "--headless needs an .xpr or --src"))
    url = f"http://127.0.0.1:{args.port}/"

    if not args.headless:
        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), None)
        except OSError:
            return use_running_instance(args, url)

    if not args.xpr and not args.src:
        found, _ = scan_projects(Path.cwd(), max_depth=3, budget_s=1.5)
        recent = next((p for p in load_recents() if Path(p).exists()), None)
        if len(found) == 1:
            args.xpr = str(found[0])
            print(T("Projet du dossier courant : ", "Project in the current folder: ") + tilde(found[0]))
        elif recent:
            args.xpr = recent
            print(T("Dernier projet ouvert : ", "Last opened project: ") + tilde(Path(recent)))
        else:
            print(T("Aucun projet : choisis-en un dans la page.", "No project: pick one in the page."))

    app = App(args)
    if args.headless:
        return headless(app)

    server.RequestHandlerClass = make_handler(app)
    server.daemon_threads = True
    print(f"nexys-sim : {url}  " + T("(Ctrl+C pour quitter)", "(Ctrl+C to quit)"))
    threading.Thread(target=app.rebuild, daemon=True).start()
    threading.Thread(target=app.watch_loop, daemon=True).start()
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if app.sim:
            app.sim.stop()
    return 0


def use_running_instance(args, url: str) -> int:
    """Le port est pris : si c'est un nexys-sim, lui passer le projet demandé et ouvrir la page."""
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            if b"nexys-sim" not in r.read(2000):
                raise OSError
    except OSError:
        print(T(f"Le port {args.port} est déjà utilisé par un autre programme : essaie --port {args.port + 1}.",
                f"Port {args.port} is already used by another program: try --port {args.port + 1}."), file=sys.stderr)
        return 1
    if args.src:
        print(T("nexys-sim tourne déjà : --src n'est possible qu'au premier lancement "
                "(ou utilise --port pour une seconde instance).",
                "nexys-sim is already running: --src only works on the first launch "
                "(or use --port for a second instance)."), file=sys.stderr)
        return 1
    if args.xpr:
        req = urllib.request.Request(url + "project", method="POST",
                                     data=json.dumps({"path": str(Path(args.xpr).expanduser().resolve())}).encode())
        try:
            urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as e:
            print(json.loads(e.read() or b"{}").get("error", e), file=sys.stderr)
            return 1
        print(T("nexys-sim tourne déjà : projet ouvert dans ", "nexys-sim is already running: project opened in ") + url)
    else:
        print(T("nexys-sim tourne déjà : ", "nexys-sim is already running: ") + url)
    if not args.no_browser:
        webbrowser.open(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
