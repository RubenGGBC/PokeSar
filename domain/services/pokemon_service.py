
from infrastrucuture.save_helper import  *



def get_pokemon_party(sav_path:str)  -> list[Pokemon]:
    sav = load_save(sav_path)
    mons = iter_party(sav)
    return mons

def get_pokemon_boxes(sav_path:str) -> list[Pokemon]:
    sav = load_save(sav_path)
    mons = iter_boxes(sav)
    return mons