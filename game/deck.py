import random
from cards.number_card import NumberCard
from cards.bonus_card import BonusCard
from cards.special_card import SpecialCard

class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []
        self._build()
        self.shuffle()

    # Initial deck
    def _build(self):
        # Numbers
        self.cards.append(NumberCard(0))
        for i in range(1, 13):
            for _ in range(i):
                self.cards.append(NumberCard(i))

        # Bonuses
        self.cards += [
            BonusCard("x2"),
            BonusCard("+2", 2),
            BonusCard("+4", 4),
            BonusCard("+6", 6),
            BonusCard("+8", 8),
            BonusCard("+10", 10),
        ]

        # Specials
        for _ in range(3):
            self.cards.append(SpecialCard("Stop"))
            self.cards.append(SpecialCard("SegundaVida"))
            self.cards.append(SpecialCard("TresSeguidas"))

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Get the Card from above of the deck
    def draw(self):
        # If no more Cards remaining on the current deck, reinitialize it with the discarded deck
        if not self.cards:
            self.cards = self.discard[:]
            self.discard.clear()
            self.shuffle()
        return self.cards.pop()

    # Discard Card to discarded deck
    def discard_card(self, card):
        self.discard.append(card)