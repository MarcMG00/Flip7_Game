from cards.card import Card

class NumberCard(Card):
    def __init__(self, value: int):
        super().__init__(f"{value}")
        self.value = value

    def __str__(self):
        return f"Número {self.value}"