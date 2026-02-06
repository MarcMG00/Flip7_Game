from collections import Counter
from cards.number_card import NumberCard
from cards.bonus_card import BonusCard
from cards.special_card import SpecialCard

class Player:
    def __init__(self, name: str):
        self.name = name
        self.total_score = 0
        self.reset_round()

    # Reset player's vars each new round
    def reset_round(self):
        self.numbers = Counter()
        self.bonuses: list[BonusCard] = []
        self.specials: dict[str, SpecialCard] = {}
        self.stopped = False
        self.round_lost = False
        self.second_life = False
        self.flip7 = False
        self.is_receiving_three_cards_row = False

    # Add Card on player's list
    def add_card(self, card):
        if isinstance(card, NumberCard):
            self.numbers[card.value] += 1
        elif isinstance(card, BonusCard):
            self.bonuses.append(card)
        elif isinstance(card, SpecialCard):
            self.specials[card.name] = card
            if card.name == "SegundaVida":
                self.second_life = True

    # Check if got a duplicated number (for number Cards)
    def has_number(self, value: int) -> bool:
        return self.numbers[value] > 0

    # Count number of Cards (checked for "Flip7") (for number Cards)
    def numeric_count(self) -> int:
        return len(self.numbers)
    
    # Get all of special Cards (if got any special card (normally only "THREE_CARDS_ROW"))
    def get_special_cards(self, special_type):
        if special_type in self.specials:
            print("El jugador tiene al menos una carta TresSeguidas")
            return [self.specials[special_type]]
        return []

    # Calculate score for current round
    def calculate_round_points(self) -> int:
        # Sum of normal numbers
        numbers_sum = sum(self.numbers.keys())

        # Apply mutliplier x2
        multiplier = 1
        double_multiplier = next((item for item in self.bonuses if item.name == "x2"), None)
        if double_multiplier is not None:
            multiplier *= 2

        total_after_multiplier = numbers_sum * multiplier

        # Sum of bonuses +N
        bonus_points = sum(bonus.value for bonus in self.bonuses if bonus.name != "x2")

        return total_after_multiplier + bonus_points
    
    # Cehck if player has pending special Cards to use (normally after recieving 3 in a row)
    def pending_specials(self):
        return [c for c in self.cards if isinstance(c, SpecialCard)]

    def __str__(self):
        return f"{self.name} (Total: {self.total_score})"