from cards.card import Card

class SpecialCard(Card):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return f"Especial {self.name}"