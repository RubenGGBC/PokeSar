# ver_dinero.py
# Script mínimo que usa la carga aislada + lectura del save

import os
from PKHeX_loader import load_pkhex_core
from save_tools import load_save_from_path, get_money, get_game_label

# === Ajusta estas rutas a TU entorno ===
PKHEX_DLL_DIR = "/home/andoni/Escritorio/SAR/libs/pkhexcore/PKHeX.Core.24.5.5/lib/net8.0"
SAVES_DIR     = "/home/andoni/Escritorio/SAR/saves"
SAVE_FILENAME = "main"   # cambia si tu archivo se llama diferente

def main():
    # 1) cargar PKHeX.Core (lógica separada en pkhex_loader)
    load_pkhex_core(PKHEX_DLL_DIR)

    # 2) cargar el save y leer dinero (lógica en save_tools)
    save_path = os.path.join(SAVES_DIR, SAVE_FILENAME)
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"No encuentro el save en: {save_path}")

    sav = load_save_from_path(save_path)
    game = get_game_label(sav)
    money = get_money(sav)

    print("== SAVE CARGADO ==")
    print("Tipo .NET:", sav.GetType().FullName)
    if game:
        print("Juego:", game)
    print(f"Dinero: {money:,}")

if __name__ == "__main__":
    main()