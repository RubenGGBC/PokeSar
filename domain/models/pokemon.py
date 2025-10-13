from dataclasses import dataclass
from typing import Dict, Any
from domain.services.pokemon_tools import *

@dataclass()
class Pokemon:
    PID: int
    SID: int
    species_name: str
    types: list[str]
    level: int
    nickname: str
    nature: str
    ability_name: str
    stats: Dict[str,int]
    moveset: list[str]

    def __init__(self, pkm: Any, game_Strings: Any):
        self.PID = pokemon_pid(pkm)
        self.SID = pokemon_sid(pkm)
        self.species_name = species_name(game_Strings, self.SID)
        self.types = pokemon_types(game_Strings, (pkm.PersonalInfo.Type1,pkm.PersonalInfo.Type2))
        self.level = pokemon_level(pkm)
        self.nickname = pokemon_nickname(pkm)
        self.nature = nature_name(game_Strings, int(pkm.Nature))
        self.ability_name = ability_name(game_Strings, pkm.Ability)
        self.stats = read_stats(pkm)
        self.moveset = read_moves(game_Strings, pkm)

    def to_dict(self) -> dict:
        return {
            "pid": self.PID,
            "species_id": self.SID,
            "species_name": self.species_name,
            "types": self.types,
            "level": self.level,
            "nickname": self.nickname,
            "nature": self.nature,
            "ability_name": self.ability_name,
            "stats": {
                "hp": self.stats['hp'], "atk": self.stats['atk'], "defe": self.stats['defe'],
                "spa": self.stats['spa'], "spd": self.stats['spd'], "spe": self.stats['spe']
            },
            "moveset": [ m for m in self.moveset],
        }
