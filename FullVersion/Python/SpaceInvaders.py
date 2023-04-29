# coding: utf-8
# インベーダー風ゲームサンプル

# 初期化など ###################################
import pygame
import sys
import random

# 初期設定
pygame.init()  # PyGame初期化
window_width, window_height = 800, 600  # ウインドウサイズを指定
screen = pygame.display.set_mode((window_width, window_height))  # ウインドウサイズを設定
pygame.display.set_caption("Space Invaders")  # ウィンドウタイトルを設定

# 色の定義  色 = (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定数（速度など）
ALIEN_NUMBER = 15
ALIEN_DEFAULT_SPEED = 3
PLAYER_DEFAULT_SPEED = 5
BULLET_DEFAULT_SPEED = 10

# 画面状態
START = 0
PLAYING = 1
GAME_OVER = 2
screen_state = START    # 現在の状態

# クラス ########################################
'''
 オブジェクトクラス
 プレイヤーやエイリアン、弾などの共通処理部分をまとめたクラス

  - 使い方（継承を利用する場合）
  class SomeObject(Object):
    # コンストラクタ
    def __init__(self):
        super().__init__(x, y, w, h, c)

    x : x座標
    y : y座標
    w : 幅
    h : 高さ
    c : 色
'''
class Object:
    # 作成時に一度だけ実行
    def __init__(self, x, y, width, height, color):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.active = True
    
    # 描画関数
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
    
    # オブジェクトを非アクティブ化するフラグを立てる関数
    def kill(self):
        self.rect.x = -1000
        self.active = False
'''
 オブジェクトリストクラス
 複数のオブジェクトをまとめて管理するクラス
'''
class ObjectList:
    # 作成時に一度だけ実行
    def __init__(self):
        self.object_list = []

    # フレームごとに実行
    def update(self):
        # それぞれの要素の情報を更新
        for i in range(len(self.object_list)):
            self.object_list[i].update()
        # 必要ない要素を削除
        del_number = 1
        for j in range(len(self.object_list)):
            if self.object_list[j-del_number].active == False:
                self.object_list.pop(j-del_number)
                del_number += 1

    # オブジェクトの描画を行う関数
    def draw(self, screen):
        # それぞれの要素の情報を更新
        for i in range(len(self.object_list)):
            self.object_list[i].draw(screen)
    
    # オブジェクトリスト（自分自身）と特定のオブジェクトの当たり判定を検出する関数
    def check_hit_object(self, target_object:Object, kill_object = True):
        result = False
        for i in range(len(self.object_list)):
            if self.object_list[i].rect.colliderect(target_object):
                if kill_object == True:
                    self.object_list[i].kill()
                result = True
        return result
'''
 弾クラス
 オブジェクトクラスを継承した弾のクラス
'''
class Bullet(Object):
    # 作成時に一度だけ実行
    def __init__(self, x, y):
        super().__init__(x, y, 5, 10, WHITE)

    # フレームごとに実行
    def update(self):
        self.rect.y -= BULLET_DEFAULT_SPEED
        if self.rect.y < 0:
            self.kill()
'''
 プレイヤークラス
 オブジェクトクラスを継承したプレイヤーのクラス
'''
class Player(Object):
    # 作成時に一度だけ実行
    def __init__(self):
        super().__init__(window_width // 2, window_height - 40, 40, 20, GREEN)
        # 弾を管理するオブジェクトリスト型インスタンスを用意
        self.bullet_group = ObjectList()

    # フレームごとに実行
    def update(self, events):
        # キー入力（移動）
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_DEFAULT_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_DEFAULT_SPEED
        # 画面外移動制限
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > window_width - 40:
            self.rect.x = window_width - 40
        # キーイベントによる入力（弾の発射）
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 弾を発射する
                    bullet = Bullet(player.rect.centerx - 2, player.rect.y)
                    self.bullet_group.object_list.append(bullet)

        # 自分が発射した弾の状態も更新
        self.bullet_group.update()

    # 描画関数
    def draw(self, screen):
        self.bullet_group.draw(screen)
        return super().draw(screen)
'''
 エイリアンクラス
 オブジェクトクラスを継承したエイリアンのクラス
'''
class Alien(Object):
    # 作成時に一度だけ実行
    def __init__(self, x = -1, speed = 3):
        if x == -1:
            x = random.randint(0, window_width - 40)
        y = 40
        super().__init__(x, y, 40, 20, RED)
        self.speed = speed

    # フレームごとに実行
    def update(self):
        self.rect.x += self.speed
        # 壁での跳ね返りと1列進む処理
        if self.rect.x < 0 or self.rect.x > window_width - 40:
            self.speed = -self.speed
            self.rect.y += 40

# 関数 ##########################################

# テキスト描画関数
def draw_text(surface, text, x, y, size=36, color=WHITE):
    font = pygame.font.Font(None, size)
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# 状態リセット関数
def reset_and_get_state():
    player = Player()
    alien_group = ObjectList()
    for i in range(ALIEN_NUMBER):
        alien_group.object_list.append(Alien(i * 50 + 20))
    return player, alien_group

# オブジェクトなどの作成 ########################

# オブジェクトの作成
player, alien_group = reset_and_get_state()
# スコアのリセット
score = 0

# メインループ ##################################
while True:
    # イベント処理
    events = pygame.event.get()
    for event in events:
        # 終了処理
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # キー入力（画面遷移用）
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_state == START:
                player, alien_group = reset_and_get_state()
                score = 0
                screen_state = PLAYING
            elif screen_state == GAME_OVER:
                screen_state = START

    # メニュー画面
    if screen_state == START:
        screen.fill(BLACK)
        draw_text(screen, "Space Invaders", window_width // 2 - 100, window_height // 2 - 30)
        draw_text(screen, "Click to start", window_width // 2 - 84, window_height // 2 + 30)
    
    # プレイ画面
    elif screen_state == PLAYING:
        # オブジェクトの更新
        player.update(events)
        alien_group.update()

        # 当たり判定(エイリアン)
        hit_number = 0
        for bullet in player.bullet_group.object_list:
            if alien_group.check_hit_object(bullet):
                bullet.kill()
                alien = Alien(-hit_number * 60 + 20, ALIEN_DEFAULT_SPEED + int(score / 100))
                alien_group.object_list.append(alien)
                hit_number += 1
                score += 10

        # 当たり判定(プレイヤー)
        if alien_group.check_hit_object(player):
            screen_state = GAME_OVER

        # 画面の描画
        screen.fill(BLACK)                            # 背景の描画
        player.draw(screen)                           # プレイヤーの描画
        alien_group.draw(screen)                      # エイリアンの描画
        draw_text(screen, f"Score: {score}", 10, 10)  # スコア表示

    # ゲームオーバー画面
    elif screen_state == GAME_OVER:
        screen.fill(BLACK)
        draw_text(screen, "Game Over", window_width // 2 - 80, window_height // 2 - 60)
        draw_text(screen, f"Score: {score}", window_width // 2 - 80, window_height // 2 - 30)  # スコア表示

    # 画面更新
    pygame.display.flip()

    # フレームレート設定
    pygame.time.Clock().tick(60)