
# ver_dinero.py
# Script mínimo que usa la carga aislada + lectura del save

import os
from domain.services.pokemon_service import *

# === Ajusta estas rutas a TU entorno ===
PKHEX_DLL_DIR = "./libs/pkhexcore/PKHeX.Core.24.5.5/lib/net8.0"
SAVES_DIR     = "./saves"
SAVE_FILENAME = "main2"   # cambia si tu archivo se llama diferente
SAVE_DST = "main"

def main():
    # 1) cargar PKHeX.Core (lógica separada en pkhex_loader)


    # 2) cargar el save y leer dinero (lógica en save_tools)
    save_path = os.path.join(SAVES_DIR, SAVE_FILENAME)
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"No encuentro el save en: {save_path}")

    party = get_pokemon_party(save_path)
    print("PARTY:")
    for pkm in party:
        print(pkm.to_dict())
    print("Dinero:")
    print(get_money(load_save(save_path)))
    save_det = os.path.join(SAVES_DIR, SAVE_DST)

    print("BOX:")
    boxes = get_pokemon_boxes(save_path)
    for pkm in boxes:
        print(pkm.to_dict())

    print("Clonando el primer Pokémon de la caja al save destino...")
    clone_pokemon(save_path, save_det, 0,os.path.join(SAVES_DIR, "cloned_"+SAVE_DST))

if __name__ == "__main__":
    main()
