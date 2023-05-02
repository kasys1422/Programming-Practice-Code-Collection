import random

#@title ハングマンゲーム { display-mode: "form" }

class Hangman:
    def __init__(self, words_list):
        self.words_list = words_list
        self.word_to_guess = random.choice(words_list)
        self.guesses = []
        self.max_wrong_guesses = 0
        self.current_wrong_guesses = 0

    def set_difficulty(self):
        while True:
            difficulty = input("難易度を選択してください（初級, 中級, 上級）: ").lower()
            if difficulty == "初級":
                self.max_wrong_guesses = 10
                break
            elif difficulty == "中級":
                self.max_wrong_guesses = 7
                break
            elif difficulty == "上級":
                self.max_wrong_guesses = 5
                break
            else:
                print("無効な入力です。初級、中級、または上級を選択してください。")

    def display_word(self):
        display = ''
        for letter in self.word_to_guess:
            if letter in self.guesses:
                display += letter
            else:
                display += '_'
        return display

    def guess_letter(self, letter):
        if len(letter) != 1 or not letter.isalpha() or not letter.isascii():
            print("無効な入力です。英単語1文字を入力してください。")
            return

        if letter not in self.guesses:
            self.guesses.append(letter)
            if letter not in self.word_to_guess:
                self.current_wrong_guesses += 1
        else:
            print("この文字は既に予想されました。")

    def play(self):
        print("ハングマンゲームへようこそ！")
        print("このゲームでは、以下の英単語のリストからランダムに選ばれた単語を予測します。")
        print("リスト:", ', '.join(self.words_list))
        print(f"間違った予想が{self.max_wrong_guesses}回を超えると、ゲームオーバーになります。")
        print("それでは、始めましょう！\n")

        while self.current_wrong_guesses < self.max_wrong_guesses:
            print("当てるべき単語:", self.display_word())
            print("間違いの回数:", self.current_wrong_guesses, "/", self.max_wrong_guesses)
            print("予想した文字:", ', '.join(self.guesses))

            letter = input("予想する文字を入力してください（英単語1文字）: ").lower()
            self.guess_letter(letter)

            if "_" not in self.display_word():
                print("おめでとうございます！単語を当てました:", self.word_to_guess)
                break

        if self.current_wrong_guesses >= self.max_wrong_guesses:
            print("ゲームオーバー！予想の回数が上限に達しました。正解の単語は:", self.word_to_guess)

words_list = ['apple', 'banana', 'cherry', 'grapefruit', 'kiwi', 'mango', 'orange', 'papaya', 'strawberry', 'watermelon']
game = Hangman(words_list)
game.set_difficulty()
game.play()
