import os
from pathlib import Path

DEFAULT_SAV_NAME = "save.sav"
DEFAULT_LOG_NAME = "logs.log"
SAV_PATH = Path("./saves_server")
LOG_PATH = Path("./logs")
class Evento:
    SubirFichero,DescargarFichero,ListarJugadores,MostrarPokemons,ClonarPokemon,RecibirMT=\
        ("Ha subido un fichero",
         "Ha descargado un fichero",
         "Ha listado los jugadores",
         "Ha mostrado los pokemons de los jugadores",
         "Ha clonado un pokemon",
         "Ha comprado una MT")

def sendOK( s, params="" ):
    s.sendall( ("OK-{}\r\n".format( params )).encode( "ascii" ) )

def sendER( s, code=1 ):
    s.sendall( ("ER-{}\r\n".format( code )).encode( "ascii" ) )

def initpaths():
    SAV_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)

