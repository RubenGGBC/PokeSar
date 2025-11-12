import socket
import sys
import os
from os import  makedirs
from pathlib import Path

import helpers
from cli_helpers import Menu
from helpers import Comando


servidor = "localhost"
activeUser = ""

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servidor, 12345))
    while True:
        Menu.mostrar_menu()
        opcion = Menu.pedir_opcion_menu()
        match opcion:
            case Menu.User:
                if activeUser == "":
                    nombre = input("Introduce tu nombre de usuario: ")
                    msj = Comando.User+nombre+helpers.FIN_LINEA
                    sock.sendall(msj.encode())
                    resp = helpers.recvline(sock).decode()
                    if helpers.iserror(resp):
                       print("No se ha podido iniciar sesion")
                       continue
                    print(f"Has iniciado sesion como: {nombre}")
                    activeUser = nombre
                else:
                    print(f"Ya se ha iniciado sesion como: {activeUser}")

            case Menu.Upload:
                if activeUser == "":
                    print("Debes iniciar sesión primero")
                else:
                    path = input("Introduce la direccion del fichero: ")
                    if not path.endswith('.sav'):
                        print("El archivo debe ser un fichero .sav")
                        continue
                    try:
                        with open(path, "rb") as f:
                            filesize = os.path.getsize(path)
                            filedata = f.read()
                    except FileNotFoundError:
                        print("El archivo no existe")
                        continue
                    msj = Comando.Upload + str(filesize) + helpers.FIN_LINEA
                    sock.sendall(msj.encode())
                    resp = helpers.recvline(sock).decode()
                    if helpers.iserror(resp):
                        continue
                    sock.sendall(filedata)
                    resp = helpers.recvline(sock).decode()
                    if not helpers.iserror(resp):
                        print("fichero subido correctamente")

            case Menu.Download:
                if activeUser == "":
                    print("Debes iniciar sesión primero (USER)")
                    continue
                path= input("Introduce la direccion del fichero: ").strip()
                path_descarga = Path(path).expanduser()
                tipo = str(input("Introduce el tipo de fichero a descargar (sav/log): ")).strip().lower()
                if tipo not in [helpers.SAV,helpers.LOG]:
                    print("Tipo inválido. Debe ser 'sav' o 'log'")
                    continue
                else:
                    msj = Comando.Download + tipo + helpers.FIN_LINEA
                    sock.sendall(msj.encode())
                    resp = helpers.recvline(sock).decode().strip()
                    if helpers.iserror(resp):
                        continue
                    params = resp[3:].split(helpers.SEPARADOR_ARGS)
                    print(params)
                    tam_fichero = int(params[0].replace("b'", "").replace("'", "").strip())
                    filename = params[1].replace("b'", "").replace("'", "").strip()
                    print("reciviendo fichero")
                    filedata = helpers.recvall(sock,tam_fichero)
                    fichero = path_descarga / Path(filename).name
                    try:
                        makedirs(path_descarga,exist_ok=True)
                        with open(fichero, "wb") as f:
                            f.write(filedata)
                        print("Fichero descargado correctamente")
                    except OSError:
                        print("El archivo no se ha podido descargar")

            case Menu.ListarJugadores:
                msj = Comando.ListarJugadores + helpers.FIN_LINEA
                sock.sendall(msj.encode())
                resp = helpers.recvline(sock).decode()
                if helpers.iserror(resp):
                    continue
                jugadores = resp[3:].split(helpers.SEPARADOR_ARGS)
                print("Jugadores disponibles")
                for jugador in jugadores:
                    print(jugador)

            case Menu.Clonar:
                jugador = str(input("Introduce el jugador al que le pertenece el pokemon: "))
                posicion = str(input("Introduce la posicion del pokemon: "))
                msj = Comando.Clonar+jugador+helpers.SEPARADOR_ARGS+posicion+helpers.FIN_LINEA
                sock.sendall(msj.encode())
                resp = helpers.recvline(sock).decode()
                if helpers.iserror(resp):
                    continue
                print(resp)

            case Menu.Salir:
                msj = Comando.Salir + helpers.FIN_LINEA
                sock.sendall(msj.encode())
                resp = helpers.recvline(sock).decode()
                break
    sock.close()
