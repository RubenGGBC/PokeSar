import socket
import sys
import os

servidor = "localhost"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((servidor, 12345))

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
    with open(path_fichero, "rb") as f:
        data = f.read()

    message = b'1' + data + b'|||' + nombre_jugador.encode()
    sock.sendall(message)

    response = sock.recv(1024)
    print(response.decode())

def obtener_datos():
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
    return data

def mostrarPokemons(nombre_jugador, separador):
    sock.send(b'3' + nombre_jugador.encode() + b'!!!' + separador.to_bytes(1, 'big'))
    
    primera_vez = True
    while True:
        datos = obtener_datos()
        if not datos:
            if primera_vez:
                print("No se encontraron pokemons o el jugador no existe")
            else:
                print("No hay mass pokemons")
            break
            
        print(datos.decode())
        primera_vez = False
        
        continuar = input("\nPresiona Enter para continuar o 'q' para salir: ")
        if continuar.lower() == 'q':
            break
            
        sock.send(b'continuar')


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
        if len(sys.argv) != 3:
            print("Uso: cli.py 2 -nombre_jugador")
        else:
            nombre_jugador = sys.argv[2]
            sock.send(b'2' + nombre_jugador.encode())
            data = obtener_datos()
            
            if not data:
                print("No se pudo descargar el save")
            elif data == b"No se ha encontrado el jugador":
                print("jugador no encontrado")
            else:
                if not os.path.exists("save_downloaded"):
                    os.mkdir("save_downloaded")
                save_path = f"save_downloaded/{nombre_jugador}.sav"
                with open(save_path, "wb") as f:
                    f.write(data)
                print(f"Save descargado en: {save_path}")

    case "3":
        if len(sys.argv) != 4:
            print("Uso: cli.py 3 -nombre_jugador -separador")
        else:
            nombre_jugador = sys.argv[2]
            separador = int(sys.argv[3])
            mostrarPokemons(nombre_jugador, separador)



    case "6":
        sock.send(b'6')
        data = obtener_datos()

        if data:
            jugadores = data.split(b'!!!')
            print("Jugadores disponibles:")
            for jugador in jugadores:
                if jugador:
                    print(f"- {jugador.decode()}")
        else:
            print("No hay jugadores registrados")

sock.close()