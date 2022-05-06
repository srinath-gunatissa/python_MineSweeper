import time
from random import randint
from turtle import clear, position
import pygame


pygame.font.init()

TILE_SIZE = 50
GRID_SIZE = 10
BOARD_EDGE = 0
WIDTH, HEIGHT = (
    TILE_SIZE * GRID_SIZE + BOARD_EDGE * 2,
    TILE_SIZE * GRID_SIZE + BOARD_EDGE * 2,
)
BOMBS = 15
TILE_COLOR = (125, 100, 100)
BORDER_COLOR = (255, 255, 255)
BOMB_COLOR = (255, 0, 0)
FLAG_COLOR = (0, 0, 255)
FILL_COLOR = (0, 255, 0)
pygame_font = pygame.font.SysFont("Arial", 12)
field = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
visited = []


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Mine Sweeper")

pygame.display.flip()


def draw_board(win, row, col, tile_color=TILE_COLOR):

    pygame.draw.rect(
        win,
        tile_color,
        (
            row * TILE_SIZE + BOARD_EDGE,
            col * TILE_SIZE + BOARD_EDGE,
            TILE_SIZE,
            TILE_SIZE,
        ),
        0,
    )
    pygame.draw.rect(
        win,
        BORDER_COLOR,
        (
            row * TILE_SIZE + BOARD_EDGE,
            col * TILE_SIZE + BOARD_EDGE,
            TILE_SIZE,
            TILE_SIZE,
        ),
        1,
    )


def fill_neighbours(field, row, col, is_bomb):
    if is_bomb:
        if row == 0 and col == 0:
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
            if field[row + 1][col + 1] != -1:
                field[row + 1][col + 1] += 1
        if row == 0 and col == GRID_SIZE - 1:
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
            if field[row + 1][col - 1] != -1:
                field[row + 1][col - 1] += 1

        if row == 0 and GRID_SIZE - 1 > col > 0:
            if field[row + 1][col - 1] != -1:
                field[row + 1][col - 1] += 1
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row + 1][col + 1] != -1:
                field[row + 1][col + 1] += 1
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
        if GRID_SIZE - 1 > row > 0 and col == 0:
            if field[row - 1][col + 1] != -1:
                field[row - 1][col + 1] += 1
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row + 1][col + 1] != -1:
                field[row + 1][col + 1] += 1
            if field[row - 1][col] != -1:
                field[row - 1][col] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
        if GRID_SIZE - 1 > row > 0 and GRID_SIZE - 1 > col > 0:
            if field[row - 1][col - 1] != -1:
                field[row - 1][col - 1] += 1
            if field[row + 1][col - 1] != -1:
                field[row + 1][col - 1] += 1
            if field[row - 1][col + 1] != -1:
                field[row - 1][col + 1] += 1
            if field[row + 1][col + 1] != -1:
                field[row + 1][col + 1] += 1
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row - 1][col] != -1:
                field[row - 1][col] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
        if GRID_SIZE - 1 > row > 0 and col == GRID_SIZE - 1:
            if field[row - 1][col - 1] != -1:
                field[row - 1][col - 1] += 1
            if field[row + 1][col - 1] != -1:
                field[row + 1][col - 1] += 1
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row - 1][col] != -1:
                field[row - 1][col] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
        if row == GRID_SIZE - 1 and GRID_SIZE - 1 > col > 0:
            if field[row - 1][col - 1] != -1:
                field[row - 1][col - 1] += 1
            if field[row - 1][col + 1] != -1:
                field[row - 1][col + 1] += 1
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row - 1][col] != -1:
                field[row - 1][col] += 1
        if GRID_SIZE - 1 == row and GRID_SIZE - 1 == col:
            if field[row - 1][col - 1] != -1:
                field[row - 1][col - 1] += 1
            if field[row][col - 1] != -1:
                field[row][col - 1] += 1
            if field[row - 1][col] != -1:
                field[row - 1][col] += 1

    return field


bps = []
bomb_positions = []


def create_bomb(win, bomb, grid_size):
    for i in range(0, bomb):
        x, y = randint(0, grid_size - 1), randint(0, grid_size - 1)
        field[x][y] = -1
        bps.append((x, y))
        bomb_positions = list(set(i for i in bps))
    return bomb_positions


def draw_bombs(win, positions):
    for i, v in enumerate(positions):
        x, y = int(v[0]), int(v[1])

        pygame.draw.circle(
            win,
            BOMB_COLOR,
            (y * TILE_SIZE + TILE_SIZE / 2, x * TILE_SIZE + TILE_SIZE / 2),
            TILE_SIZE * (1 / 3),
            0,
        )

        pygame.display.update()


def draw_flag(win, x, y):

    pygame.draw.circle(
        win,
        FLAG_COLOR,
        (y * TILE_SIZE + TILE_SIZE / 2, x * TILE_SIZE + TILE_SIZE / 2),
        TILE_SIZE * (1 / 3),
        0,
    )

    pygame.display.update()


def fill_board(win, value, row, col):
    prect = pygame.draw.rect(
        win,
        FILL_COLOR,
        (
            col * TILE_SIZE + BOARD_EDGE,
            row * TILE_SIZE + BOARD_EDGE,
            TILE_SIZE,
            TILE_SIZE,
        ),
        0,
    )
    pygame.draw.rect(
        win,
        BORDER_COLOR,
        (
            col * TILE_SIZE + BOARD_EDGE,
            row * TILE_SIZE + BOARD_EDGE,
            TILE_SIZE,
            TILE_SIZE,
        ),
        1,
    )
    if field[row][col] != 0:
        text = pygame_font.render(
            str(value),
            True,
            (0, 0, 0),
        )
        win.blit(
            text,
            (
                col * TILE_SIZE + text.get_height() / 2,
                row * TILE_SIZE + text.get_height() / 2,
            ),
        )
    pygame.display.update()


