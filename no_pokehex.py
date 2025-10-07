import struct
import socket
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# Offsets basados en la documentación de ProjectPokemon
SAVE_FILE_SIZE = 0x100000  # 1MB
SAVE_1_OFFSET = 0x02000
SAVE_2_OFFSET = 0x81000

# Offsets específicos (relativos al inicio del save file)
PARTY_OFFSET = 0x14200  # Aproximado - necesitas verificar el offset exacto del Block ID
BOX_OFFSET = 0x04C00    # Aproximado - offset de las cajas
POKEMON_SIZE = 0xE8     # 232 bytes por Pokémon (formato EK6)
PARTY_SIZE = 6
BOX_COUNT = 31
BOX_SLOTS = 30

@dataclass
class PokemonData:
    """Estructura básica de datos de un Pokémon"""
    id: int
    nickname: str
    level: int
    gender: int
    is_shiny: bool
    is_egg: bool
    encrypted_data: bytes
    box_number: Optional[int] = None
    slot_number: Optional[int] = None

class SaveData:
    def __init__(self, savepath: str):
        self.savepath = savepath
        self.save_data = None
        self.active_save_offset = SAVE_1_OFFSET
    def cargarsave(self):
        with open(self.save_path, 'rb') as f:
            self.save_data = f.read()
        if self.save_data != SAVE_FILE_SIZE:
            print("El archivo esta corrupto")
    def encontrarParty(self):
        with open(self.save_path,'rb') as f:
            self.save_data = f.read()
            offsetparty=self.active_save_offset + PARTY_OFFSET
            indexequip=0
            indexmax=6





