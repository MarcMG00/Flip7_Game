import random
from collections import Counter

# ======================
# Cards
# ======================

class Card:
    def __init__(self, name):
        self.name = name

    def apply(self, game, player):
        pass

# Number Card
class NumberCard(Card):
    def __init__(self, value):
        super().__init__(str(value))
        self.value = value

# Bonus Card
class BonusCard(Card):
    def __init__(self, bonus_type, value):
        super().__init__(f"{bonus_type}{value}")
        self.bonus_type = bonus_type  # "+" or "x"
        self.value = value

# Special Card
class SpecialCard(Card):
    def __init__(self, special_type):
        super().__init__(special_type)
        self.special_type = special_type


# ======================
# Player
# ======================

class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.reset_round()

    # Reset round
    def reset_round(self):
        self.number_cards = []
        self.bonus_cards = []
        self.special_cards = []
        self.stopped = False
        self.second_life = False
        self.alive = True
        self.is_receiving_three_cards_row = False

    # Check if number is duplicated
    def has_duplicate_number(self, value):
        return value in self.number_cards

    # Add number on current list if not duplicated
    def add_number(self, value):
        self.number_cards.append(value)

    # Add special card on special Cards list (normally only "THREE_CARDS_ROW")
    def add_special_card(self, card):
        self.special_cards.append(card)

    # Get if got any special card (normally only "THREE_CARDS_ROW")
    def get_special_cards(self, special_type):
        return [c for c in self.special_cards if c.special_type == special_type]

    # Remove special cards after the effects (normally only "THREE_CARDS_ROW")
    def remove_special_card(self, card):
        self.special_cards.remove(card)

    # Check if is a Flip7 (7 diferent Cards)
    def has_flip7(self):
        return len(set(self.number_cards)) >= 7

    # Count score for current round
    def round_score(self):
        total = sum(self.number_cards)
        multiplier = 1
        bonus_add = 0

        for b in self.bonus_cards:
            if b.bonus_type == "x":
                multiplier *= b.value
            else:
                bonus_add += b.value

        return total * multiplier + bonus_add


# ======================
# Deck
# ======================

class Deck:
    def __init__(self):
        self.main_deck = []
        self.discard = []
        self.build_deck()
        random.shuffle(self.main_deck)

    # Set values on Deck
    def build_deck(self):
        # One Card "0"
        self.main_deck.append(NumberCard(0))

        # Cards from 1 to 12
        for i in range(1, 13):
            for _ in range(i):
                self.main_deck.append(NumberCard(i))

        # Bonus values ("+")
        for v in [2, 4, 6, 8, 10]:
            self.main_deck.append(BonusCard("+", v))
        # One Card "x2"
        self.main_deck.append(BonusCard("x", 2))

        # 3 Special Cards (3 of each one)
        for _ in range(3):
            self.main_deck.append(SpecialCard("STOP"))
            self.main_deck.append(SpecialCard("SECOND_LIFE"))
            self.main_deck.append(SpecialCard("THREE_IN_ROW"))

    # Get Card from above of the Deck (if no more Cards, shuffle again Cards discarded)
    def draw(self):
        if not self.main_deck:
            self.main_deck = self.discard
            self.discard = []
            random.shuffle(self.main_deck)

        return self.main_deck.pop()


