import time
from random import randint
from turtle import position
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
pygame_font = pygame.font.SysFont("Arial", 14)
field = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Mine Sweeper")

pygame.display.flip()


def draw_board(
    win,
    row,
    col,
):

    pygame.draw.rect(
        win,
        TILE_COLOR,
        (i * TILE_SIZE + BOARD_EDGE, j * TILE_SIZE + BOARD_EDGE, TILE_SIZE, TILE_SIZE),
        0,
    )
    pygame.draw.rect(
        win,
        BORDER_COLOR,
        (i * TILE_SIZE + BOARD_EDGE, j * TILE_SIZE + BOARD_EDGE, TILE_SIZE, TILE_SIZE),
        1,
    )


def get_neighbours(field, row, col, is_bomb):
    if is_bomb:
        if row == 0 and col == 0:
            if field[row][col + 1] != -1:
                field[row][col + 1] += 1
            if field[row + 1][col] != -1:
                field[row + 1][col] += 1
            if field[row + 1][col + 1] != -1:
                field[row + 1][col + 1] += 1
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
        print(x, y)
        pygame.draw.circle(
            win,
            BOMB_COLOR,
            (y * TILE_SIZE + TILE_SIZE / 2, x * TILE_SIZE + TILE_SIZE / 2),
            TILE_SIZE * (1 / 3),
            0,
        )

        pygame.display.update()


def main():

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                j = int(x // 50)
                i = int(y // 50)

                for k, v in enumerate(bomb_positions):

                    if int(v[0]) == i and int(v[1]) == j:

                        draw_bombs(WIN, bomb_positions)

    pygame.quit()


def fill_board(win, value, row, col):
    text = pygame_font.render(
        str(value),
        True,
        (0, 0, 0),
    )
    win.blit(text, (col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))


def create_field(field, bombs):
    for i, v in enumerate(bombs):
        print(int(v[0]), int(v[1]))
        filled_field = get_neighbours(field, v[0], v[1], True)

    return filled_field


def get_empty_spaces(field, row, col):
    if field[row][col] == 0:

        pass


if __name__ == "__main__":
    bomb_positions = create_bomb(WIN, BOMBS, GRID_SIZE)
    field = create_field(field, bomb_positions)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            draw_board(WIN, i, j)

    pygame.display.update()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            fill_board(WIN, field[i][j], i, j)
    pygame.display.update()
    print(field)
    print(bomb_positions)
    main()
