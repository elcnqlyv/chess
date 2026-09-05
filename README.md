# Chess

A local two-player chess game built with Python and Turtle. Play on the same computer, see available moves, and save a game to pick it up later.

We built this as a group project during our programming studies. It gave us a chance to put what we were learning into practice and work together on a shared application.

## Features

- Click a piece to see its available moves, then click a destination to move it
- Keep track of whose turn it is and which pieces each player has captured
- See the previous move highlighted on the board
- Ask for a random move suggestion
- Save and load a game with keyboard shortcuts
- Automatically promote pawns to queens when they reach the opposite end of the board

## Getting started

You need Python 3 with Tk support and a desktop environment. The game uses Python's standard library, so there are no packages to install with pip.

Clone the repository and open the project folder:

```bash
git clone https://github.com/developerilahe/chess.git
cd chess
```

Start the game:

```bash
python3 main.py
```

On Windows, you can use `py main.py` instead.

If Python reports that `tkinter` or `_tkinter` is missing, install Tk support for your Python installation. You can check that Tk works by running `python3 -m tkinter`, which should open a small test window.

## How to play

White moves first. Click one of your pieces to select it, then click a square marked with a green dot. Both players take turns using the same mouse.

Click inside the game window before using the keyboard shortcuts. Press the keys without Shift.

| Control | Action |
| --- | --- |
| Mouse click | Select a piece or move to a highlighted square |
| `r` | Restart the game |
| `s` | Save the current game |
| `l` | Load the saved game |
| `h` | Show a random move suggestion in orange |

Saving writes to `chess_save.json` in the folder you launched the game from. Each save replaces the previous one. Loading restores the board, turn, move count, captured pieces, and game result.

## Game rules

This project uses a simplified version of chess. Pieces follow their basic movement patterns, but check, checkmate, castling, and en passant are not implemented. A king can move into an attacked square, and capturing the opponent's king wins the game.

If neither king has been captured after 60 individual moves across both players, the game ends in a draw. Each player's turn counts as one move toward that limit.

Pawns always promote to queens. Hints choose a random move allowed by the game, so they are suggestions rather than strategic advice.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Game window, mouse and keyboard controls, and status messages |
| `board.py` | Board drawing, piece display, and board state |
| `game.py` | Movement rules, turns, captures, hints, and saving and loading |
| `constants.py` | Board dimensions, colors, piece symbols, and shared settings |

## Team

Created together by **Aydan, Aytaj, Ilaha, Gadir, and Elchin** as part of our programming studies.
