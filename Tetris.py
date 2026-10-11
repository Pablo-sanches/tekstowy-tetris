import time
import os
import msvcrt
import random

level = 0
score = 0
lines = 0

shapes = (
    ((1, 1, 1, 1),),

    ((1, 1),
     (1, 1)),

    ((1, 0),
     (1, 0),
     (1, 1)),

    ((0, 1),
     (0, 1),
     (1, 1)),

    ((1, 0),
     (1, 1),
     (0, 1)),

    ((0, 1),
     (1, 1),
     (1, 0)),

    ((0, 1, 0),
     (1, 1, 1)),
)

left_panel = [
    "TETRIS",
    "",
    f"SCORE: {score}",
    f"LEVEL: {level}",
    f"LINES: {lines}"
]

right_panel = [
    "CONTROLS",
    "",
    "← / → - MOVE",
    "↓ - HARD DROP",
    "↑ - ROTATE"
]


game_space = [
    [2] + [0] * 10 + [2]
    for _ in range(20)
]

current_shape = random.choice(shapes)
shape_x = 5
shape_y = 0


def game_over():
    for i in range(len(game_space)):
        game_space[i] = [2] + [0] * 10 + [2]

        os.system("cls")

        for row in game_space:
            board_row = ""

            for cell in row:
                if cell == 0:
                    board_row += " ."
                elif cell == 1:
                    board_row += "██"
                elif cell == 2:
                    board_row += "| "

            print(f"{'':18}{board_row:^28}")

        time.sleep(0.08)

    os.system("cls")

    for i, row in enumerate(game_space):
        board_row = ""

        for cell in row:
            if cell == 0:
                board_row += " ."
            elif cell == 1:
                board_row += "██"
            elif cell == 2:
                board_row += "| "

        if i == 9:
            board_row = "| " + " GAME OVER ".center(20) + "|"

        print(f"{'':18}{board_row:^28}")

    print(f"\n{'':18}{f'SCORE: {score}':^28}")
    print(f"{'':18}{f'LINES: {lines}':^28}")
    print(f"\n{'':18}{'Press Enter to restart':^28}")

    input()
    return True


def rotate_shape(shape):
    return tuple(
        tuple(row[i] for row in reversed(shape))
        for i in range(len(shape[0]))
    )


def can_move(x, y, shape):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 1:
                if y + i >= len(game_space):
                    return False

                if x + j < 0 or x + j >= len(game_space[0]):
                    return False

                if game_space[y + i][x + j] != 0:
                    return False

    return True


def update_physics():
    global shape_y, shape_x, current_shape
    global score, level, lines, drop_delay

    if can_move(shape_x, shape_y + 1, current_shape):
        shape_y += 1

    else:
        for i, row in enumerate(current_shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    game_space[shape_y + i][shape_x + j] = 1

        current_shape = random.choice(shapes)
        shape_x = 5
        shape_y = 0

        if not can_move(shape_x, shape_y, current_shape):
            return game_over()

        full_rows = []

        for index, row in enumerate(game_space):
            count = 0

            for cell in row:
                if cell == 1:
                    count += 1

            if count == 10:
                full_rows.append(index)

        for index in sorted(full_rows, reverse=True):
            del game_space[index]
            game_space.insert(0, [2] + [0] * 10 + [2])

        lines += len(full_rows)

        if len(full_rows) == 1:
            score += 40 * level

        elif len(full_rows) == 2:
            score += 100 * level

        elif len(full_rows) == 3:
            score += 300 * level

        elif len(full_rows) == 4:
            score += 1200 * level
            level += 1
            drop_delay = max(0.2, 0.7 - (level - 1) * 0.2)

    time.sleep(drop_delay)
    return False


def game_renderer():
    left_panel[2] = f"SCORE: {score}"
    left_panel[3] = f"LEVEL: {level}"
    left_panel[4] = f"LINES: {lines}"

    display_space = [row.copy() for row in game_space]

    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell == 1:
                display_space[shape_y + i][shape_x + j] = 1

    for i in range(len(display_space)):
        row = ""

        left = left_panel[i] if i < len(left_panel) else ""
        right = right_panel[i] if i < len(right_panel) else ""

        for j in range(len(display_space[i])):
            if display_space[i][j] == 0:
                row += " ."
            elif display_space[i][j] == 1:
                row += "██"
            elif display_space[i][j] == 2:
                row += "|"

        print(f"{left:<18}{row:^28}{right:<18}")

    print(f"{'':<18}{'▔' * 20:^28}")


while True:
    while True:
        try:
            os.system("cls")
            print("\n\n\n\n\n\n\n\n\n\n                   Tetris\n\n\n\n\n\n\n\n\n\n")
            level = int(input("Choose difficulty level (1-9): "))

            if 1 <= level <= 9:
                break

            print("The level must be in the range of 1-9!")
            time.sleep(2)

        except ValueError:
            print("You must enter an integer!")
            time.sleep(2)

    left_panel[3] = f"LEVEL: {level}"

    drop_delay = max(0.2, 0.7 - (level - 1) * 0.2)

    while True:
        os.system("cls")
        game_renderer()

        if update_physics():
            break

        if msvcrt.kbhit():
            key = msvcrt.getwch()

            if key in ("\x00", "\xe0"):
                key = msvcrt.getwch()

                if key == "H":
                    rotated_shape = rotate_shape(current_shape)

                    if can_move(shape_x, shape_y, rotated_shape):
                        current_shape = rotated_shape

                elif key == "P":
                    while can_move(shape_x, shape_y + 1, current_shape):
                        shape_y += 1

                elif key == "K":
                    if can_move(shape_x - 1, shape_y, current_shape):
                        shape_x -= 1

                elif key == "M":
                    if can_move(shape_x + 1, shape_y, current_shape):
                        shape_x += 1

    game_space = [
        [2] + [0] * 10 + [2]
        for _ in range(20)
    ]

    score = 0
    lines = 0
    current_shape = random.choice(shapes)
    shape_x = 5
    shape_y = 0