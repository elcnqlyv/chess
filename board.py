# ============================================================
# Draw board with pieces at correct geometric centers
# ============================================================

import turtle
from constants import *

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()

label_pen = turtle.Turtle()
label_pen.speed(0)
label_pen.hideturtle()
label_pen.penup()

grid = [['' for _ in range(SIZE)] for _ in range(SIZE)]


def reset_grid():
    grid[0] = list('rnbqkbnr')
    grid[1] = list('pppppppp')
    for r in range(2, 6):
        grid[r] = [''] * SIZE
    grid[6] = list('PPPPPPPP')
    grid[7] = list('RNBQKBNR')


def square_pos(row, col):
    """Return (top_left, center) screen coords for a square (offset included)."""
    x = -HALF + col * CELL
    y = HALF - row * CELL + BOARD_Y_OFFSET
    return (x, y), (x + CELL / 2, y - CELL / 2)


def draw_outline(row, col, color, width=4):
    (x, y), _ = square_pos(row, col)
    pen.goto(x, y)
    pen.pencolor(color)
    pen.pensize(width)
    pen.pendown()
    for _ in range(4):
        pen.forward(CELL)
        pen.right(90)
    pen.penup()


def draw_dot(cx, cy, color, radius):
    pen.goto(cx, cy)
    pen.pencolor(color)
    pen.fillcolor(color)
    pen.pendown()
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()
    pen.penup()


def draw_board(selected=None, valid_moves=None, last_move=None, hint=None):
    pen.clear()

    for row in range(SIZE):
        for col in range(SIZE):
            (x, y), _ = square_pos(row, col)
            pen.goto(x, y)
            pen.fillcolor(LIGHT if (row + col) % 2 == 0 else DARK)
            pen.pendown()
            pen.begin_fill()
            for _ in range(4):
                pen.forward(CELL)
                pen.right(90)
            pen.end_fill()
            pen.penup()

    if last_move:
        for r, c in last_move:
            draw_outline(r, c, LAST_MOVE, 3)

    for row in range(SIZE):
        for col in range(SIZE):
            piece = grid[row][col]
            if piece:
                _, (cx, cy) = square_pos(row, col)
                pen.goto(cx, cy - 12)  # baseline adjustment for font
                pen.pencolor("white" if piece.isupper() else "black")
                pen.write(SYMBOLS[piece], align="center", font=("Arial", 28, "normal"))

    if selected:
        draw_outline(*selected, HIGHLIGHT, 4)

    if valid_moves:
        for r, c in valid_moves:
            _, (cx, cy) = square_pos(r, c)
            draw_dot(cx, cy, VALID, CELL / 6)

    if hint:
        (fr, fc), (tr, tc) = hint
        draw_outline(fr, fc, HINT_COLOR, 3)
        _, (cx, cy) = square_pos(tr, tc)
        draw_dot(cx, cy, HINT_COLOR, CELL / 5)

    draw_labels()


def draw_labels():
    """File (a-h) and rank (1-8) coordinate labels around the board."""
    label_pen.clear()
    label_pen.pencolor("#dddddd")
    for col, letter in enumerate(FILES):
        _, (cx, _) = square_pos(SIZE - 1, col)
        label_pen.goto(cx, BOARD_BOTTOM - 22)
        label_pen.write(letter, align="center", font=("Arial", 11, "normal"))
    for row, number in enumerate(RANKS):
        _, (_, cy) = square_pos(row, 0)
        label_pen.goto(-HALF - 25, cy - 8)
        label_pen.write(number, align="center", font=("Arial", 11, "normal"))


def get_piece(row, col):
    return grid[row][col] if 0 <= row < SIZE and 0 <= col < SIZE else ''


def set_piece(row, col, piece):
    if 0 <= row < SIZE and 0 <= col < SIZE:
        grid[row][col] = piece