from dataclasses import dataclass

from domain.models.pokemon import Pokemon

@dataclass()
class Pokemon_in_Box:
    pokemon: Pokemon
    box_slot: int

    def __init__(self, pokemon: Pokemon, slot: int):
        self.pokemon = pokemon
        self.box_slot = slot

    def to_dict(self) -> dict:
        return {
            "box_slot": self.box_slot,
            "pokemon": self.pokemon.to_dict()
        }