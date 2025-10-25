
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

def print_inventario(save_path:str):
    sav=load_save(save_path)
    print_inventario_helper(sav)


