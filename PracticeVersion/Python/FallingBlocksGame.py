# coding: utf-8
# テトリス風ゲームサンプル

# 課題
'''
1. ブロック生成メソッドを完成させる 229行目
 A 乱数を生成し、色と形を決定する
  [ヒント]
  ・乱数はrandom.randint(初期値, 終了値)で取得できます
  ・最初の方にCOLORSリストとSHAPESリストがあるので参照しましょう

2. lock_blockメソッドを完成させる 319行目
 A 一列揃っている行を見つけてリストに追加
  [ヒント]
  ・self.grid[i].count(特定の要素)でグリッド内の要素の数を数えられます
  ・グリッド内で、何もない場所には0が格納されています
  ・full_linesリストに揃った行のインデックスを入れましょう

 B 一列揃っている行があれば消去処理を行う
  [ヒント]
  ・forループを使って揃った行のインデックスをfull_linesリストから取り出して、そのインデックスの列を削除しましょう
  ・新しい空の列を追加してgridの一番上の列に追加ましょう
  ・スコアを加算しましょう（例:100点*消去した桁数）
 
3. コンティニュー処理の実装 396行目
 A キーを取得し、ループを抜ける
  [ヒント]
  ・コードを良く読んでゲームループの構造を把握しましょう
  ・event.type == KEYDOWN and event.key == K_RETURN の条件式でキー判定を行えます
  ・breakを使ってループを抜けましょう
  ・for-else構文とcontinue文を使って2重ループ構造を抜ける方法を検討しましょう
'''

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
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED, PURPLE]

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
    # 作成時に一度だけ実行
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    # ブロックの回転
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    # 現在の回転状態を取得
    def get_current_rotation(self):
        return self.shape[self.rotation]

# ゲーム管理クラス
class FallingBlocksGame:
    # 作成時に一度だけ実行
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Falling Blocks Game')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_block = self.new_block()

    # 縁付テキスト描画メソッド
    def draw_text_with_outline(self, text, font, color, outline_color, x, y, outline_thickness=1):
        text_surface = font.render(text, True, outline_color)
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                text_rect = text_surface.get_rect(center=(x + dx, y + dy))
                self.screen.blit(text_surface, text_rect)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    # ブロック生成メソッド
    def new_block(self):
        shape, color = None
        # 課題1A ランダムな色と形を指定しよう
        # ここに処理を記述

        return Block(GRID_WIDTH // 2 - 2, -2, shape, color)
    
    # グリッド表示メソッド
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.grid[y][x] or GRAY
                # グリッド内の色の表示
                pygame.draw.rect(self.screen, color,
                                (GAME_AREA_LEFT + x * GRID_SIZE, GAME_AREA_TOP + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                # 枠線の表示
                pygame.draw.rect(self.screen, BLACK,
                                (GAME_AREA_LEFT + x * GRID_SIZE, GAME_AREA_TOP + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                
    # ブロック表示メソッド
    def draw_block(self, block):
        shape = block.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    pygame.draw.rect(self.screen, block.color,
                                     (GAME_AREA_LEFT + (block.x + x) * GRID_SIZE,
                                      GAME_AREA_TOP + (block.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    
    # ゲーム領域全体の描画メソッド
    def draw_game_area(self):
        pygame.draw.rect(self.screen, WHITE, (GAME_AREA_LEFT, GAME_AREA_TOP, GAME_AREA_WIDTH, GAME_AREA_HEIGHT), 1)
        self.draw_grid()
        self.draw_block(self.current_block)

    # スコア表示メソッド
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (30, 30))

    # スタート画面表示メソッド
    def draw_start_screen(self):
        font = pygame.font.Font(None, 72)
        text = font.render('Falling Blocks Game', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render('Press ENTER to start', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 * 2))
        self.screen.blit(text, text_rect)

    # ゲームオーバー画面表示メソッド
    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        self.draw_text_with_outline('Game Over', font, RED, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)

        font = pygame.font.Font(None, 36)
        self.draw_text_with_outline(f'Final Score: {self.score}', font, WHITE, BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        font = pygame.font.Font(None, 36)
        self.draw_text_with_outline('Press ENTER to restart', font, WHITE, BLACK, WINDOW_WIDTH // 2, 3 * WINDOW_HEIGHT // 4)

    # ブロックの当たり判定を行うメソッド
    def collision_check(self, block, dx=0, dy=0, dr=0):
        shape = block.shape[(block.rotation + dr) % len(block.shape)]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    try:
                        if block.x + x + dx < 0 or block.x + x + dx >= GRID_WIDTH or \
                                block.y + y + dy < 0 or block.y + y + dy >= GRID_HEIGHT or \
                                self.grid[block.y + y + dy][block.x + x + dx]:
                            return True
                    except IndexError:
                        return True
        return False
    
    # ブロックの固定を行うメソッド
    def lock_block(self):
        shape = self.current_block.get_current_rotation()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == 'O':
                    self.grid[self.current_block.y + y][self.current_block.x + x] = self.current_block.color
        self.score += 10
        self.current_block = self.new_block()

        if self.collision_check(self.current_block, dy=0) and self.current_block.y >= 0:
            self.game_over = True

        # 一列揃ったことを確認して消去
        # 課題2A 一列揃っている行を見つけてリストに追加
        full_lines = []
        # ここに処理を記述

        # 課題2B 一列揃っている行があれば消去処理を行う
        if full_lines:
            # ここに処理を記述

            pass

    # ゲームループ
    def game_loop(self):
        while True:
            # スタート画面
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

            # ゲームプレイ画面
            while not self.game_over:
                # 画面に情報を表示
                self.screen.fill(BLACK)
                self.draw_game_area()
                self.draw_score()
                pygame.display.flip()
                # キーイベント取得
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_LEFT and not self.collision_check(self.current_block, dx=-1):
                            self.current_block.x -= 1
                        elif event.key == K_RIGHT and not self.collision_check(self.current_block, dx=1):
                            self.current_block.x += 1
                        elif event.key == K_DOWN and not self.collision_check(self.current_block, dy=1):
                            self.current_block.y += 1
                        elif event.key == K_UP:
                            self.current_block.rotate()
                            if self.collision_check(self.current_block, dr=1):
                                self.current_block.rotate()
                                self.current_block.rotate()
                                self.current_block.rotate()

                if not self.collision_check(self.current_block, dy=1):
                    self.current_block.y += 1
                else:
                    self.lock_block()
                    if self.collision_check(self.current_block, dy=0):
                        self.game_over = True
                # フレームレートを5に指定
                self.clock.tick(5)

            # ゲームオーバー画面
            while True:
                # 画面に情報を表示
                self.screen.fill(BLACK)
                self.draw_game_area()
                self.draw_score()
                self.draw_game_over()
                pygame.display.flip()
                # キーイベント取得
                for event in pygame.event.get():
                    # ゲーム終了処理
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    # 課題3A コンティニュー処理 
                    # ここに処理を記述

    # ゲームの状態をリセットするメソッド
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_block = self.new_block()

# メイン
if __name__ == '__main__':
    falling_blocks_game = FallingBlocksGame()   # ゲーム管理クラスのインスタンスを作成
    falling_blocks_game.game_loop()             # ゲームループを実行