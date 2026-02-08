import tkinter as tk

class PlayerView:
    def __init__(self, parent, player):
        self.player = player
        self.frame = tk.Frame(parent, bd=0, highlightthickness=3, highlightbackground="black")

        self.name_label = tk.Label(self.frame, text=player.name, font=("Arial", 12, "bold"))
        self.name_label.pack()

        self.cards_frame = tk.Frame(self.frame)
        self.cards_frame.pack()

        self.score_label = tk.Label(self.frame)
        self.score_label.pack()

        self.score_frame = tk.Frame(self.frame, bd=1, relief="sunken")
        self.score_frame.pack(fill="x", pady=(5, 0))
        self.total_score_label = tk.Label(self.score_frame, font=("Arial", 10, "bold"))
        self.total_score_label.pack()

        self.refresh()
        self.refresh_total_score()

    def refresh(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for n in self.player.number_cards:
            tk.Label(self.cards_frame, text=str(n.value), width=3).pack(side=tk.LEFT)

        for b in self.player.bonuses:
            tk.Label(self.cards_frame, text=b.name).pack(side=tk.LEFT)

        for s in self.player.specials.values():
            tk.Label(self.cards_frame, text=s.name, fg="red").pack(side=tk.LEFT)

        self.score_label.config(text=f"Puntos ronda: {self.player.calculate_round_points()}")

        if self.player.stopped:
            self.frame.config(highlightbackground="red", highlightthickness=3)
        else:
            self.frame.config(highlightbackground="black", highlightthickness=3)

        if self.player.total_score >= 200:
            self.frame.config(highlightbackground="gold", highlightthickness=4)


    def refresh_total_score(self):
        self.total_score_label.config(
            text=f"Score: {self.player.total_score}"
        )