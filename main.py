import turtle
from constants import *
from board import draw_board, get_piece, reset_grid
import game

screen = turtle.Screen()
screen.setup(WINDOW_W, WINDOW_H)
screen.bgcolor("#2c3e50")
screen.title("♟ Chess")
screen.tracer(0)
screen.listen()

reset_grid()
hint_move = None  # (fr, fc, tr, tc) or None - shown after pressing H

title_pen = turtle.Turtle(); title_pen.penup(); title_pen.hideturtle()
status = turtle.Turtle(); status.penup(); status.hideturtle()
tray = turtle.Turtle(); tray.penup(); tray.hideturtle()
tip = turtle.Turtle(); tip.penup(); tip.hideturtle()
message = turtle.Turtle(); message.penup(); message.hideturtle()


def draw_title():
    title_pen.clear()
    title_pen.goto(0, BOARD_TOP + 80)
    title_pen.pencolor("white")
    title_pen.write("♟ Chess", align="center", font=("Arial", 26, "bold"))


def update_status():
    status.clear()
    y = BOARD_TOP + 45
    if game.game_over:
        msg = {WHITE: "White wins! 🏆", BLACK: "Black wins! 🏆"}.get(game.winner, "Draw 🤝")
        status.goto(0, y)
        status.pencolor("gold")
        status.write(msg, align="center", font=("Arial", 20, "bold"))
    else:
        name = "White" if game.current_player == WHITE else "Black"
        status.goto(0, y)
        status.pencolor(name.lower())
        status.write(f"{name}'s turn  (move {game.move_count})",
                      align="center", font=("Arial", 18, "bold"))


def update_tray():
    """Show each side's captured material just above the board."""
    tray.clear()
    w = "".join(SYMBOLS[p] for p in game.captured_summary(WHITE))
    b = "".join(SYMBOLS[p] for p in game.captured_summary(BLACK))
    tray.goto(0, BOARD_TOP + 15)
    tray.pencolor("#cccccc")
    tray.write(f"White captured: {w or '-'}    Black captured: {b or '-'}",
               align="center", font=("Arial", 12, "normal"))


def flash_message(text, secs=1500):
    message.clear()
    message.goto(0, BOARD_BOTTOM - 65)
    message.pencolor("#7BFF7B")
    message.write(text, align="center", font=("Arial", 12, "italic"))
    screen.update()
    screen.ontimer(lambda: (message.clear(), screen.update()), secs)


def redraw():
    hint_pair = ((hint_move[0], hint_move[1]), (hint_move[2], hint_move[3])) if hint_move else None
    draw_board(selected=game.selected, valid_moves=game.valid_moves,
               last_move=game.last_move, hint=hint_pair)
    update_status()
    update_tray()
    screen.update()


def select_if_own_piece(row, col):
    piece = get_piece(row, col)
    if piece and piece.isupper() == (game.current_player == WHITE):
        game.selected = (row, col)
        game.valid_moves = game.get_valid_moves(row, col)
        return True
    return False


def on_click(x, y):
    global hint_move
    if game.game_over:
        return
    col = int((x + HALF) / CELL)
    row = int((HALF - (y - BOARD_Y_OFFSET)) / CELL)
    if not (0 <= row < SIZE and 0 <= col < SIZE):
        return

    hint_move = None  # clear any stale hint once the player acts

    if game.selected is None:
        if select_if_own_piece(row, col):
            redraw()
        return

    fr, fc = game.selected
    if (row, col) in game.valid_moves:
        game.make_move(fr, fc, row, col)
        game.selected, game.valid_moves = None, []
        redraw()
        return

    if not select_if_own_piece(row, col):
        game.selected, game.valid_moves = None, []
    redraw()


def reset_and_update():
    global hint_move
    hint_move = None
    game.reset_game()
    redraw()
    flash_message("New game started")


def save_and_notify():
    flash_message(f"Game saved to {SAVE_FILE}" if game.save_game() else "Save failed")


def load_and_update():
    global hint_move
    hint_move = None
    if game.load_game():
        redraw()
        flash_message(f"Game loaded from {SAVE_FILE}")
    else:
        flash_message("No save file found")


def show_hint():
    """Suggest a random legal move for whoever is to move."""
    global hint_move
    if game.game_over:
        return
    hint_move = game.random_hint(game.current_player)
    flash_message("Hint: orange squares show a possible move" if hint_move else "No legal moves available")
    if hint_move:
        redraw()


screen.onclick(on_click)
screen.onkey(reset_and_update, "r")
screen.onkey(save_and_notify, "s")
screen.onkey(load_and_update, "l")
screen.onkey(show_hint, "h")

draw_title()
redraw()

tip.goto(0, BOARD_BOTTOM - 35)
tip.pencolor("#aaa")
tip.write("Click a piece, then a green dot to move  |  R restart   S save   L load   H hint",
          align="center", font=("Arial", 12, "normal"))
screen.update()

screen.mainloop()