
from PokeSar.infrastrucuture.save_helper import  *



def get_pokemon_party(sav_path:str):
    sav = load_save(sav_path)
    mons = iter_party(sav)
    return mons