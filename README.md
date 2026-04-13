# Sudoku Collision Visualizer (O(1) Validation)

A desktop Sudoku game built with Python and [Flet](https://flet.dev/), focused on visualizing **collision zones** in real time — the rows, columns, and 3×3 blocks that a given number already occupies. Move validation is done in O(1) time using a precomputed binary highlight map.

---

## Origin

While playing Sudoku one day, I noticed that most apps just let you play — they don't really help you *understand* the game. I wanted something that could serve as a gentle tutorial: a way to visually show a new player which cells a given number is already blocking, so they can start to internalize the rules naturally rather than just guessing. That idea turned into this project.

---

## Features

- **Drag-and-drop gameplay** — drag numbers from the number bank onto the board
- **Click-to-highlight** — click any number in the bank to instantly highlight all cells it cannot legally occupy (its row, column, and block conflicts)
- **O(1) move validation** — uses a precomputed `bin_highlight_map` to check if a cell is legal in constant time, no scanning required
- **Auto-highlight mode** — click the `?` button to cycle through all numbers 1–9 automatically, highlighting each one's collision zone in sequence
- **Random puzzle generation** — a new puzzle is generated on every launch using the `sudoku` library
- **JSON config** — difficulty and highlight interval are controlled from a single config file, no code changes needed

---

## How It Works

### Collision Map (`bin_highlight_map`)

When a number is selected or dragged, the game computes which cells are "blocked" for that number by setting entries to `1` in a 9×9 binary array:

- every cell in the same **row** as an existing instance of that number
- every cell in the same **column**
- every cell in the same **3×3 block**

A move is valid if and only if the target cell has a `0` in this map **and** is currently empty — no iteration over the board needed at validation time.

### Block Map (`block_map`)

A separate 9×9 array is filled once at startup, assigning each cell a block number (1–9). This lets block lookups happen in O(1) instead of computing `(row // 3, col // 3)` repeatedly.

---

## Project Structure

```
.
├── main.py       # UI layer — Flet components, drag/drop, number bank, help button
├── logic.py      # Game logic — grid state, highlight map, move validation, puzzle loading
└── config.json   # User-facing settings — difficulty and highlight interval
```

---

## Configuration

All tuneable settings live in `config.json` at the project root:

```json
{
    "difficulty": 0.5,
    "highlight_interval_seconds": 0.5
}
```

| Key | Description | Range |
|---|---|---|
| `difficulty` | How many cells are left empty in the generated puzzle | `0.1` (easy) – `0.9` (very hard) |
| `highlight_interval_seconds` | Time between each number in auto-highlight cycle | Any positive float |

Edit this file and relaunch the app — no code changes needed.

---

## Requirements

- Python 3.9+
- [Flet](https://flet.dev/) — `pip install flet`
- [py-sudoku](https://pypi.org/project/py-sudoku/) — `pip install py-sudoku`

---

## Running the App

```bash
python main.py
```

---

## Controls

| Action | How |
|---|---|
| Place a number | Drag from the number bank onto a board cell |
| Highlight collision zone | Click a number in the bank |
| Auto-cycle highlights | Click the `?` icon button (turns yellow when active) |
| Stop auto-cycle | Click the `?` icon button again |
