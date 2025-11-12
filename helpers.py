SEPARADOR_ARGS = "@"
FIN_LINEA = "\r\n"
OK_CODE = "OK"
ERROR_CODE = "ER"
SAV = "sav"
LOG = "log"
PKM = "pkm"

ERROR_MSG = (
    "Comando desconocido o inesperado",
    "No ha sido posible iniciar sesion",
    "Error al subir fichero",
    "Error al bajar el fichero.",
    "Un usuario anonimo no tiene permisos para esta operacion.",
    "El directorio esta vacio",
    "No se ha podido clonar"
    )

class Comando:
    User, Upload, Download, MostrarPokemon, ListarJugadores, Clonar, RecibirMt, Salir = ("USER","UPLD","DWLD","PKMN","LIST","CLON","RCMT","EXIT")


def recvline( s, removeEOL = True ):
    line = b''
    CRreceived = False
    while True:
        c = s.recv( 1 )
        if c == b'':
            raise EOFError( "Connection closed by the peer before receiving an EOL." )
        line += c
        if c == b'\r':
            CRreceived = True
        elif c == b'\n' and CRreceived:
            if removeEOL:
                return line[:-2]
            else:
                return line
        else:
            CRreceived = False

"""
Reads exactly size bytes from socket s and returns them.
"""
def recvall( s, size ):
    message = b''
    while( len( message ) < size ):
        chunk = s.recv( size - len( message ) )
        if chunk == b'':
            raise EOFError( "Connection closed by the peer before receiving the requested {} bytes.".format( size ) )
        message += chunk
    return message


def iserror(msg,code=1):
    if msg.startswith("ER-"):
        code = int(msg[2:])
        print(ERROR_MSG[code])
        return True
    else:
        return False

