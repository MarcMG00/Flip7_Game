import tkinter as tk

class PlayerView:
    def __init__(self, parent, player):
        self.player = player
        self.frame = tk.Frame(parent, bd=2, relief="groove")

        self.name_label = tk.Label(self.frame, text=player.name, font=("Arial", 12, "bold"))
        self.name_label.pack()

        self.cards_frame = tk.Frame(self.frame)
        self.cards_frame.pack()

        self.score_label = tk.Label(self.frame)
        self.score_label.pack()

        self.refresh()

    def refresh(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for n in self.player.numbers:
            tk.Label(self.cards_frame, text=str(n), width=3).pack(side=tk.LEFT)

        for b in self.player.bonuses:
            tk.Label(self.cards_frame, text=b.name).pack(side=tk.LEFT)

        for s in self.player.specials.values():
            tk.Label(self.cards_frame, text=s.name, fg="red").pack(side=tk.LEFT)

        self.score_label.config(text=f"Puntos ronda: {self.player.calculate_round_points()}")