def create_field(field, bombs):
    for i, v in enumerate(bombs):

        filled_field = fill_neighbours(field, v[0], v[1], True)

    return filled_field


def get_empty_spaces(field, row, col):
    if field[row][col] == 0:

        pass


def get_neighbour(field, row, col):
    neighbours = []
    # neighbours.append((row, col))
    if row == 0 and col == 0:
        neighbours.append((row, col + 1))
        neighbours.append((row + 1, col))
        neighbours.append((row + 1, col + 1))

    if row == 0 and col == GRID_SIZE - 1:
        neighbours.append((row, col - 1))
        neighbours.append((row + 1, col))
        neighbours.append((row + 1, col - 1))

    if row == 0 and GRID_SIZE - 1 > col > 0:
        neighbours.append((row + 1, col - 1))
        neighbours.append((row, col - 1))
        neighbours.append((row + 1, col + 1))
        neighbours.append((row, col + 1))
        neighbours.append((row + 1, col))

    if GRID_SIZE - 1 > row > 0 and col == 0:
        neighbours.append((row - 1, col + 1))
        neighbours.append((row, col + 1))
        neighbours.append((row + 1, col + 1))
        neighbours.append((row - 1, col))
        neighbours.append((row + 1, col))

    if GRID_SIZE - 1 > row > 0 and GRID_SIZE - 1 > col > 0:
        neighbours.append((row - 1, col - 1))
        neighbours.append((row + 1, col - 1))
        neighbours.append((row - 1, col + 1))
        neighbours.append((row + 1, col + 1))
        neighbours.append((row, col - 1))
        neighbours.append((row, col + 1))
        neighbours.append((row - 1, col))
        neighbours.append((row + 1, col))

    if GRID_SIZE - 1 > row > 0 and col == GRID_SIZE - 1:
        neighbours.append((row - 1, col - 1))
        neighbours.append((row + 1, col - 1))
        neighbours.append((row, col - 1))
        neighbours.append((row - 1, col))
        neighbours.append((row + 1, col))

    if row == GRID_SIZE - 1 and GRID_SIZE - 1 > col > 0:
        neighbours.append((row - 1, col - 1))
        neighbours.append((row - 1, col + 1))
        neighbours.append((row, col - 1))
        neighbours.append((row, col + 1))
        neighbours.append((row - 1, col))

    if row == GRID_SIZE - 1 and col == 0:
        neighbours.append((row - 1, col))
        neighbours.append((row, col + 1))
        neighbours.append((row - 1, col + 1))

    if row == GRID_SIZE - 1 and col == GRID_SIZE - 1:
        neighbours.append((row - 1, col - 1))
        neighbours.append((row, col - 1))
        neighbours.append((row - 1, col))

    return neighbours


vis_zeros = []
checked_naghbours = []


def open_field(field, row, col):
    if (row, col) not in checked_naghbours:
        neighbours = get_neighbour(field, row, col)
        checked_naghbours.append((row, col))

        for i, n in enumerate(neighbours):
            if field[n[0]][n[1]] != -1:
                fill_board(WIN, field[n[0]][n[1]], n[0], n[1])
                if (n[0], n[1]) not in visited:
                    visited.append((n[0], n[1]))


zeros = []


def zero_neighbours(field, row, col):

    neighbours = get_neighbour(field, row, col)
    for i, n in enumerate(neighbours):
        if (
            field[n[0]][n[1]] == 0
            and (n[0], n[1]) not in vis_zeros
            and (n[0], n[1]) not in zeros
        ):
            zeros.append((n[0], n[1]))
    if field[row][col] == 0 and (row, col) not in vis_zeros:
        vis_zeros.append((row, col))

    while len(zeros) > 0:
        value = zeros.pop(0)

        zero_neighbours(field, value[0], value[1])
    return vis_zeros


def left_click(x, y):

    j = int(x // TILE_SIZE)
    i = int(y // TILE_SIZE)
    if (i, j) not in visited:
        fill_board(WIN, field[i][j], i, j)
        visited.append((i, j))
    if field[i][j] == 0:

        zeros = zero_neighbours(field, i, j)
        for i, v in enumerate(zeros):
            open_field(field, v[0], v[1])

    elif field[i][j] > 0:
        fill_board(WIN, field[i][j], i, j)

    for k, v in enumerate(bomb_positions):

        if int(v[0]) == i and int(v[1]) == j:

            draw_bombs(WIN, bomb_positions)


def write_click(x, y):
    j = int(x // TILE_SIZE)
    i = int(y // TILE_SIZE)
    draw_flag(WIN, i, j)


def main():

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    left_click(x, y)
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    write_click(x, y)
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                # hilight_squre(x, y)
    pygame.quit()


def hilight_squre(x, y):
    j = int(x // TILE_SIZE)
    i = int(y // TILE_SIZE)
    draw_flag(WIN, i, j)
    nbrs = get_neighbour(field, i, j)
    for i, v in enumerate(nbrs):
        pygame.draw.rect(
            WIN,
            (125, 100, 125),
            (
                j * TILE_SIZE + BOARD_EDGE,
                i * TILE_SIZE + BOARD_EDGE,
                TILE_SIZE,
                TILE_SIZE,
            ),
            100,
        )


if __name__ == "__main__":
    bomb_positions = create_bomb(WIN, BOMBS, GRID_SIZE)
    field = create_field(field, bomb_positions)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_board(WIN, i, j)

    pygame.display.update()

    pygame.display.update()

    main()
