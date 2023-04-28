# インベーダーサンプル
# made by GPT-4

##############################################
# 課題                                       #
# 1. プレイヤー死亡判定の追加                #
# 2. 得点処理の追加                          #
# 3. 敵オブジェクトを生成する仕組みの追加    #
##############################################

# 初期化など ###################################
import pygame
import sys
import random

# 初期設定
pygame.init()  # PyGame初期化
width, height = 800, 600  # ウインドウサイズを指定
screen = pygame.display.set_mode((width, height))  # ウインドウサイズを設定
pygame.display.set_caption("Space Invaders")  # ウィンドウタイトルを設定

# 色の定義  色 = (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# クラス ########################################
# プレイヤークラス (pygameのスプライトクラスをオーバーライド)
class Player(pygame.sprite.Sprite):
    # 作成時に一度だけ実行
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = width // 2
        self.rect.y = height - 40
    # フレームごとに実行
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > width - 40:
            self.rect.x = width - 40

# エイリアンクラス (pygameのスプライトクラスをオーバーライド)
class Alien(pygame.sprite.Sprite):
    # 作成時に一度だけ実行
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - 40)
        self.rect.y = 40
        self.speed = 3
    # フレームごとに実行
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > width - 40:
            self.speed = -self.speed
            self.rect.y += 40

# 弾クラス (pygameのスプライトクラスをオーバーライド)
class Bullet(pygame.sprite.Sprite):
    # 作成時に一度だけ実行
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # フレームごとに実行
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()

# スプライトグループの作成
player_group = pygame.sprite.GroupSingle()
player = Player()
player_group.add(player)

alien_group = pygame.sprite.GroupSingle()
alien = Alien()
alien_group.add(alien)

bullet_group = pygame.sprite.Group()

# メインループ ##################################
while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # キー入力
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx - 2, player.rect.y)
                bullet_group.add(bullet)

    # スプライトの更新
    player_group.update()
    alien_group.update()
    bullet_group.update()

    # 当たり判定
    for bullet in bullet_group.sprites():
        if pygame.sprite.spritecollide(bullet, alien_group, True):
            bullet.kill()
            alien = Alien()
            alien_group.add(alien)

    # 画面の描画
    screen.fill(BLACK)
    player_group.draw(screen)
    alien_group.draw(screen)
    bullet_group.draw(screen)

    # 画面更新
    pygame.display.flip()

    # フレームレート設定
    pygame.time.Clock().tick(60)


