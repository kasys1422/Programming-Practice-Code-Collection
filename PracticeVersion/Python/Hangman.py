#@title # ハングマンゲームサンプル（Colaboratory用）

#@markdown ## 課題

#@markdown  1. set_difficultyメソッドを完成させる<br>
#@markdown   A 難易度に応じた最大間違い回数を設定する
#@markdown    [ヒント]
#@markdown    - 難易度に応じて、max_wrong_guessesの値を設定しましょう。
#@markdown    - 難易度の入力にはinput()を使いましょう

#@markdown  2. display_wordメソッドを完成させる<br>
#@markdown   A 単語の中で予想済みの文字を表示し、未予想の文字をアンダースコア(_)に置き換える
#@markdown    [ヒント]
#@markdown    - word_to_guessの各文字をループし、その文字がguessesに含まれる場合はその文字をdisplay変数に追加し、含まれない場合はアンダースコア(_)をdisplay変数に追加しましょう。

#@markdown  3. guess_letterメソッドを完成させる<br>
#@markdown   A 入力された文字が正しい形式かチェックし、予想を処理する
#@markdown    [ヒント]
#@markdown    - 入力が1文字の英字であり、マルチバイト文字ではないことを確認してください。
#@markdown    - 予想された文字がまだ予想されていないかチェックし、予想リストに追加してください。予想リストはself.guessesです。
#@markdown    - 予想された文字が正解の単語に含まれない場合、間違いの回数を増やしてください。

import random

class Hangman:
    def __init__(self, words_list):
        self.words_list = words_list  # 単語リストの設定
        self.word_to_guess = random.choice(words_list)  # ランダムに単語を選択
        self.guesses = []  # 予想済みの文字を格納するリスト
        self.max_wrong_guesses = 0  # 許容される最大間違い回数
        self.current_wrong_guesses = 0  # 現在の間違い回数

    # 難易度を設定するメソッド
    def set_difficulty(self):
        # 課題1A 難易度に応じた最大間違い回数を設定する
        # ここに処理を記述
        
        pass

    # 単語の表示を更新するメソッド
    def display_word(self):
        display = ''
        # 課題2A 単語の中で予想済みの文字を表示し、未予想の文字をアンダースコア(_)に置き換える
        # ここに処理を記述
        
        return display

    # 入力された文字が正しいかチェックし、予想を処理するメソッド
    def guess_letter(self, letter):
        # 課題3A 入力された文字が正しい形式かチェックし、予想を処理する
        # ここに処理を記述
        
        pass

    def play(self):
        print("ハングマンゲームへようこそ！")
        print("このゲームでは、以下の英単語のリストからランダムに選ばれた単語を予測します。")
        print("リスト:", ', '.join(self.words_list))
        print(f"間違った予想が{self.max_wrong_guesses}回を超えると、ゲームオーバーになります。")
        print("それでは、始めましょう！\n")

        while self.current_wrong_guesses < self.max_wrong_guesses:
            print("当てるべき単語:", self.display_word())  # 表示用の単語を更新
            print("間違いの回数:", self.current_wrong_guesses, "/", self.max_wrong_guesses)
            print("予想した文字:", ', '.join(self.guesses))  # 予想済みの文字を表示

            letter = input("予想する文字を入力してください（英単語1文字）: ").lower()
            self.guess_letter(letter)  # 入力された文字を処理

            if "_" not in self.display_word():  # 全ての文字が予想された場合
                print("おめでとうございます！単語を当てました:", self.word_to_guess)
                break

        if self.current_wrong_guesses >= self.max_wrong_guesses:  # 間違い回数が上限に達した場合
            print("ゲームオーバー！予想の回数が上限に達しました。正解の単語は:", self.word_to_guess)


words_list = ['apple', 'banana', 'cherry', 'grapefruit', 'kiwi', 'mango', 'orange', 'papaya', 'strawberry', 'watermelon']
game = Hangman(words_list)
game.set_difficulty()  # 難易度を設定
game.play()
