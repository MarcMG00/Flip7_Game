import tkinter as tk
from cards.special_card import SpecialCard
from ui.player_view import PlayerView
from functools import partial

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

    # Draw action
    def on_draw(self):
        # Check if there are forced actions (normally only if a player is receiving 3 Cards in a row)
        forced = self.game.process_forced_actions()
        if forced:
            player = self.game.current_player
            # If forced but has done flip7, it ends instantly
            if player.numeric_count() == 7:
                self.finish_round()
                return
            
            print(f"[DEBUG] There are forced actions to do")

            if forced.get("three_row_finished"):
                pending = player.pending_specials()

                if pending:
                    # If having special Card after recieving 3 Cards => forced to use it
                    self.ask_target(pending[0])
                    return

            self.refresh()
            return
        
        # Draw card to next player
        result = self.game.draw_card()
        card = result["card"]
        print(f"[DEBUG] Card returned : {card.name}")

        if "round_lost" in result["extra_actions"]:
            print("repeated Card number")
            self.game.current_player.stopped = True

        if result["needs_target"]:
            self.ask_target(card)
            return

        # Round over if all players are stopped
        if result["flip7"] or result["round_over"] or all(p.stopped or p.round_lost for p in self.game.players):
            self.finish_round()
            return

        self.game.next_player()
        self.refresh()

    # Stop action
    def on_stop(self):
        self.game.current_player.stopped = True

        if all(p.stopped or p.round_lost for p in self.game.players):
            self.finish_round()

        self.game.next_player()
        self.refresh()    

    # Refresh view
    def refresh(self):
        for view in self.player_views:
            view.refresh()

    # Ask a target to give the special Card
    def ask_target(self, special_type):
        available_players = [p for p in self.game.players if not p.stopped]

        if special_type.name == "SegundaVida" and len(available_players) == 1:
            target = available_players[0]

            if "SegundaVida" in target.specials:
                print(f"[AUTO] Segunda vida descartada (no se puede aplicar a nadie más)")
                self.game.deck.discard_card(special_type)
                return
        
        # Apply Card to only player remaining on the round
        elif (special_type.name == "TresSeguidas" or special_type.name == "Stop") and len(available_players) == 1:
            target = available_players[0]
            print(f"[AUTO] TresSeguidas aplicado a {target.name}")
            self.on_target_selected(special_type, target, popup=None)
            return

        popup = tk.Toplevel(self.root)
        popup.title(f"Elegir objetivo ({special_type})")

        for p in available_players:
            if not p.stopped:
                tk.Button(
                    popup,
                    text=p.name,
                    command=partial(self.on_target_selected, special_type, p, popup)
                ).pack()

    # Apply special Card to target selected
    def on_target_selected(self, special_type, target, popup):
        print(f"[DEBUG] {special_type} aplicado a {target.name}")
        if special_type.name == "Stop":
            target.specials["Stop"] = SpecialCard("Stop")
            target.stopped = True

        elif special_type.name == "SegundaVida":
            target.specials["SegundaVida"] = SpecialCard("SegundaVida")
            target.second_life = True

        elif special_type.name == "TresSeguidas":
            target.specials["TresSeguidas"] = SpecialCard("TresSeguidas")
            self.game.start_three_in_row(target)

        if popup:
            popup.destroy()
        self.game.next_player()
        self.refresh()

    # Calulate the score of the round
    def score_round(self):
        for p in self.game.players:
            if not p.round_lost:
                points = p.calculate_round_points()
                if p.flip7:
                    points += 15
                p.total_score += points

    # Actions when finishing round (reset vars + calculate scores)
    def finish_round(self):
        print(f"[DEBUG] all players are stopped / or Flip7")
        self.game.round_over = True
        self.score_round()

        for view in self.player_views:
            view.refresh_total_score()

        winner = self.game.check_game_over()
        if winner:
            self.show_winner(winner)
            return
    
        self.game.discard_players_cards()
        self.game.reset_round()
        self.game.start_round()
        self.refresh()

    # Show winner
    def show_winner(self, winner):
        popup = tk.Toplevel(self.root)
        popup.title("🏆 Fin del juego")
        popup.geometry("300x200")

        tk.Label(
            popup,
            text=f"🏆 GANADOR 🏆\n\n{winner.name}\n\n{winner.total_score} puntos",
            font=("Arial", 14, "bold"),
            fg="green",
            justify="center"
        ).pack(pady=20)

        tk.Button(
            popup,
            text="🔄 Reiniciar juego",
            command=lambda: self.restart_game(popup)
        ).pack(pady=10)

        tk.Button(
            popup,
            text="❌ Salir",
            command=self.root.destroy
        ).pack()

    # Reset the game
    def restart_game(self, popup):
        popup.destroy()

        # Reset players
        for p in self.game.players:
            p.total_score = 0
            p.reset_round()

        # Reset game
        self.game.deck.reset()
        self.game.current_player_index = 0
        self.game.round_over = False

        self.refresh()

        for view in self.player_views:
            view.refresh_total_score()

    def run(self):
        self.root.mainloop()