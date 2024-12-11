import os
import time
import random
class Game:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.suits = {}
        self.vis = {}
        self.match_round = 0

    def full_val(self):
        self.suits = {ch: random.randint(0, 10) for ch in self.alphabet}

    def show_oct(self, a, b, c, d):
        os.system("cls" if os.name == "nt" else "clear")

        for pair in self.suits.items():
            color_code = random.randint(31, 37)
            print(f"\033[{color_code}m  [{pair[0]}]  \033[0m", end=" ")

        print(f"\nScore of {a} : {b} ", end="")
        print(f"Score of {c} : {d}")

    def show_val(self, ch, name):
        print(f"{name} has revealed [{ch}] with a value of {self.suits[ch]}")

    def check_if_already_chosen(self, ch):
        return self.vis.get(ch, False)

    def set_color(self, color_code):
        print(f"\033[{color_code}m", end="")

    def reset_color(self):
        print("\033[0m", end="")

    def menu(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.set_color(36)

        print("  W   W  EEEEE  L      CCCC   OOO   M   M  EEEEE\n"
              "  W   W  E      L     C      O   O  MM MM  E    \n"
              "  W W W  EEEE   L     C      O   O  M M M  EEEE \n"
              "  W W W  E      L     C      O   O  M   M  E    \n"
              "   W W   EEEEE  LLLLL  CCCC   OOO   M   M  EEEEE\n")
        self.reset_color()

        print("\n\t1)  Player Vs. AI"
              "\n\t2)  Multiplayer"
              "\n\t0)  EXIT"
              "\n\nSelect a game mode: ")

    def check_winner(self, name, score, other_name, other_score):
        if score > other_score:
            print(f"\nCONGRATULATIONS {name} you have won!")
        elif score < other_score:
            print(f"\nCONGRATULATIONS {other_name} you have won!")
        else:
            print("It's a draw!")


class playerVSai(Game):
    def __init__(self):
        super().__init__()

    def play(self):
        self.full_val()
        player_name = input("\nWhat's your name? ")
        ai_name = "AI"
        player_score = 0
        ai_score = 0
        self.vis.clear()

        while self.match_round < 26:
            self.show_oct(player_name, player_score, ai_name, ai_score)
            print(f"\n\n{player_name} it's your turn...")

            ch = input("Please enter the letter of your choice: ").upper()
            while ch not in self.alphabet:
                ch = input("Enter a valid move: ").upper()

            if self.check_if_already_chosen(ch):
                print("This character was already chosen.")
                print(f"Your score is decreased by {self.suits[ch]}")
                player_score -= self.suits[ch]
                player_score = max(0, player_score)
            else:
                self.vis[ch] = True
                player_score += self.suits[ch]

            self.show_val(ch, player_name)
            print(f"{player_name} your score is: {player_score}")
            self.match_round += 1
            time.sleep(1.2);

            self.show_oct(player_name, player_score, ai_name, ai_score)
            print("\n\nIt's the AI's turn...")

            ch = random.choice(self.alphabet)
            while self.check_if_already_chosen(ch):
                ch = random.choice(self.alphabet)

            self.vis[ch] = True
            ai_score += self.suits[ch]
            self.show_val(ch, ai_name)
            print(f"AI your score is: {ai_score}")
            self.match_round += 1
            time.sleep(1.2);

        self.show_oct(player_name, player_score, ai_name, ai_score)
        print("\nFinal Score: "
              f"\n{player_name}: {player_score}"
              f"\nAI: {ai_score}")

        self.check_winner(player_name, player_score, ai_name, ai_score)


class Multiplayer(Game):
    def __init__(self):
        super().__init__()

    def play(self):
        self.full_val()
        player1_name = input("\nName of Player 1: ")
        player2_name = input("\nName of Player 2: ")
        player1_score = 0
        player2_score = 0
        self.vis.clear()

        while self.match_round < 26:
            os.system("cls" if os.name == "nt" else "clear")
            self.show_oct(player1_name, player1_score, player2_name, player2_score)
            print(f"\n\n{player1_name} it's your turn...")

            ch = input("Please enter the letter of your choice: ").upper()
            while ch not in self.alphabet:
                ch = input("Enter a valid move: ").upper()

            if ch in self.vis:
                print("This character was already chosen.")
                player1_score -= self.suits[ch]
                player1_score = max(0, player1_score)
            else:
                self.vis[ch] = True
                player1_score += self.suits[ch]

            self.show_val(ch, player1_name)
            print(f"{player1_name} your score is: {player1_score}")
            self.match_round += 1
            time.sleep(1.2);

            self.show_oct(player1_name, player1_score, player2_name, player2_score)
            print(f"\n\n{player2_name} it's your turn...")

            ch = input("Please enter the letter of your choice: ").upper()
            while ch not in self.alphabet:
                ch = input("Enter a valid move: ").upper()

            if ch in self.vis:
                print("This character was already chosen.")
                player2_score -= self.suits[ch]
                player2_score = max(0, player2_score)
            else:
                self.vis[ch] = True
                player2_score += self.suits[ch]

            self.show_val(ch, player2_name)
            print(f"{player2_name} your score is: {player2_score}")
            self.match_round += 1
            time.sleep(1.2);

        self.show_oct(player1_name, player1_score, player2_name, player2_score)
        print("\nFinal Score: "
              f"\n{player1_name}: {player1_score}"
              f"\n{player2_name}: {player2_score}")

        self.check_winner(player1_name, player1_score, player2_name, player2_score)


while True:
    game = Game()
    game.menu()
    opt = input()
    if opt == "1":
        print("\n\n[  P L A Y E R    V S.   C P U  ]")
        game_mode = playerVSai()
        game_mode.play()
    elif opt == "2":
        print("\n\n[  M U L T I P L A Y E R  ]")
        game_mode = Multiplayer()
        game_mode.play()
    elif opt == "0":
        break
    else:
        print("Invalid input")
        time.sleep(1)