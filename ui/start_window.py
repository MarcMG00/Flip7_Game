import tkinter as tk
from game.player import Player
from game.game import Game
from ui.main_window import MainWindow

class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip 7 - Inicio")
        self.root.geometry("400x400")

        self.players_entries = []

        tk.Label(root, text="Número de jugadores (mín 3)").pack(pady=5)

        self.num_players_var = tk.IntVar(value=3)
        self.num_spin = tk.Spinbox(
            root,
            from_=3,
            to=6,
            textvariable=self.num_players_var,
            command=self.update_player_fields,
            width=5
        )
        self.num_spin.pack()

        self.players_frame = tk.Frame(root)
        self.players_frame.pack(pady=10)

        self.update_player_fields()

        tk.Button(
            root,
            text="Empezar partida",
            command=self.start_game,
            bg="green",
            fg="white"
        ).pack(pady=15)

    def update_player_fields(self):
        for w in self.players_frame.winfo_children():
            w.destroy()

        self.players_entries.clear()

        for i in range(self.num_players_var.get()):
            frame = tk.Frame(self.players_frame)
            frame.pack(pady=2)

            tk.Label(frame, text=f"Jugador {i+1}:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            entry.insert(0, f"Jugador{i+1}")

            self.players_entries.append(entry)

    def start_game(self):
        players = []

        for entry in self.players_entries:
            name = entry.get().strip()
            if not name:
                name = "Jugador"
            players.append(Player(name))

        self.root.destroy()  # cerramos pantalla inicio

        game = Game(players)
        ui = MainWindow(game)
        ui.run()