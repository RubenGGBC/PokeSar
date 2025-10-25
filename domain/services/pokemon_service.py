from contextlib import nullcontext
from enum import nonmember

from infrastrucuture.save_helper import  *

def get_pokemon_party(sav_path:str)  -> list[Pokemon]:
    sav = load_save(sav_path)
    mons = iter_party(sav)
    return mons


def get_pokemon_boxes(sav_path:str) -> list[Pokemon]:
    sav = load_save(sav_path)
    mons = iter_boxes(sav)
    return mons

def clone_pokemon(orig_sav,dst_sav, box_pos,path):
    orig = load_save(orig_sav)
    dst = load_save(dst_sav)
    slot_count = orig.BoxSlotCount
    pkm = copy_pkm_from_box(orig,box_pos)
    empty_slot = first_empty_box_slot(dst)
    box, slot = transform_idc(empty_slot,slot_count)
    paste_pokemon_to_box(dst, pkm, box, slot)
    write_sav(dst,path)

def remove_pokemon(orgin,box_pos,path):
    orig = load_save(orgin)
    slot_count=orig.BoxSlotCount
    box, slot = transform_idc(box_pos, slot_count)
    empty_pkm = orig.BlankPKM
    paste_pokemon_to_box(orig, empty_pkm, box, slot)
    write_sav(orig, path)


def get_random_MT(sav_path:str, write_path:str):
    sav = load_save(sav_path)
    inventory = sav.Inventory
    pouch = get_MT_pouch(inventory)
    owned = [i.Index for i in pouch.Items if i.Index != 0]
    all_mt = get_all_MT(sav,pouch)
    mt_aleatoria = dar_mt_aleatoria(owned,all_mt)
    pouch.GiveItem(sav,mt_aleatoria,1)
    print(owned)
    sav.Inventory = inventory
    write_sav(sav,write_path)
    return mt_aleatoria

def get_random_MT_for_50000(sav_path:str, write_path:str):
    sav = load_save(sav_path)
    left_money = withdraw_money(sav,50000, write_path)
    if left_money < 0:
        return None
    print("Money left: ", left_money)
    return get_random_MT(sav_path,write_path)