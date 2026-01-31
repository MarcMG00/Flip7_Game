from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __str__(self):
        pass