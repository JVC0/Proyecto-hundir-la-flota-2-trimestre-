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
POSITION = " ABCDEFGHIJ"
num_ships = 5
shot_positions = set()
visible_board = ""
column_and_row = {}
ship_health = {}
ship_sunked = 0
Turnos = 1
num_ships_count = []
player_points = 0  
while num_ships > 0:
    location = input(
        f'Turno {Turnos}, {num_ships} barcos restantes: Ataque una casilla <letra><número>: '
    ).upper()

    if (
        len(location) == 0
        or len(location) > 3
        or location[0] not in POSITION[1:]
        or not location[1:].isnumeric()
        or int(location[1:]) not in range(1, 11)
    ):
        print('ERROR:La casilla que has seleccionado no se encuentra en el tablero')
        continue
    if location in  shot_positions:
        print("Ya has disparado en esta casilla anteriormente")
        continue
    shot_positions.add(location)
    Turnos += 1
    
    row = int(location[1:])
    if row in column_and_row:
        column_and_row[row].append(POSITION.find(location[0]))
    else:
        column_and_row[row] = [POSITION.find(location[0])]
    print('     A B C D E F G H I J')
    for row in range(1, 11):
        visible_board = EMPTY
        for column in range(1, 11):
            if row in column_and_row.keys() and column in column_and_row.get(row):
                ship_id = board[row - 1][column - 1]
                if ship_id != EMPTY:
                    if ship_id not in ship_health:
                        ship_health[ship_id] = set()
                    ship_health[ship_id].add((column, row))
                    if len(ship_health) != 0:
                        if len(ship_health[ship_id]) == int(ship_id[0]) and ship_id not in num_ships_count :
                            num_ships_count.append(ship_id)
                            num_ships -= 1
                            player_points += 4*int(ship_id[0])- 2*int(ship_id[0])
                            
                    if len(ship_health[ship_id]) == int(ship_id[0]):
                        visible_board += SUNKEN
                    else:
                        visible_board += TOUCHED
                    
                else:
                    visible_board += WATER
            else:
                visible_board += UNEXPLORED

        print(f'{row: ^3} {visible_board}')
    row = int(location[1:])
    column = POSITION.find(location[0])
    ship_id=board[row - 1][column - 1]
    if ship_id == EMPTY:
        if player_points == 0:  
            layer_points = 0
        else:
            player_points -= 1  
    else:
        player_points += 2*int(ship_id[0])
    print(f"Puntuación actual: {player_points}")
print('Has hundido todos los barcos, has ganado ')
