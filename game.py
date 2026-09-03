# ============================================================
# Game logic
# ============================================================

import json
import random

from constants import *
from board import grid, get_piece, set_piece, reset_grid

current_player = WHITE
game_over = False
winner = 0
selected = None
valid_moves = []
move_count = 0

captured_by_white = []      # pieces White has captured (lowercase)
captured_by_black = []      # pieces Black has captured (uppercase)
move_history = []           # (fr, fc, tr, tc, piece, captured)
last_move = None            # ((fr, fc), (tr, tc)) - for board highlight
promoted_squares = set()    # squares where a pawn was promoted


def path_clear(fr, fc, tr, tc):
    dr = (tr > fr) - (tr < fr)
    dc = (tc > fc) - (tc < fc)
    r, c = fr + dr, fc + dc
    while (r, c) != (tr, tc):
        if get_piece(r, c):
            return False
        r, c = r + dr, c + dc
    return True


def can_move(fr, fc, tr, tc):
    piece = get_piece(fr, fc)
    if not piece:
        return False
    target = get_piece(tr, tc)
    if target and target.isupper() == piece.isupper():
        return False  # can't capture your own piece

    dr, dc = tr - fr, tc - fc
    p = piece.upper()

    if p == 'P':
        d = -1 if piece.isupper() else 1
        if fc == tc and dr == d and not target:
            return True
        if fc == tc and dr == 2 * d and fr in (1, 6) and not target:
            return not get_piece(fr + d, fc)
        return abs(dc) == 1 and dr == d and bool(target)
    if p == 'N':
        return (abs(dr), abs(dc)) in ((2, 1), (1, 2))
    if p == 'B':
        return abs(dr) == abs(dc) and path_clear(fr, fc, tr, tc)
    if p == 'R':
        return (dr == 0 or dc == 0) and path_clear(fr, fc, tr, tc)
    if p == 'Q':
        return (abs(dr) == abs(dc) or dr == 0 or dc == 0) and path_clear(fr, fc, tr, tc)
    if p == 'K':
        return max(abs(dr), abs(dc)) == 1
    return False


def get_valid_moves(row, col):
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if can_move(row, col, r, c)]


def get_all_moves_for_player(player):
    """All (fr, fc, tr, tc) move tuples available to a player - used for hints."""
    moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            piece = get_piece(r, c)
            if piece and piece.isupper() == (player == WHITE):
                moves += [(r, c, tr, tc) for tr, tc in get_valid_moves(r, c)]
    return moves


def random_hint(player):
    moves = get_all_moves_for_player(player)
    return random.choice(moves) if moves else None


def make_move(fr, fc, tr, tc):
    global current_player, game_over, winner, move_count, last_move
    piece = get_piece(fr, fc)
    target = get_piece(tr, tc)
    set_piece(tr, tc, piece)
    set_piece(fr, fc, '')
    move_count += 1

    if target:
        (captured_by_black if target.isupper() else captured_by_white).append(target)

    if piece.upper() == 'P' and tr in (0, 7):
        set_piece(tr, tc, 'Q' if piece.isupper() else 'q')
        promoted_squares.add((tr, tc))

    move_history.append((fr, fc, tr, tc, piece, target))
    last_move = ((fr, fc), (tr, tc))

    if target and target.upper() == 'K':
        game_over, winner = True, current_player
    elif move_count >= 60:
        game_over, winner = True, 0
    else:
        current_player = BLACK if current_player == WHITE else WHITE
    return True


def captured_summary(player):
    """Pieces captured by `player`, ranked by material value."""
    pieces = captured_by_white if player == WHITE else captured_by_black
    return sorted(pieces, key=lambda p: VALUES[p.upper()], reverse=True)


def reset_game():
    global current_player, game_over, winner, selected, valid_moves, move_count, last_move
    reset_grid()
    current_player, game_over, winner = WHITE, False, 0
    selected, valid_moves, move_count, last_move = None, [], 0, None
    captured_by_white.clear()
    captured_by_black.clear()
    move_history.clear()
    promoted_squares.clear()


def save_game(filename=SAVE_FILE):
    """Serialize the full game state to a JSON file."""
    state = {
        "grid": grid,
        "current_player": current_player,
        "move_count": move_count,
        "captured_by_white": captured_by_white,
        "captured_by_black": captured_by_black,
        "game_over": game_over,
        "winner": winner,
    }
    try:
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)
        return True
    except OSError:
        return False


def load_game(filename=SAVE_FILE):
    """Restore a game state previously written by save_game()."""
    global current_player, move_count, game_over, winner, selected, valid_moves, last_move
    try:
        with open(filename, "r") as f:
            state = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False

    for r in range(SIZE):
        for c in range(SIZE):
            set_piece(r, c, state["grid"][r][c])

    current_player = state["current_player"]
    move_count = state["move_count"]
    game_over = state["game_over"]
    winner = state["winner"]
    selected, valid_moves, last_move = None, [], None

    captured_by_white.clear()
    captured_by_white.extend(state["captured_by_white"])
    captured_by_black.clear()
    captured_by_black.extend(state["captured_by_black"])
    return True