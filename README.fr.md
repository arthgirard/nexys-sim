# nexys-sim — simulateur Nexys A7

*[English](README.md) · Français*

Simule un projet Vivado (VHDL) et affiche une Nexys A7 dans le navigateur :
16 switches, 5 boutons + CPU_RESET, 16 LEDs, 2 LEDs RGB, 8 afficheurs 7 segments.

```sh
nexys-sim                              # ouvre http://127.0.0.1:8765
nexys-sim ~/chemin/vers/projet.xpr     # ou un .xpr / un dossier précis
```

`nexys-sim` est un alias (`~/.zshrc`) de `python3 ~/Documents/Outils/nexys-sim/nexys_sim.py`.

**Langue** : bouton **FR / EN** dans la barre du haut (mémorisé par le navigateur). Il change aussi
la langue des messages du serveur (erreurs, journal). Au lancement : `--lang fr|en`, sinon selon
la variable `LANG`.

## Choix du projet

Sans argument, `nexys-sim` ouvre le projet du dossier courant s'il y en a un seul, sinon le
dernier projet ouvert, sinon la fenêtre de sélection. Dans la page, le nom du projet (barre du
haut) ou la touche <kbd>P</kbd> ouvre le **sélecteur** :

- projets récents, puis tous les `.xpr` trouvés sous `~/Documents` (`--racine DOSSIER` pour en
  choisir un autre ; alias `--root`), du plus récemment modifié au plus ancien ;
- recherche par nom, top ou chemin (`labo3 seg`) ; <kbd>↑</kbd> <kbd>↓</kbd> <kbd>Entrée</kbd> ;
- on peut aussi coller un chemin (`~/…/labo4` ou `…/labo4.xpr`) ;
- les exports Logisim (`…/Bin_7Seg/sandbox/vp/vp.xpr`) sont nommés d'après leur dossier.

Si `nexys-sim` tourne déjà, `nexys-sim autre.xpr` bascule la page ouverte sur ce projet au lieu
de lancer une seconde instance. Projets récents : `~/.config/nexys-sim/recents.json`.

Recompilation automatique à chaque sauvegarde d'un `.vhd`, du `.xdc` ou de la liste des sources
du `.xpr` (case **Auto** dans la barre du haut, `--no-watch` pour la désactiver au lancement).
Sinon : bouton **Recompiler** ou touche <kbd>R</kbd>. Une erreur de compilation s'affiche en
bandeau rouge au-dessus de la carte (`fichier:ligne`), et la carte est voilée tant qu'elle n'est
plus à jour.

## Dans la page

- **Switches** : clic, ou saisie directe de `SW[15:0]` : `0x00FF`, `x"00FF"`, `00FFh`, `0b0101`,
  `"0101"`, `0101b` ou décimal ; boutons *Tout à 0 / Tout à 1 / Inverser*.
- **Boutons** : clic maintenu, ou <kbd>←</kbd> <kbd>↑</kbd> <kbd>→</kbd> <kbd>↓</kbd> <kbd>Espace</kbd>.
- **Table de vérité** : cocher les switches à balayer (12 au plus) puis *Générer*. Pour chaque
  combinaison, le simulateur applique les entrées, laisse 100 cycles au design, puis mesure les
  sorties sur une fenêtre : 10 µs en *Auto* sans afficheurs, 20 ms avec afficheurs (il faut couvrir
  un balayage complet du multiplexage). Une LED vaut `~` si elle n'est allumée qu'une partie du
  temps. Les switches non cochés et les boutons gardent leur valeur. La carte est en pause pendant
  le balayage. *Copier (CSV)* pour coller le résultat dans un tableur. Pour un circuit séquentiel,
  le résultat dépend de l'état interne au moment du balayage.

## Moteurs

| `--moteur` (ou `--engine`) | Chaîne | Vitesse | U/X |
|---|---|---|---|
| `auto` (défaut) | Verilator si le design se synthétise, sinon GHDL | — | — |
| `verilator` | `ghdl --synth` → netlist Verilog → Verilator (C++) | ≈ ×0,2 du temps réel | non (2 états) |
| `ghdl` | simulation événementielle du VHDL | ≈ ×0,007 | oui (9 états) |

Avec Verilator, un balayage d'afficheurs à ~95 Hz se voit presque comme sur la carte. Si la
synthèse échoue (code non synthétisable : `wait for`, `after`…), l'outil passe sur GHDL et
affiche l'erreur de synthèse dans le journal : Vivado refusera aussi ce code.
`--no-init` force GHDL (les `U` n'existent qu'en 9 états).

Prérequis : `ghdl` ; `verilator` (optionnel, `sudo dnf install verilator`).

## Fonctionnement

- Lit le `.xpr` : sources VHDL de `sources_1`, module top, fichiers `.xdc`.
- Branche les ports du top sur la carte **selon le `.xdc`** (`PACKAGE_PIN`). Une broche fausse
  dans le `.xdc` donne donc le même mauvais résultat que sur la vraie carte. Les avertissements
  (port absent du `.xdc`, contrainte sur un port inexistant…) s'affichent dans le journal.
- Horloge 100 MHz sur `E3`. Les afficheurs multiplexés sont rendus avec persistance.
- Les signaux sans valeur initiale démarrent à 0, comme les bascules du FPGA au chargement
  du bitstream. `--no-init` désactive ça (comportement de simulation pur, `'U'` partout).
- Bandeau orange si une sortie vaut `U`/`X`.

## Limites

- Pas le bitstream : ni synthèse Vivado, ni timing. Simulation fonctionnelle, sans délais.
- Plus lent que le temps réel (voir tableau). Un diviseur vers 1 Hz tourne ≈ 5× trop lentement
  avec Verilator, ≈ 150× avec GHDL.
- Moteur Verilator : ports de 64 bits au plus, pas de port `inout`.
- VHDL seulement (pas de Verilog ni d'IP Vivado). Ports `std_logic`, `std_logic_vector`,
  `unsigned`, `signed`, `bit` avec bornes numériques.

## Autres modes

```sh
# Sans .xpr
nexys-sim --src a.vhd b.vhd --xdc c.xdc --top Top

# Sans interface (test rapide) : SW3..SW0 = 0101, 20 ms simulées
nexys-sim projet.xpr --headless --sw 0101 --ms 20
```

Fichiers compilés : `.build/` (supprimable).
