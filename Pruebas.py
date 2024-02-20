import random
import string

EMPTY = ''

UNEXPLORED = '⬛'
WATER = '🟦'
TOUCHED = '🟧'
SUNKEN = '🟥'


def generate_board(
    size: int = 10,
    ships: tuple[tuple[int, int]] = ((5, 1), (4, 1), (3, 2), (2, 1)),
) -> list[list[str]]:
    board = [[EMPTY for _ in range(size)] for _ in range(size)]
    for sheep_size, num_ships in ships:
        placed_ships = 0
        while placed_ships < num_ships:
            sheep_id = f'{sheep_size}{string.ascii_uppercase[placed_ships]}'
            row, col = random.randint(0, size), random.randint(0, size)
            step = random.choice((-1, 1))
            row_step, col_step = (step, 0) if random.randint(0, 1) else (0, step)
            breadcrumbs = []
            for _ in range(sheep_size):
                try:
                    if not (0 <= row < size and 0 <= col < size):
                        raise IndexError()
                    if board[row][col] == EMPTY:
                        board[row][col] = sheep_id
                        breadcrumbs.append((row, col))
                    else:
                        raise IndexError()
                    row += row_step
                    col += col_step
                except IndexError:
                    # reset board
                    for bc in breadcrumbs:
                        board[bc[0]][bc[1]] = EMPTY
                    break
            else:
                placed_ships += 1

    return board


def show_board(board: list[list[str]]) -> None:
    for row in board:
        for item in row:
            print(f'[{item:2s}]', end='')
        print()


# TU CÓDIGO DESDE AQUÍ HACIA ABAJO
# ↓↓↓↓↓↓↓↓↓


board = generate_board()
show_board(board)
POSITION = " ABCDEFGHIJ"
num_ships = 5

visible_board = ""
column_and_row = {}
Ship_health = {}
ship_pos={}
# while Estaria aqui
for row in range(1, 11):
    for column in range(1, 11):
        if board[row - 1][column - 1] != EMPTY:
            ship_id = board[row - 1][column - 1]
            if ship_id not in ship_pos:
                ship_pos[row] = set()
            ship_pos[row].add(column)
while num_ships > 0:
    location = input('Ataque una casilla <letra><número>: ').upper()
    if location[0] in POSITION:
        row = int(location[1:])
        if row in column_and_row:
            column_and_row[row].append(POSITION.find(location[0]))
        else:
            column_and_row[row] = [POSITION.find(location[0])]
    else:
        print("Letra inválida. Por favor, introduzca una letra válida (de la A a la J).")
        continue
    print('     A B C D E F G H I J')
    for row in range(1, 11):
        visible_board = ""
        for column in range(1, 11):
            if row in column_and_row.keys() and column in column_and_row.get(row):
                if board[row - 1][column - 1] != EMPTY:
                    if column not in ship_pos[row]:
                        visible_board += SUNKEN
                    else:
                        visible_board += TOUCHED
                        print(ship_pos[row] , )
                else:
                    visible_board += WATER
            else:
                visible_board += UNEXPLORED
        print(f'{row: ^3} {visible_board}')
    