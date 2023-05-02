# ブラックジャックゲームサンプル（Colaboratory用）
import random
import time

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

class Card:
    suits = ["♠", "♥", "♦", "♣"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value}{self.suit}"

    def get_value(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        elif self.value == "A":
            return 11
        else:
            return int(self.value)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.draw())

    def show_hand(self, hidden=False):
        print(f"{self.name}の手札: ", end="")
        for i, card in enumerate(self.hand):
            if i == 0 and hidden:
                print("??", end=" ")
            else:
                print(card, end=" ")
        print()

    def calculate_score(self):
        score = 0
        aces = 0
        for card in self.hand:
            value = card.get_value()
            if value == 11:
                aces += 1
            score += value

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

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

    while True:
        action = input("ヒットしますか？ スタンドしますか？ (h/s): ").lower()
        if action == 'h':
            player.draw(deck)
            player.show_hand()
            if player.calculate_score() > 21:
                print("バスト！ ディーラーの勝ちです。")
                return
        elif action == 's':
            break
        else:
            print("無効な入力です。h または s を入力してください。")

    dealer.show_hand()

    while dealer.calculate_score() < 17:
        time.sleep(0.5)
        dealer.draw(deck)
        dealer.show_hand()

    player_score = player.calculate_score()
    dealer_score = dealer.calculate_score()

    if dealer_score > 21:
        print("ディーラーがバスト！ プレイヤーの勝ちです。")
    elif player_score > dealer_score:
        print("プレイヤーの勝ち！")
    elif player_score < dealer_score:
        print("ディーラーの勝ち！")
    else:
        print("引き分け！")

if __name__ == '__main__':
    play_blackjack()