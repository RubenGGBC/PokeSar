# save_tools.py
# Responsabilidad: lógica para trabajar con saves usando PKHeX.Core
# Requiere que pkhex_loader.load_pkhex_core() se haya llamado antes.

import re

def load_save_from_path(save_path: str):
    """
    Carga un save de Pokémon desde ruta usando PKHeX.Core.
    Devuelve el objeto 'sav' (tipo SAV* según el juego).
    """
    from System import Array, Byte
    from PKHeX.Core import SaveUtil

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
    if p_money:
        try:
            return p_money.GetValue(sav, None)
        except:
            pass

    # 2) Money en propiedades tipo Trainer/TrainerData/Status
    for holder_name in ("Trainer", "TrainerData", "MyStatus", "Status"):
        ph = t.GetProperty(holder_name)
        if not ph:
            continue
        try:
            holder = ph.GetValue(sav, None)
            if holder is None:
                continue
            p2 = holder.GetType().GetProperty("Money")
            if p2:
                return p2.GetValue(holder, None)
        except:
            pass

    return None


def get_money(sav):
    """
    Obtiene el dinero desde un objeto 'sav'.
    Devuelve int (dinero) o lanza excepción si no es posible determinarlo.
    """
    money = try_get_money_direct(sav)
    if money is not None:
        return int(money)

    # Como último recurso, ofrece contexto para depurar
    t = sav.GetType()
    raise RuntimeError(
        "No se encontró una propiedad de dinero de forma automática. "
        f"Tipo de save: {t.FullName}. Puedes inspeccionar propiedades numéricas para identificarla."
    )

def get_game_label(sav):
    """Devuelve una etiqueta corta del juego si hay info disponible (opcional)."""
    t = sav.GetType()
    for prop_name in ("Game", "Version", "Format", "Generation"):
        p = t.GetProperty(prop_name)
        if p:
            try:
                return str(p.GetValue(sav, None))
            except:
                pass
    return None
