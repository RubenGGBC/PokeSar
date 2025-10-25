# save_tools.py
# Responsabilidad: lógica para trabajar con saves usando PKHeX.Core
# Requiere que pkhex_loader.load_pkhex_core() se haya llamado antes.

from domain.services.pokemon_tools import pokemon_pid
from infrastrucuture.PKHeX_loader import load_pkhex_core
load_pkhex_core("libs/pkhexcore/PKHeX.Core.24.5.5/lib/net8.0")
import PKHeX.Core as core
from PKHeX.Core import SaveUtil,SlotEditor, SlotTouchType, SlotTouchResult
from System import Array, Byte,Int32
from domain.models.pokemon import Pokemon
from domain.models.pokemon_in_box import  Pokemon_in_Box
import random

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

def get_game_strings():
    return core.GameInfo.GetStrings(5)
def get_money(sav):
    """
    Obtiene el dinero desde un objeto 'sav'.
    Devuelve int (dinero)
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

def iter_boxes(sav):
    game_strings = core.GameInfo.GetStrings(5)
    mons = sav.BoxData
    box_count = sav.BoxCount
    box = []
    box_slot_count = sav.BoxSlotCount
    total_box_slots = box_slot_count * box_count
    for i in range(total_box_slots):
        pkm = Pokemon(mons[i],game_strings)
        if pokemon_pid(pkm) == 0:
            continue
        pkm_in_box = Pokemon_in_Box(pkm, i)
        box.append(pkm_in_box)
    return box

def transform_idc(box_idx,slot_count):
    box = box_idx // slot_count
    slot = box_idx % slot_count
    return box, slot

def copy_pkm_from_box(orig,box_pos):
    pkm = orig.BoxData[box_pos]
    return pkm.Clone()

def first_empty_box_slot(sav):
    mons = sav.BoxData
    box_count = sav.BoxCount
    box_slot_count = sav.BoxSlotCount
    total_box_slots = box_slot_count * box_count
    for i in range(total_box_slots):
        if mons[i].Species == 0 or mons[i].PID == 0:
            return i
    return None


def paste_pokemon_to_box(dst, pkm, box, slot):
    dst.SetBoxSlotAtIndex(pkm, Int32(box), Int32(slot))

def get_MT_pouch(inventory):
    return inventory[2]


def get_all_MT(sav,pouch):
    max_id = sav.MaxItemID
    all_mt = []
    print(max_id)

    for i in range(max_id):
        print(f"{i}+{pouch.CanContain(i)}")
        if pouch.CanContain(i):
            all_mt.append(i)
    return all_mt

def dar_mt_aleatoria(owned,all_mt):
    candidatos = sorted(set(all_mt) - set(owned))
    tm_id = random.choice(candidatos)
    return tm_id

def write_sav(sav,path):
    raw = sav.Write()
    with open(path, "wb") as f:
        f.write(bytearray(raw))


