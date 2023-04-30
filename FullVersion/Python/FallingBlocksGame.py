# coding: utf-8
# テトリス風ゲームサンプル

import sys
import pygame
import random
from pygame.locals import *

# ゲームのパラメータ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
GAME_AREA_WIDTH = GRID_WIDTH * GRID_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * GRID_SIZE
GAME_AREA_LEFT = (WINDOW_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_TOP = (WINDOW_HEIGHT - GAME_AREA_HEIGHT) // 2

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# ブロックの形状
SHAPES = [
    [['.....',
      '.....',
      '..O..',
      '.OOO.',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....'],
     ['.....',
      '.OO..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.O...',
      '.OO..',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....'],
     ['.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '.OO..',
      '.O...',
      '.O...',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '.OO..',
      '.....']],
    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '...O.',
      '..OO.',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '..O..',
      '.....'],
     ['.....',
      '..OO.',
      '.OO..',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OOOO',
      '.....',
      '.....'],
     ['..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOOO',
      '.....',
      '.....'],
     ['..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....']]
]

# ブロッククラス
class Block:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_current_rotation(self):
        return self.shape[self.rotation]

# ゲーム管理クラス
class FallingBlocksGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Falling Blocks Game')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_tetromino = self.new_block()

    def draw_text_with_outline(self, text, font, color, outline_color, x, y, outline_thickness=1):
        text_surface = font.render(text, True, outline_color)
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                text_rect = text_surface.get_rect(center=(x + dx, y + dy))
                self.screen.blit(text_surface, text_rect)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def new_block(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return Block(GRID_WIDTH // 2 - 2, -2, shape, color)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x] or GRAY
                pygame.draw.rect(self.screen, color,
                                (GAME_AREA_LEFT + x * GRID_SIZE, GAME_AREA_TOP + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                pygame.draw.rect(self.screen, BLACK,
                                (GAME_AREA_LEFT + x * GRID_SIZE, GAME_AREA_TOP + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_tetromino(self, tetromino):
        shape = tetromino.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    pygame.draw.rect(self.screen, tetromino.color,
                                     (GAME_AREA_LEFT + (tetromino.x + x) * GRID_SIZE,
                                      GAME_AREA_TOP + (tetromino.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def draw_game_area(self):
        pygame.draw.rect(self.screen, WHITE, (GAME_AREA_LEFT, GAME_AREA_TOP, GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 1)
        self.draw_grid()
        self.draw_tetromino(self.current_tetromino)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (30, 30))

    def draw_start_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render('Falling Blocks Game', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render('Press ENTER to start', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 * 2))
        self.screen.blit(text, text_rect)

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        self.draw_text_with_outline('Game Over', font, RED, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)

        font = pygame.font.Font(None, 36)
        self.draw_text_with_outline(f'Final Score: {self.score}', font, WHITE, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        font = pygame.font.Font(None, 36)
        self.draw_text_with_outline('Press ENTER to restart', font, WHITE, BLACK, WINDOW_WIDTH // 2, 3 * WINDOW_HEIGHT // 4)

    def collision_check(self, tetromino, dx=0, dy=0, dr=0):
        shape = tetromino.shape[(tetromino.rotation + dr) % len(tetromino.shape)]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    try:
                        if tetromino.x + x + dx < 0 or tetromino.x + x + dx >= GRID_WIDTH or \
                                tetromino.y + y + dy < 0 or tetromino.y + y + dy >= GRID_HEIGHT or \
                                self.grid[tetromino.y + y + dy][tetromino.x + x + dx]:
                            return True
                    except IndexError:
                        return True
        return False

    def lock_tetromino(self):
        shape = self.current_tetromino.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    self.grid[self.current_tetromino.y + y][self.current_tetromino.x + x] = self.current_tetromino.color
        self.score += 10
        self.current_tetromino = self.new_block()

        if self.collision_check(self.current_tetromino, dy=0):
            self.game_over = True

        # Check for full lines
        full_lines = [y for y, row in enumerate(self.grid) if all(cell for cell in row)]
        if full_lines:
            for y in full_lines:
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.score += 100 * len(full_lines)

    def game_loop(self):
        start_screen = True
        while start_screen:
            self.screen.fill(BLACK)
            self.draw_start_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    start_screen = False

        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_game_area()
            self.draw_score()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT and not self.collision_check(self.current_tetromino, dx=-1):
                        self.current_tetromino.x -= 1
                    elif event.key == K_RIGHT and not self.collision_check(self.current_tetromino, dx=1):
                        self.current_tetromino.x += 1
                    elif event.key == K_DOWN and not self.collision_check(self.current_tetromino, dy=1):
                        self.current_tetromino.y += 1
                    elif event.key == K_UP:
                        self.current_tetromino.rotate()
                        if self.collision_check(self.current_tetromino, dr=1):
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()

            if not self.collision_check(self.current_tetromino, dy=1):
                self.current_tetromino.y += 1
            else:
                self.lock_tetromino()
                if self.collision_check(self.current_tetromino, dy=0):
                    self.game_over = True

            self.clock.tick(5)

        while True:
            self.screen.fill(BLACK)
            self.draw_game_area()
            self.draw_score()
            self.draw_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    self.reset_game()
                    self.game_loop()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_tetromino = self.new_block()

if __name__ == '__main__':
    falling_blocks_game = FallingBlocksGame()
    falling_blocks_game.game_loop()