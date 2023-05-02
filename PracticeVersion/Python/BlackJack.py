#@title # ブラックジャックゲームサンプル（Colaboratory用）

#@markdown ## 課題

#@markdown  1. デッキクラスの初期化処理を完成させる<br>
#@markdown   A すべての組み合わせのカードをデッキに追加  
#@markdown    [ヒント]
#@markdown    - 2重forループを使ってすべての組み合わせを作りましょう
#@markdown    - 最初の方にSUITSリストとVALUESリストがあるので参照しましょう
#@markdown    - 各スート(♠, ♥, ♦, ♣)と値の組み合わせに対してCardオブジェクトを作成し、デッキに追加しましょう
     
#@markdown  2. Playerクラスのcalculate_score()メソッドを完成させる<br>
#@markdown   A ブラックジャックのスコア計算を行う
#@markdown    [ヒント]
#@markdown    - カードクラスのget_value()メソッドでカード単体のスコアを取得できます
#@markdown    - ブラックジャックのスコア計算方法は以下の通りです
#@markdown      1. スコアとエースのカウントをそれぞれ0に初期化します。
#@markdown      2. 手札内の各カードに対して、カードの値を整数に変換し、それをスコアに加算します。J、Q、Kは10として扱い、エースは11として扱います。エースのカードを見つけた場合、エースのカウントも増やします。
#@markdown      3. 合計スコアが21を超えている場合、エースが1枚以上あるか確認します。エースがある場合、スコアから10を引いてエースを1として扱い、エースのカウントを1減らします。この処理を繰り返し、スコアが21以下になるかエースがなくなるまで実行します。
     
#@markdown  3. ゲーム終了前のスコア判定処理を完成させる<br>
#@markdown   A それぞれのスコアを計算して勝敗の判定
#@markdown    [ヒント]
#@markdown    - player_scoreとdealer_scoreを計算するために、Playerクラスのcalculate_score()メソッドを呼び出しましょう。
#@markdown    - ディーラーのスコアが21を超えているか確認し、バスト（スコアが21を超える）した場合はプレイヤーの勝ちと表示しましょう。
#@markdown    - プレイヤーのスコアがディーラーのスコアより高い場合はプレイヤーの勝ち、低い場合はディーラーの勝ち、同じ場合は引き分けと表示しましょう。


import random
import time

# ルール表示関数
def print_rules():
    print("""
ブラックジャックのルール:
1. プレイヤーとディーラーはそれぞれ2枚のカードを受け取ります。
2. プレイヤーは自分の手札を見て、ヒット（追加のカードを引く）かスタンド（現在の手札で勝負する）を選択できます。
3. プレイヤーがバスト（手札の合計が21を超える）すると、ディーラーの勝ちです。
4. プレイヤーがスタンドを選択したら、ディーラーは手札の合計が17以上になるまでカードを引き続けます。
5. ディーラーがバストすると、プレイヤーの勝ちです。
6. 両者がバストしない場合、手札の合計が21に近い方が勝ちです。同じ場合は引き分けとなります。
""")
    
# 定数
SUITS = ["♠", "♥", "♦", "♣"]
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# カードクラス
class Card:
    # 作成時に一度だけ実行
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    # オブジェクトの文字列表現を定義(特殊メソッド)
    def __str__(self):
        return f"{self.value}{self.suit}"

    # カードの値を取得するメソッド
    def get_value(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        elif self.value == "A":
            return 11
        else:
            return int(self.value)

# デッキクラス
class Deck:
    # 作成時に一度だけ実行
    def __init__(self):
        self.cards = []

        # 課題1A　すべての組み合わせのカードをデッキに追加
        # ここに処理を記述


        # カードをシャッフル
        random.shuffle(self.cards)

    # デッキからカードが引かれる処理
    def draw(self):
        return self.cards.pop()

# プレイヤークラス
class Player:
    # 作成時に一度だけ実行
    def __init__(self, name):
        self.name = name
        self.hand = []

    # カードを引くメソッド
    def draw(self, deck):
        self.hand.append(deck.draw())

    # 手札を表示するメソッド
    def show_hand(self, hidden=False):
        print(f"{self.name}の手札: ", end="")
        for i, card in enumerate(self.hand):
            if i == 0 and hidden:
                print("??", end=" ")
            else:
                print(card, end=" ")
        print()

    # スコアを計算するメソッド
    def calculate_score(self):
        score = 0
        aces = 0
        # 課題2A スコアの計算
        # ここに処理を記述

        return score

# ゲームプレイ関数
def play_blackjack():
    print("ブラックジャックへようこそ！")
    print_rules()
    deck = Deck()
    player = Player("プレイヤー")
    dealer = Player("ディーラー")

    for _ in range(2):
        player.draw(deck)
        dealer.draw(deck)

    player.show_hand()
    dealer.show_hand(hidden=True)

    # プレイヤーのターンの入力ループ
    while True:
        action = input("ヒットしますか？ スタンドしますか？ (h/s): ").lower()
        if action == 'h':
            player.draw(deck)
            player.show_hand()
            # プレーヤーの負け判定
            if player.calculate_score() > 21:
                print("バスト！ ディーラーの勝ちです。")
                return
        elif action == 's':
            break
        else:
            print("無効な入力です。h または s を入力してください。")

    dealer.show_hand()

    # ディーラーがカードを引く
    while dealer.calculate_score() < 17:
        time.sleep(0.5)
        dealer.draw(deck)
        dealer.show_hand()

    # 課題3A それぞれのスコアを計算して勝敗の判定
    # ここに処理を記述

if __name__ == '__main__':
    play_blackjack()
