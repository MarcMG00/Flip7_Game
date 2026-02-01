from cards.card import Card

class BonusCard(Card):
    def __init__(self, name: str, value: int | None = None):
        super().__init__(name)
        self.value = value  # None to get x2

    def __str__(self):
        return f"Bonus {self.name}"