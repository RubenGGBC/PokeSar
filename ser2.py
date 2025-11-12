import os
import socket
import signal
from pathlib import Path
import helpers
import ser_helpers
from helpers import Comando
from ser_helpers import Evento, sendER

PORT = 12345

def escribir_log(evento,usuario,*args):
    with open(ser_helpers.LOG_PATH/Path(ser_helpers.DEFAULT_LOG_NAME), "a") as f:
        if args is None:
            f.write(f"{usuario}:{evento}\n")
        else:
            f.write(f"{usuario} {evento}: {args}")

def session(sock):

    usuario_sesion = None
    path_save_usuario = None

    while True:

        msg = helpers.recvline(sock).decode()
        if not msg:
            continue

        if msg.startswith(Comando.User):
            nombre = msg[4:]
            if not nombre:
                ser_helpers.sendER(sock, 1)
                continue
            usuario_sesion = nombre
            path_save_usuario = ser_helpers.SAV_PATH/Path(usuario_sesion)
            os.makedirs(path_save_usuario,exist_ok=True)
            ser_helpers.sendOK(sock)
            print(f"Sesión iniciada para: {nombre}")

        elif msg.startswith(Comando.Upload):
            tam_fichero = int(msg[4:])
            if tam_fichero is None or usuario_sesion is None:
                ser_helpers.sendER(sock, 2)
                continue
            ser_helpers.sendOK(sock)

            save_path = ser_helpers.SAV_PATH/Path(usuario_sesion)/Path(ser_helpers.DEFAULT_SAV_NAME)
            print(save_path)
            filedata = helpers.recvall(sock, tam_fichero)
            try:
                with open(save_path, "wb") as f:
                    f.write(filedata)
            except:
                ser_helpers.sendER(sock, 2)
            else:
                escribir_log(Evento.SubirFichero,usuario_sesion,save_path)
                ser_helpers.sendOK(sock)

        elif msg.startswith(Comando.Download):
            params = msg[4:]
            if not params.startswith(helpers.PKM):
                print(params)
                if params.startswith(helpers.SAV):
                    filename = ser_helpers.DEFAULT_SAV_NAME
                    filepath = os.path.join(path_save_usuario, filename)
                else:
                    filename = ser_helpers.DEFAULT_LOG_NAME
                    filepath = os.path.join(ser_helpers.LOG_PATH, filename)
                try:
                    filesize = os.path.getsize(filepath)
                except:
                    ser_helpers.sendER(sock, 2)
                    continue
                else:
                    msg = str(filesize)+helpers.SEPARADOR_ARGS+filename
                    ser_helpers.sendOK(sock,msg.encode())
                    try:
                        with open(filepath, "rb") as f:
                            filedata = f.read()
                        sock.sendall(filedata)
                        escribir_log(Evento.DescargarFichero, usuario_sesion, filename)
                    except:
                        ser_helpers.sendER(sock, 3)
                    else:
                        ser_helpers.sendOK(sock)
                        sock.sendall(filedata)
            else:
                ser_helpers.sendER(sock, 3)

        elif msg.startswith(Comando.Salir):

            ser_helpers.sendOK(sock)
            return

        else:
            sendER(sock,1)


def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PORT))
    sock.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    ser_helpers.initpaths()

    while True:
        dialog, addr = sock.accept()
        print("Conexión aceptada del socket {0[0]}:{0[1]}.".format(addr))
        if os.fork():
            dialog.close()
        else:
            sock.close()
            session(dialog)
            dialog.close()
            exit(0)
    sock.close()
if __name__ == "__main__":
    main()