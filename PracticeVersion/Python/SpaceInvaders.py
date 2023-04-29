# coding: utf-8
# インベーダー風ゲームサンプル(練習版)

# 課題 #########################################
'''
1. Playerクラスを完成させる
 A キー入力による移動を実装する
  [ヒント]
  以下のコードで特定のキーを押した状態を取得できます
   keys = pygame.key.get_pressed()
   if keys[pygame.K_LEFT]:
       処理
   if keys[pygame.K_RIGHT]:
       処理

 B プレイヤーが画面外に移動できないように制限する
 [ヒント]
 ・プレイヤーのx座標が画面の左端または右端に達したかどうかを判断し、達した場合はプレイヤーの移動を制限します。

 C スペースキーのキーイベントで弾を発射できるようにする
 [ヒント]
 ・pygame.KEYDOWNイベントを使って、スペースキーが押されたときに弾を発射する処理を実装します。

 D 弾クラスを利用した弾の発射を実装する
 [ヒント]
 ・Alienの生成部分を参考にしてみてください
 ・弾の発射は、プレイヤーの位置から始まります。プレイヤーのx座標とy座標を参照して、弾の初期位置を設定しましょう。
 ・弾のインスタンスを作成したら、弾のリストに追加しましょう。これにより、画面上に複数の弾が同時に存在できるようになります。

2. Alienクラスを完成させる
 A エイリアンが壁に衝突すると進行方向を反転させ、1列下方向に進行するコードを書く
 [ヒント]
 ・エイリアンが壁に衝突したかどうかを判定するには、エイリアンのx座標と画面の幅を比較してください。エイリアンが壁に衝突した場合、進行方向を反転させる必要があります。
 ・進行方向を反転させるには、エイリアンの速度の符号を反転させましょう。例えば、速度が正の場合は負に、速度が負の場合は正に変更してください。
 ・エイリアンが壁に衝突した際に1列下に移動するには、y座標を更新してください。一定量の値を加算することで、下方向に移動させることができます。

3. 当たり判定の実装
 A 弾とエイリアンの当たり判定を実装
 [ヒント]
 ・衝突が発生した場合、エイリアンと弾を削除し、プレイヤーのスコアを加算してください。
'''
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
        # キー入力（移動）課題1A
        
        # 画面外移動制限 課題1B
        
        # キーイベントによる入力（弾の発射）課題1C, 課題1D
        

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
        # 壁での跳ね返りと1列進む処理 課題2A
        

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
    # プレイヤー生成
    player = Player()
    # エイリアン生成
    alien_group = ObjectList() # 複数のエイリアンを管理するオブジェクトリスト型クラスを使用
    # 複数のエイリアンを生成
    for i in range(ALIEN_NUMBER):
        alien = Alien(i * 50 + 20)            # 新しいエイリアンを定義
        alien_group.object_list.append(alien) # オブジェクトリスト型のインスタンスに複数のエイリアンを格納
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
        # キー入力（ゲーム終了用）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # マウス入力（画面遷移用）
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_state == START:
                # オブジェクトの作成
                player, alien_group = reset_and_get_state()
                # スコアのリセット
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

        # 当たり判定(エイリアン) 課題3A


        # 当たり判定(プレイヤー)
        if alien_group.check_hit_object(player):
            player.kill()
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