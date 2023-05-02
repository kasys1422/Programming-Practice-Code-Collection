###課題#########
'''
課題A.Playerの左右移動と移動の制限
    Playerクラスの「update」メソッドを作成してください。
    updateはキーボードの左右入力をうけつけてplayerを左右に移動させます。
    playerはPlAYER_SPEEDの速度で移動し、画面内（0<x<640）の変域だけ
    移動可能にしてください。

    ＜ヒント＞
    ・ソースコード内にあるpressed_keysが関係します。
    ・pygame.K_LEFT, pygame.K_RIGHTを使用します。


課題B.フルーツのランダム生成
    任意の確率で、画面上部（x,0）のどこかに3種類からランダムに選ばれたフルーツを
    fruits配列にいれる処理をかいてください。
    また、randomモジュールを利用してください。

    ＜ヒント＞
    ・フルーツインスタンスを作成します。
    ・イニシャライザには座標、画像のパス、落下速度、スコアが必要です。
    ・落下速度、スコアは定義済みです。


課題C.フルーツの状態更新後の衝突判定（フルーツのキャッチ）と画面外のフルーツの除去
    fruits配列にあるすべてのフルーツの状態を更新し、その後、衝突判定
    を行ってください。衝突の際にはスコア加算とフルーツの削除をしてくだ
    さい。さらに、フルーツが画面外にある時も削除をしてください。

    ＜ヒント＞
    ・updateメソッドを使用します。
    ・pygameのrectで衝突判定ができるメソッドがあります。
'''
###############




#モジュールをimport
import pygame
import random
import time

###パラメータ###

#移動・落下速度
PLAYER_SPEED=5
APPLE_SPEED=8
BANANA_SPEED=4
ORANGE_SPEED=6

#フルーツのスコア
APPLE_SCORE=30
BANANA_SCORE=10
ORANGE_SCORE=20

#目標スコア
TARGET_SCORE=200


### プレイヤークラス　###
class Player:

    def __init__(self):
        self.image = pygame.image.load("FruitCatch_pictures/player.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 450)

    ##課題A## キー入力をうけて左右移動
    ####以下にコードを書いてください
    """
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-1*PLAYER_SPEED, 0)
            if self.rect.left<0:
                self.rect.left=0
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)
            if self.rect.right>640:
                self.rect.right=640

    """
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            new_x = self.rect.x - PLAYER_SPEED
            if new_x < 0:
                new_x = 0
            self.rect.x = new_x
        if pressed_keys[pygame.K_RIGHT]:
            new_x = self.rect.x + PLAYER_SPEED
            if new_x + self.rect.width > 640:
                new_x = 640 - self.rect.width
            self.rect.x = new_x
    ####   
        
    #プレイヤーを描画
    def draw(self, screen):
        screen.blit(self.image, self.rect)


### フルーツクラス　###
class Fruit:

    def __init__(self, x, y, img, speed, score):
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (64,64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.score = score

    # フルーツの落下
    def update(self):
        self.rect.move_ip(0, self.speed)
    
    # フルーツを描画
    def draw(self, screen):
        screen.blit(self.image, self.rect)


### ゲームシステムクラス　###
class GameSystem:

    #ゲームの基本設定
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Fruit Catch")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 50)
        self.total_score = 0
        self.game_state = "title"

    # タイトル画面の描画
    def draw_title(self):
        self.screen.fill((0,0,0))
        text = self.title_font.render("Fruits Catch", True, (255, 255, 255))
        self.screen.blit(text, (160, 200))
        text = self.font.render("Press ENTER to Start!", True, (255, 255, 255))
        self.screen.blit(text, (180, 270))
        pygame.display.flip()

    # ゲームプレイ画面の描画
    def draw_gameplay(self, player, fruits):
        self.screen.fill((0,0,0))

        #プレイヤーの描画
        player.draw(self.screen)

        #フルーツの描画
        for fruit in fruits:
            fruit.draw(self.screen)

        # スコアの表示
        text = self.score_font.render("Score: " + str(self.total_score), True, (255,255,255))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    # ゲームクリア画面
    def draw_gameclear(self):
        self.screen.fill((0,0,0))
        text = self.title_font.render("Game Clear!", True, (255, 255, 255))
        self.screen.blit(text, (160, 200))
        text = self.font.render("Clear Time: {:.2f} seconds".format(self.clear_time), True, (255, 255, 255))
        self.screen.blit(text, (165, 270))  # クリアタイムを表示
        text = self.font.render("Press ENTER to restart!", True, (255, 255, 255))
        self.screen.blit(text, (180, 300))
        pygame.display.flip()
        
    # ゲームループ
    def game_loop(self):
        player = Player()
        fruits=[]
        start_time=None

        while True:

            #イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                # タイトルorクリア画面時にエンターキーでゲームスタート
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_state == "title" or self.game_state == "gameclear":
                            self.game_state = "gameplay"
                            self.total_score = 0
                            fruits=[]

            pressed_keys = pygame.key.get_pressed()

            ##ゲームの状態によって画面遷移##

            #タイトル画面
            if self.game_state == "title":
                self.draw_title()

            #ゲーム画面
            elif self.game_state == "gameplay":

                # ゲームの開始時に開始時間を記録
                if start_time is None:  
                    start_time = time.time()

                #プレイヤーの状態を更新
                player.update(pressed_keys)

                ##課題B## フルーツのランダム生成
                ####以下にコードを書いてください。

                if random.randint(1, 50) == 1:
                    x = random.randint(0, 600)
                    fruit_type = random.randint(1, 3)
                    if fruit_type == 1:
                        fruits.append(Fruit(x, 0, "FruitCatch_pictures/banana.png", BANANA_SPEED, BANANA_SCORE))
                    elif fruit_type == 2:
                        fruits.append(Fruit(x, 0, "FruitCatch_pictures/orange.png", ORANGE_SPEED, ORANGE_SCORE))
                    elif fruit_type == 3:
                        fruits.append(Fruit(x, 0, "FruitCatch_pictures/apple.png", APPLE_SPEED, APPLE_SCORE))
                ####

                ##課題C## フルーツの状態更新後の衝突判定と画面外のフルーツの除去
                ####以下にコードを書いてください。

                for fruit in fruits[:]:
                    fruit.update()
                    if player.rect.colliderect(fruit.rect):
                        self.total_score += fruit.score
                        fruits.remove(fruit)

                    if fruit.rect.top > 480:
                        fruits.remove(fruit)
                ####

                # ゲームクリア判定
                if self.total_score >= TARGET_SCORE:
                    #クリアタイムを計算
                    self.clear_time = time.time() - start_time  
                    self.game_state = "gameclear"


                #ゲームプレイ画面の描画
                self.draw_gameplay(player, fruits)


            #ゲームクリア画面
            elif self.game_state == "gameclear":
                self.draw_gameclear()

            self.clock.tick(60)

#ゲームの実行
if __name__ == "__main__":
    game = GameSystem()
    game.game_loop()