# ======================
# Game
# ======================

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.round_over = False

    # Play the game
    def play(self):
        round_number = 1
        # Game ends when at least one player has 200 points
        while max(p.total_score for p in self.players) < 200:
            print(f"\n===== RONDA {round_number} =====")
            self.play_round()
            round_number += 1

        # Get winner
        winner = max(self.players, key=lambda p: p.total_score)
        print(f"\n GANADOR: {winner.name} con {winner.total_score} puntos")

    # Play round
    def play_round(self):
        # Reset all vars when starting a round
        for p in self.players:
            p.reset_round()

        self.round_over = False
        current = 0

        while not self.round_over:
            # Get player for turn
            player = self.players[current]
            if not player.stopped and player.alive:
                self.take_turn(player)
            current = (current + 1) % len(self.players)

            if all(p.stopped or not p.alive for p in self.players):
                self.round_over = True

        for p in self.players:
            if p.alive:
                score = p.round_score()
                p.total_score += score
                print(f"{p.name} gana {score} puntos (total {p.total_score})")

    # Get an option from game
    def take_turn(self, player):
        # IA simple (it stops if 20 points cumulatedfor the current round)
        if not player.is_receiving_three_cards_row and sum(player.number_cards) >= 20:
            player.stopped = True
            print(f"{player.name} se planta")
            return

        # Get card from above of the deck
        card = self.deck.draw()
        print(f"{player.name} roba {card.name}")

        # get instance type of the Card
        if isinstance(card, NumberCard):
            self.handle_number(card, player)
        elif isinstance(card, BonusCard):
            self.handle_bonus(card, player)
        else:
            self.handle_special(card, player)

        self.deck.discard.append(card)

    # Handle number Card
    def handle_number(self, card, player):
        # If duplicated
        if player.has_duplicate_number(card.value):
            # Check if second life
            if player.second_life:
                print(f"{player.name} usa SEGUNDA VIDA")
                player.second_life = False
            else:
                print(f"{player.name} REPITE número → pierde ronda")
                player.alive = False
                player.number_cards.clear()
        # If not duplicated        
        else:
            player.add_number(card.value)
            if player.has_flip7():
                print(f"{player.name} hace FLIP 7")
                player.total_score += 15
                self.round_over = True

    # Handle bonus Card
    def handle_bonus(self, card, player):
        if card.name not in [b.name for b in player.bonus_cards]:
            player.bonus_cards.append(card)
        # Has not to enteer on this case (only one of each)
        else:
            print("Bonus repetido descartado")

    # Handle special Card
    def handle_special(self, card, player):
        # STOP
        if card.special_type == "STOP":
            # Choose some to stop
            target = self.choose_target(player)
            target.stopped = True
            print(f"{target.name} queda parado")

        # SECOND LIFE
        elif card.special_type == "SECOND_LIFE":
            if not player.second_life:
                player.second_life = True
            # If player has already a second_life, choose someone to give the Card
            else:
                target = self.choose_target(player)
                if target:
                    target.second_life = True

        # THREE IN A ROW
        elif card.special_type == "THREE_IN_ROW":
            # Case 1 : is not receiving cards, start receiving
            if not player.is_receiving_three_cards_row:
                target = self.choose_target(player)
                print(f"{target.name} recibe 3 cartas seguidas")

                target.is_receiving_three_cards_row = True

                for _ in range(3):
                    if not target.alive or self.round_over:
                        break

                    self.take_turn(target)

                target.is_receiving_three_cards_row = False

                # Check if recieving another special card THREE_ROW_CARDS
                pending_three_in_row = target.get_special_cards("THREE_IN_ROW")

                for special in pending_three_in_row:
                    print(f"{target.name} puede ahora usar su carta THREE_IN_ROW")
                    target.remove_special_card(special)

                    # Recursivty
                    new_target = self.choose_target(target)
                    print(f"{new_target.name} recibe 3 cartas seguidas")

                    new_target.is_receiving_three_cards_row = True
                    for _ in range(3):
                        if not new_target.alive or self.round_over:
                            break
                        self.take_turn(new_target)
                    new_target.is_receiving_three_cards_row = False

            # Case 2: is recieving cards => hold for after the actual effect of special Card
            else:
                print(f"{player.name} recibe THREE_IN_ROW pero debe esperar")
                player.add_special_card(card)
    
    # Get player to STOP (because of special card "Stop")
    def choose_target(self, player):
        candidates = [p for p in self.players if p != player and not p.stopped and p.alive]
        return random.choice(candidates) if candidates else player

# ======================
# MAIN
# ======================

if __name__ == "__main__":
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    game = Game(players)
    game.play()
