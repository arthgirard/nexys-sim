# nexys-sim — Nexys A7 simulator

*English · [Français](README.fr.md)*

Simulates a Vivado (VHDL) project and shows a Nexys A7 board in the browser:
16 switches, 5 buttons + CPU_RESET, 16 LEDs, 2 RGB LEDs, 8 seven-segment displays.

```sh
nexys-sim                              # opens http://127.0.0.1:8765
nexys-sim ~/path/to/project.xpr        # or a specific .xpr / folder
```

`nexys-sim` is an alias (`~/.zshrc`) for `python3 ~/Documents/Outils/nexys-sim/nexys_sim.py`.

**Language**: **FR / EN** button in the top bar (remembered by the browser). It also switches
the language of the server messages (errors, log). At launch: `--lang fr|en`, otherwise taken
from the `LANG` variable.

## Choosing a project

Without an argument, `nexys-sim` opens the project in the current folder if there is exactly
one, otherwise the last opened project, otherwise the picker. In the page, the project name (top
bar) or the <kbd>P</kbd> key opens the **picker**:

- recent projects, then every `.xpr` found under `~/Documents` (`--root FOLDER` to use another
  one; French alias `--racine`), most recently modified first;
- search by name, top entity or path (`labo3 seg`); <kbd>↑</kbd> <kbd>↓</kbd> <kbd>Enter</kbd>;
- you can also paste a path (`~/…/labo4` or `…/labo4.xpr`);
- Logisim exports (`…/Bin_7Seg/sandbox/vp/vp.xpr`) are named after their folder.

If `nexys-sim` is already running, `nexys-sim other.xpr` switches the open page to that project
instead of starting a second instance. Recent projects: `~/.config/nexys-sim/recents.json`.

Automatic rebuild whenever a `.vhd`, the `.xdc` or the `.xpr` source list is saved (**Auto**
checkbox in the top bar, `--no-watch` to disable it at launch). Otherwise: **Rebuild** button or
the <kbd>R</kbd> key. A build error shows as a red banner above the board (`file:line`), and the
board is dimmed while it is out of date.

## In the page

- **Switches**: click, or type `SW[15:0]` directly: `0x00FF`, `x"00FF"`, `00FFh`, `0b0101`,
  `"0101"`, `0101b` or decimal; *All 0 / All 1 / Invert* buttons.
- **Buttons**: click and hold, or <kbd>←</kbd> <kbd>↑</kbd> <kbd>→</kbd> <kbd>↓</kbd> <kbd>Space</kbd>.
- **Truth table**: tick the switches to sweep (12 at most), then *Generate*. For each
  combination, the simulator applies the inputs, gives the design 100 cycles, then measures the
  outputs over a window: 10 µs in *Auto* without displays, 20 ms with displays (it must cover a
  full multiplexing scan). An LED shows `~` if it is only lit part of the time. Unticked switches
  and the buttons keep their value. The board is paused during the sweep. *Copy (CSV)* to paste
  the result into a spreadsheet. For a sequential circuit, the result depends on the internal
  state at the time of the sweep.

## Engines

| `--engine` (or `--moteur`) | Pipeline | Speed | U/X |
|---|---|---|---|
| `auto` (default) | Verilator if the design synthesises, otherwise GHDL | — | — |
| `verilator` | `ghdl --synth` → Verilog netlist → Verilator (C++) | ≈ 0.2× real time | no (2-state) |
| `ghdl` | event-driven VHDL simulation | ≈ 0.007× | yes (9-state) |

With Verilator, a display scan at ~95 Hz looks almost like on the real board. If synthesis
fails (non-synthesisable code: `wait for`, `after`…), the tool falls back to GHDL and shows the
synthesis error in the log: Vivado will reject that code too.
`--no-init` forces GHDL (`U` only exists in 9-state logic).

Requirements: `ghdl`; `verilator` (optional, `sudo dnf install verilator`).

## How it works

- Reads the `.xpr`: VHDL sources from `sources_1`, top module, `.xdc` files.
- Connects the top's ports to the board **according to the `.xdc`** (`PACKAGE_PIN`). A wrong pin
  in the `.xdc` therefore gives the same wrong result as on the real board. Warnings (port
  missing from the `.xdc`, constraint on a non-existent port…) are shown in the log.
- 100 MHz clock on `E3`. Multiplexed displays are rendered with persistence.
- Signals without an initial value start at 0, like the FPGA flip-flops when the bitstream is
  loaded. `--no-init` turns this off (pure simulation behaviour, `'U'` everywhere).
- Orange banner if an output is `U`/`X`.

## Limitations

- Not the bitstream: no Vivado synthesis, no timing. Functional simulation, without delays.
- Slower than real time (see table). A divider down to 1 Hz runs ≈ 5× too slowly with Verilator,
  ≈ 150× with GHDL.
- Verilator engine: ports of 64 bits at most, no `inout` ports.
- VHDL only (no Verilog, no Vivado IP). Ports `std_logic`, `std_logic_vector`, `unsigned`,
  `signed`, `bit` with numeric bounds.

## Other modes

```sh
# Without an .xpr
nexys-sim --src a.vhd b.vhd --xdc c.xdc --top Top

# Without UI (quick test): SW3..SW0 = 0101, 20 ms simulated
nexys-sim project.xpr --headless --sw 0101 --ms 20
```

Build files: `.build/` (safe to delete).
