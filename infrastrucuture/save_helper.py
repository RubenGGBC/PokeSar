# save_tools.py
# Responsabilidad: lógica para trabajar con saves usando PKHeX.Core
# Requiere que pkhex_loader.load_pkhex_core() se haya llamado antes.

import re
from PokeSar.infrastrucuture.PKHeX_loader import load_pkhex_core
load_pkhex_core("/home/andoni/Escritorio/SAR/libs/pkhexcore/PKHeX.Core.24.5.5/lib/net8.0")
import PKHeX.Core as core
from PKHeX.Core import SaveUtil
from System import Array, Byte
from PokeSar.domain.services.pokemon_tools import *
from PokeSar.domain.models.pokemon import Pokemon


def load_save(save_path: str):
    """
    Carga un save de Pokémon desde ruta usando PKHeX.Core.
    Devuelve el objeto 'sav' (tipo SAV* según el juego).
    """
    with open(save_path, "rb") as f:
        data = f.read()
    b = Array[Byte](data)

    sav = SaveUtil.GetVariantSAV(b)
    if sav is None:
        raise Exception("PKHeX.Core no pudo identificar/cargar el save. ¿Dump correcto/desencriptado?")
    return sav

def try_get_money_direct(sav):
    """Intento directo: propiedad 'Money' en el objeto save o en sub-objetos comunes."""
    t = sav.GetType()

    # 1) Money directamente en el save
    p_money = t.GetProperty("Money")
    p_money.GetValue(sav, None)



def get_money(sav):
    """
    Obtiene el dinero desde un objeto 'sav'.
    Devuelve int (dinero) o lanza excepción si no es posible determinarlo.
    """
    t = sav.GetType()
    return t.GetProperty("Money").GetValue(sav, None)

def iter_party(sav):
    game_strings = core.GameInfo.GetStrings(5)
    mons = sav.PartyData
    party_count = sav.PartyCount
    party = []
    for i in range(party_count):
        pkm = Pokemon(mons[i],game_strings)
        party.append(pkm)
    return party




