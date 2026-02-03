import tkinter as tk
from ui.player_view import PlayerView

class MainWindow:
    def __init__(self, game):
        self.game = game

        self.root = tk.Tk()
        self.root.title("Flip 7")
        self.root.geometry("900x600")

        self.players_frame = tk.Frame(self.root)
        self.players_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.BOTTOM, pady=10)

        self.player_views = []
        self.draw_players()
        self.draw_controls()

    def draw_players(self):
        for player in self.game.players:
            view = PlayerView(self.players_frame, player)
            view.frame.pack(side=tk.LEFT, padx=10)
            self.player_views.append(view)

    def draw_controls(self):
        tk.Button(
            self.controls_frame,
            text="Robar carta",
            command=self.on_draw
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.controls_frame,
            text="Plantarse",
            command=self.on_stop
        ).pack(side=tk.LEFT, padx=10)

    def on_draw(self):
        result = self.game.draw_card()
        card = result["card"]

        if "round_lost" in result["extra_actions"]:
            if all(p.stopped for p in self.game.players):
                result["round_over"] = True

        if result["needs_target"]:
            self.ask_target(card)

        if result["round_over"]:
            self.game.round_over = True
            self.score_round()
            self.game.reset_round()

        result = self.game.next_player()
        if result is None:
            self.game.round_over = True
            self.score_round()
            self.game.reset_round()
            self.game.next_player()

        self.refresh()

    def on_stop(self):
        self.game.current_player.stopped = True
        self.game.next_player()
        self.refresh()

    def refresh(self):
        for view in self.player_views:
            view.refresh()

    def process_forced_actions(self):
        if self.game.has_forced_action():
            self.game.continue_three_in_row()
            self.refresh()

            # Delay to draw Cards
            self.root.after(800, self.process_forced_actions)

    def ask_target(self, special_type):
        popup = tk.Toplevel(self.root)
        popup.title(f"Elegir objetivo ({special_type})")

        for p in self.game.players:
            if not p.stopped:
                tk.Button(
                    popup,
                    text=p.name,
                    command=lambda pl=p: self.on_target_selected(special_type, pl, popup)
                ).pack()

    def on_target_selected(self, special_type, target, popup):
        if special_type == "Stop":
            target.specials[special_type.name] = special_type
            target.stopped = True

        elif special_type == "SegundaVida":
            target.specials[special_type.name] = special_type
            target.second_life = True

        elif special_type == "TresSeguidas":
            self.game.start_three_in_row(target)

        popup.destroy()
        self.refresh()

    def check_pending_specials(self, player):
        three = player.get_special_cards("TresSeguidas")
        if three:
            return True
        return False

    def has_forced_action(self):
        return (
            self.pending_three_row is not None
            or len(self.forced_actions) > 0
        )
    
    def pop_forced_action(self):
        if not self.forced_actions:
            return None
        return self.forced_actions.popleft()

    def process_game_flow(self):
        # 1 TresSeguidas en curso (robos automáticos)
        if self.game.pending_three_row:
            self.game.continue_three_in_row()
            self.refresh()
            self.root.after(700, self.process_game_flow)
            return

        # 2 Acciones forzadas pendientes (especiales)
        forced = self.game.pop_forced_action()
        if forced:
            if forced["type"] == "TresSeguidas":
                owner = forced["owner"]
                self.ask_target("TresSeguidas", owner)
            return

        # 3 Si no hay nada pendiente → juego normal
        self.on_draw()

    # Calulate the score of the round
    def score_round(self):
        for p in self.game.players:
            if not p.round_lost:
                points = p.calculate_round_points()
                if p.flip7:
                    points += 15
                p.total_score += points

    def run(self):
        self.root.mainloop()