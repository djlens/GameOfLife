import numpy as np
import pygame
import time
import argparse

parser = argparse.ArgumentParser(description="Game of Life rules")
parser.add_argument("rules", metavar="rules", type=str, help="set rules for the game")
args = parser.parse_args()

rules = [list(_) for _ in args.rules.split('/')]


# cells colors
COLOR_BG = (0, 0, 0)
COLOR_GRID = (50, 50, 50)
COLOR_ALIVE = (255, 255, 255)

# game parameters

KEEP_ALIVE = [int(_) for _ in rules[0]]
BRING_TO_LIFE = [int(_) for _ in rules[1]]

SIZE = 10

def draw(window, cells, size, apply_rules=False):
    updated_cells = np.zeros(cells.shape)

    for row, col in np.ndindex(cells.shape):
        neigbors_count = np.sum(cells[row - 1: row + 2, col - 1: col + 2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if neigbors_count not in KEEP_ALIVE:
                if apply_rules:
                    color = COLOR_BG
            else:
                updated_cells[row, col] = 1
                if apply_rules:
                    color = COLOR_ALIVE

        else:
            if neigbors_count in BRING_TO_LIFE:
                updated_cells[row, col] = 1
                if apply_rules:
                    color = COLOR_ALIVE

        pygame.draw.rect(window, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    cells = np.zeros((60, 80))
    window.fill(COLOR_GRID)
    draw(window, cells, SIZE)

    pygame.display.flip()
    pygame.display.update()

    is_on = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_on = not is_on
                    draw(window, cells, SIZE)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                coordinates = pygame.mouse.get_pos()
                cells[coordinates[1] // SIZE, coordinates[0] // SIZE] = 1
                draw(window, cells, SIZE)
                pygame.display.update()

        window.fill(COLOR_GRID)

        if is_on:
            cells = draw(window, cells, SIZE, apply_rules=True)
            pygame.display.update()

        time.sleep(0.01)


if __name__ == '__main__':
    main()
