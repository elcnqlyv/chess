SIZE = 8
CELL = 70
BOARD_SIZE = SIZE * CELL              # 560
HALF = BOARD_SIZE / 2                 # 280

TOP_MARGIN = 130      # space above board for title/status/tray
BOTTOM_MARGIN = 110   # space below board for tips

BOARD_Y_OFFSET = -(TOP_MARGIN - BOTTOM_MARGIN) / 2   # keeps layout centered

WINDOW_W = BOARD_SIZE + 140
WINDOW_H = BOARD_SIZE + TOP_MARGIN + BOTTOM_MARGIN

BOARD_TOP = HALF + BOARD_Y_OFFSET
BOARD_BOTTOM = -HALF + BOARD_Y_OFFSET

LIGHT, DARK = "#F0D9B5", "#B58863"
HIGHLIGHT, VALID, LAST_MOVE, HINT_COLOR = "#7B61FF", "#7BFF7B", "#F5F56B", "#FF9F43"

SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
}

VALUES = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}  # for ranking captures

FILES = "abcdefgh"
RANKS = "87654321"

WHITE, BLACK = 1, 2
SAVE_FILE = "chess_save.json"
