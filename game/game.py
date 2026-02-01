from game.deck import Deck
from game.player import Player
from utils.input_helpers import choose_from_list
from cards.number_card import NumberCard
from cards.special_card import SpecialCard
from cards.bonus_card import BonusCard

class Game:
    # def __init__(self, players: list[Player]):
    #     self.players = players
    #     self.deck = Deck()
    #     self.round_over = False

    # # Play the round
    # def play_round(self):
    #     round_number = 1
    #      # Game ends when at least one player has 200 points
    #     while max(p.total_score for p in self.players) < 200:
    #         print(f"\n===== RONDA {round_number} =====")
    #         for p in self.players:
    #             p.reset_round()

    #         self.round_over = False

    #         # Play turns until round it's not over
    #         while not self.round_over:
    #             for player in self.players:
    #                 if player.stopped:
    #                     continue

    #                 print(f"\nTurno de {player.name}")
    #                 print(f"Números: {list(player.numbers.keys())}")
    #                 print(f"Puntos ronda: {player.calculate_round_points()}")

    #                 # Do action of draw or stop
    #                 action = input("¿Robar (r) o Plantarse (p)? ").lower()
    #                 if action == "p":
    #                     player.stopped = True
    #                     if all(p.stopped for p in self.players):
    #                         self.round_over = True
    #                     continue

    #                 self.take_turn(player)
    #                 if all(p.stopped for p in self.players):
    #                     self.round_over = True

    #         # Round ends, so calculate the points for each player
    #         for p in self.players:
    #             if not p.stopped:
    #                 score = p.calculate_round_points()
    #                 if p.flip7:
    #                     score += 15
    #                 p.total_score += score
    #                 print(f"{p.name} gana {score} puntos (total {p.total_score})")

    #         round_number += 1
    #         print("Fin de la ronda")

    #     # Get winner
    #     winner = max(self.players, key=lambda p: p.total_score)
    #     print(f"\n GANADOR: {winner.name} con {winner.total_score} puntos")

    # # Get the option draw from game
    # def take_turn(self, player):
    #     # Get card from above of the deck
    #     card = self.deck.draw()
    #     print(f"{player.name} roba {card.name}")

    #     # Number Card
    #     if isinstance(card, NumberCard):
    #         if player.has_number(card.value):
    #             # Use second life if number duplicated
    #             if player.second_life:
    #                 print("Segunda vida usada, carta descartada.")
    #                 player.second_life = False
    #                 self.deck.discard_card(card)
    #             # Lose round
    #             else:
    #                 print("Número repetido → pierdes la ronda.")
    #                 player.round_lost = True
    #                 player.stopped = True
    #         # Add number not existing
    #         else:
    #             player.add_card(card)
    #             # If Flip 7 => end round
    #             if player.numeric_count() == 7:
    #                 print("¡Flip 7! +15 puntos")
    #                 player.flip7 = True
    #                 self.round_over = True
    #                 return
    #     # Special Card
    #     elif isinstance(card, SpecialCard):
    #         # STOP
    #         if card.name == "Stop":
    #             target = choose_from_list("¿A quién paras?", [p for p in self.players if not p.stopped])
    #             target.stopped = True
    #         # SECOND LIFE
    #         elif card.name == "SegundaVida":
    #             if not player.second_life:
    #                 player.second_life = True
    #             # Chose a player if already current player has a second life
    #             else:
    #                 target = choose_from_list("¿A quién le das la segunda vida ?", [p for p in self.players if not p.stopped and not p.second_life])
    #                 if target:
    #                     target.second_life = True
    #         # THREE IN A ROW
    #         else:
    #             # Check if current player is not already receiving three cards
    #             if not player.is_receiving_three_cards_row:
    #                 target = choose_from_list("¿A quién le das 3 cartas seguidas ?", [p for p in self.players if not p.stopped])
    #                 target.is_receiving_three_cards_row = True

    #                 # Start receiving 3 Cards to player choosen
    #                 for _ in range(3):
    #                     if target.stopped or self.round_over:
    #                         break

    #                     self.take_turn(target)

    #                 target.is_receiving_three_cards_row = False

    #                 # Check if recieving another special card THREE_ROW_CARDS
    #                 pending_three_in_row = target.get_special_cards("TresSeguidas")

    #                 # If player choosen got another three cards in a row, use it
    #                 for special in pending_three_in_row:
    #                     print(f"{target.name} puede ahora usar su carta TresSeguidas")
    #                     target.remove_special_card(special)

    #                     # Recursivity
    #                     new_target = choose_from_list("¿A quién le das 3 cartas seguidas ?", [p for p in self.players if not p.stopped])
    #                     print(f"{new_target.name} recibe 3 cartas seguidas")

    #                     new_target.is_receiving_three_cards_row = True
    #                     for _ in range(3):
    #                         if target.stopped or self.round_over:
    #                             break
    #                         self.take_turn(new_target)
    #                     new_target.is_receiving_three_cards_row = False
    #             # Add Cards (three in a row) => use it at the end when not receiving anymore
    #             else:
    #                 print(f"{player.name} recibe TresSeguidas pero debe esperar")
    #                 player.add_card(card)
    #     # Bonus Cards
    #     else:
    #         player.add_card(card)

    #     self.deck.discard.append(card)

    # # Calulate the score of the round
    # def score_round(self):
    #     for p in self.players:
    #         if not p.round_lost:
    #             points = p.calculate_round_points()
    #             if p.flip7:
    #                 points += 15
    #             p.total_score += points

    # # Play the game
    # def play(self):
    #     while max(p.total_score for p in self.players) < 200:
    #         self.play_round()
    #         self.score_round()

    #     # Show the winner
    #     winner = max(self.players, key=lambda p: p.total_score)
    #     print(f"\n🏆 Ganador: {winner.name} con {winner.total_score} puntos")
    def __init__(self, players):
       self.players = players
       self.deck = Deck()
       self.current_player_index = 0
       self.round_over = False

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def start_round(self):
        self.round_over = False
        for p in self.players:
            p.reset_round()

    def draw_card(self):
        player = self.current_player
        card = self.deck.draw()
        return self.apply_card(player, card)
    
    def draw_and_apply(self, player):
        card = self.deck.draw()
        return self.apply_card(player, card)

    def stop_current_player(self):
        self.current_player.stopped = True
        self.next_player()

    def apply_card(self, player, card):
        result = {
        "card": card,
        "round_over": False,
        "needs_target": False,
        "special_type": None,
        "extra_actions": [],
        }

        # NUMBER CARD
        if isinstance(card, NumberCard):
            if player.has_number(card.value):
                if player.second_life:
                    player.second_life = False
                    self.deck.discard_card(card)
                    player.specials.remove(next((item for item in self.specials if item.name == "SegundaVida")))
                else:
                    player.round_lost = True
                    player.stopped = True
                    result["extra_actions"].append("round_lost")
            else:
                player.add_card(card)
                if player.numeric_count() == 7:
                    player.flip7 = True
                    self.round_over = True
                    result["round_over"] = True

        # BONUS CARD
        elif isinstance(card, BonusCard):
            player.add_card(card)

        # SPECIAL CARD
        elif isinstance(card, SpecialCard):

            # STOP
            if card.name == "Stop":
                result["needs_target"] = True
                result["special_type"] = "Stop"
                player.add_card(card)

            # SECOND LIFE
            elif card.name == "SegundaVida":
                if not player.second_life:
                    player.second_life = True
                    player.add_card(card)
                else:
                    result["needs_target"] = True
                    result["special_type"] = "SegundaVida"
                    player.add_card(card)

            # THREE IN A ROW
            elif card.name == "TresSeguidas":
                if not player.is_receiving_three_cards_row:
                    player.add_card(card)
                    result["needs_target"] = True
                    result["extra_actions"].append("three_row_pending")
                else:
                    result["needs_target"] = True
                    result["special_type"] = "TresSeguidas"
                    player.add_card(card)

        return result
    
    def start_three_in_row(self, target):
        target.is_receiving_three_cards_row = True
        self.pending_three_row = {
            "target": target,
            "remaining": 3
        }

    def continue_three_in_row(self):
        state = self.pending_three_row
        if not state:
            return

        target = state["target"]
        self.draw_and_apply(target)

        state["remaining"] -= 1
        if state["remaining"] == 0 or target.stopped:
            target.is_receiving_three_cards_row = False
            self.pending_three_row = None