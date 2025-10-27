import socket
import sys
import os

servidor = "localhost"

if len(sys.argv) < 2:
    print("Introduce un comando"
          "\n 1.Upload"
          "\n 2.Download"
          "\n 3.VerPokemons"
          "\n 4.RobarPokemon"
          "\n 5.ClonarPokemon"
          "\n 6.Listar_jugadores")
    sys.exit(1)


def upload(path_fichero, nombre_jugador):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servidor, 12345))

    with open(path_fichero, "rb") as f:
        data = f.read()

    message = b'1' + data + b'|||' + nombre_jugador.encode()
    sock.sendall(message)

    response = sock.recv(1024)
    print(response.decode())
    sock.close()


option = sys.argv[1]

match option.lower():
    case "upload":
        if len(sys.argv) != 4:
            print("Uso: cli.py upload -path -jugador")
        else:
            path_fichero = sys.argv[2]
            nombre_jugador = sys.argv[3]
            upload(path_fichero, nombre_jugador)

    case "2":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((servidor, 12345))
        sock.send(b'6|||')
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break

        if not data:
            print("No hay jugadores registrados")
        else:
            jugadores = data.split(b'!!!')
            lista_jugadores = [j.decode() for j in jugadores if j]
            if not os.path.exists("save_downloaded"):
                os.mkdir("save_downloaded")
        sock.close()

    case "6":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((servidor, 12345))
        sock.send(b'6')

        data = b''
        sock.settimeout(1.0)
        try:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 4096:
                    break
        except socket.timeout:
            pass
        finally:
            sock.settimeout(None)

        if data:
            jugadores = data.split(b'!!!')
            print("Jugadores disponibles:")
            for jugador in jugadores:
                if jugador:
                    print(f"- {jugador.decode()}")
        else:
            print("No hay jugadores registrados")

        sock.close()