from collections import Counter
from cards.number_card import NumberCard
from cards.bonus_card import BonusCard
from cards.special_card import SpecialCard

class Player:
    def __init__(self, name: str):
        self.name = name
        self.total_score = 0
        self.reset_round()

    def reset_round(self):
        self.numbers = Counter()
        self.bonuses: list[BonusCard] = []
        self.specials: dict[str, SpecialCard] = {}
        self.stopped = False
        self.round_lost = False
        self.second_life = False
        self.voltear7 = False

    def add_card(self, card):
        if isinstance(card, NumberCard):
            self.numbers[card.value] += 1
        elif isinstance(card, BonusCard):
            self.bonuses.append(card)
        elif isinstance(card, SpecialCard):
            self.specials[card.name] = card
            if card.name == "SegundaVida":
                self.second_life = True

    def has_number(self, value: int) -> bool:
        return self.numbers[value] > 0

    def numeric_count(self) -> int:
        return len(self.numbers)

    def calculate_round_points(self) -> int:
        total = sum(self.numbers.keys())
        multiplier = 1
        bonus_sum = 0

        for b in self.bonuses:
            if b.name == "x2":
                multiplier *= 2
            else:
                bonus_sum += b.value

        return total * multiplier + bonus_sum

    def __str__(self):
        return f"{self.name} (Total: {self.total_score})"