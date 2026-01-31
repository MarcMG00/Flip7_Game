from game.deck import Deck
from game.player import Player
from utils.input_helpers import choose_from_list
from cards.number_card import NumberCard
from cards.special_card import SpecialCard

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        self.deck = Deck()

    def play_round(self):
        for p in self.players:
            p.reset_round()

        while not all(p.stopped for p in self.players):
            for player in self.players:
                if player.stopped:
                    continue

                print(f"\nTurno de {player.name}")
                print(f"Números: {list(player.numbers.keys())}")
                print(f"Puntos ronda: {player.calculate_round_points()}")

                action = input("¿Robar (r) o Plantarse (p)? ").lower()
                if action == "p":
                    player.stopped = True
                    continue

                card = self.deck.draw()
                print(f"{player.name} roba {card}")

                if isinstance(card, NumberCard):
                    if player.has_number(card.value):
                        if player.second_life:
                            print("Segunda vida usada, carta descartada.")
                            player.second_life = False
                            self.deck.discard_card(card)
                        else:
                            print("Número repetido → pierdes la ronda.")
                            player.round_lost = True
                            player.stopped = True
                    else:
                        player.add_card(card)
                        if player.numeric_count() == 7:
                            print("¡¡VOLTEAR 7!! +15 puntos")
                            player.voltear7 = True
                            return
                elif isinstance(card, SpecialCard):
                    if card.name == "Stop":
                        target = choose_from_list(
                            "¿A quién paras?",
                            [p for p in self.players if not p.stopped]
                        )
                        target.stopped = True
                    else:
                        player.add_card(card)
                else:
                    player.add_card(card)

    def score_round(self):
        for p in self.players:
            if not p.round_lost:
                points = p.calculate_round_points()
                if p.voltear7:
                    points += 15
                p.total_score += points

    def play(self):
        while max(p.total_score for p in self.players) < 200:
            self.play_round()
            self.score_round()

        winner = max(self.players, key=lambda p: p.total_score)
        print(f"\n🏆 Ganador: {winner.name} con {winner.total_score} puntos")