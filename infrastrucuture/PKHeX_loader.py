# pkhex_loader.py
# Responsabilidad: inicializar pythonnet y cargar PKHeX.Core.dll

import os
import sys

_LOADED = False

def init_pythonnet():
    """Inicializa el runtime de .NET para pythonnet (idempotente)."""
    global _LOADED
    if _LOADED:
        return
    from pythonnet import load
    load("coreclr")  # usa CoreCLR en Linux/macOS
    _LOADED = True

def load_pkhex_core(dll_dir: str):
    """
    Carga PKHeX.Core.dll desde dll_dir.
    Deja el assembly disponible para 'from PKHeX.Core import ...' en otros módulos.
    """
    init_pythonnet()
    if dll_dir and dll_dir not in sys.path:
        sys.path.append(dll_dir)

    import clr
    try:
        # intenta por nombre (si el assembly ya es resoluble)
        clr.AddReference("PKHeX.Core")
    except Exception:
        # carga directa por ruta como fallback
        dll_path = os.path.join(dll_dir, "PKHeX.Core.dll")
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"No se encontró PKHeX.Core.dll en: {dll_path}")
        clr.AddReference(dll_path)

    # Verificación: comprobar que el assembly quedó cargado
    import System
    ok = any(a.GetName().Name.lower().startswith("pkhex.core")
             for a in System.AppDomain.CurrentDomain.GetAssemblies())
    if not ok:
        raise RuntimeError("No se pudo cargar el assembly PKHeX.Core.")
