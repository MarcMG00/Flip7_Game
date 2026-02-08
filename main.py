from game.player import Player
from game.game import Game
from ui.main_window import MainWindow

# Only can play between 2 to 4 players
def ask_number_of_players(min_players=3):
    while True:
        try:
            num = int(input("Número de jugadores: "))
            if min_players <= num:
                return num
            else:
                print(f"El número debe ser superior o gual a {min_players}.")
        except ValueError:
            print("Solo se puede jugar con un mínimo de 3 jugadores.")

def main():
    num_players = ask_number_of_players()
    players = [Player(input(f"Nombre jugador {i+1}: ")) for i in range(num_players)]
    game = Game(players)
    #game.play()

    ui = MainWindow(game)
    ui.run()

if __name__ == "__main__":
    main()