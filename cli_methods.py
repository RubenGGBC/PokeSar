import socket
import os
import json
from menu import Menu

sock = None
comando = None
separador = None
user=None

def upload(nombre_jugador):
    path = input("Introduce la direccion del fichero: ")
    if not os.path.exists(path):
        print("El fichero no existe")
        return

    if not path.endswith('.sav'):
        print("El archivo debe ser un fichero .sav")
        return

    tamaño_archivo = os.path.getsize(path)
    print(f"Tamaño del archivo: {tamaño_archivo} bytes")

    with open(path, "rb") as f:
        data = f.read()

    mensaje = Menu.UPLOAD.encode() + Menu.SEPARADOR + nombre_jugador.encode() + Menu.SEPARADOR + data
    sock.sendall(mensaje)

    response = sock.recv(1024).decode().strip()
    if response.startswith(Menu.ERROR):
        print(f"Error: {response}")
    else:
        print(f"Fichero subido correctamente. Bytes escritos: {response}")

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

def mostrar_pokemons(pokemon_list_json):
    try:
        pokemon_list = json.loads(pokemon_list_json)

        for i, pkmn in enumerate(pokemon_list, 1):
            print(f"\n{'='*70}")
            print(f"  #{i} - {pkmn['nickname']} (Lv.{pkmn['level']}) - {pkmn['species_name']}")
            print(f"{'='*70}")
            print(f"  Tipos: {' / '.join(pkmn['types'])}")
            print(f"  Naturaleza: {pkmn['nature']} | Habilidad: {pkmn['ability_name']}")

            stats = pkmn['stats']
            print(f"\n  Stats:")
            print(f"    HP: {stats['hp']:3d}  ATK: {stats['atk']:3d}  DEF: {stats['defe']:3d}")
            print(f"    SPA: {stats['spa']:3d}  SPD: {stats['spd']:3d}  SPE: {stats['spe']:3d}")

            if pkmn['moveset']:
                print(f"\n  Movimientos: {', '.join(pkmn['moveset'])}")

            if pkmn['held_item']:
                print(f"  Objeto: {pkmn['held_item']}")

        print(f"{'='*70}\n")
        print(f"Total: {len(pokemon_list)} Pokémons")

    except json.JSONDecodeError:
        print(pokemon_list_json.decode() if isinstance(pokemon_list_json, bytes) else pokemon_list_json)

def ver_pokemons_usuarios(lista_usuarios):
    if not lista_usuarios:
        print("La lista de usuarios está vacía")
        return

    tamaño_lista = len(lista_usuarios)

    mensaje = Menu.POKEMON.encode()
    for usuario in lista_usuarios:
        mensaje += Menu.SEPARADOR + usuario.encode()
    sock.sendall(mensaje)

    if tamaño_lista == 1:
        respuesta = obtener_datos()
        if respuesta:
            print(f"\n=== Pokémons de {lista_usuarios[0]} ===")
            mostrar_pokemons(respuesta.decode())
        else:
            print("No se encontraron Pokémons o el jugador no existe")
        return

    indice_actual = 0

    respuesta = obtener_datos()
    if respuesta:
        print(f"\n=== Pokémons de {lista_usuarios[indice_actual]} (posición {indice_actual + 1}/{tamaño_lista}) ===")
        mostrar_pokemons(respuesta.decode())
    else:
        print("No se encontraron Pokémons para el primer usuario")

    while True:
        Menu.mostrar_menu_navegacion()
        comando_input = input("Introduce un comando: ").strip()

        comando_partes = comando_input.split(None, 1)
        comando_principal = comando_partes[0].upper() if comando_partes else ""

        if comando_principal == Menu.STOP:
            mensaje = Menu.STOP.encode()
            sock.sendall(mensaje)
            print("Comunicación de listado cerrada")
            break

        elif comando_principal == Menu.NEXT:
            indice_actual = (indice_actual + 1) % tamaño_lista
            mensaje = Menu.NEXT.encode()
            sock.sendall(mensaje)

            respuesta = obtener_datos()
            if respuesta:
                print(f"\n=== Pokémons de {lista_usuarios[indice_actual]} (posición {indice_actual + 1}/{tamaño_lista}) ===")
                mostrar_pokemons(respuesta.decode())
            else:
                print("No se encontraron Pokémons para este usuario")

        elif comando_principal == Menu.PREV:
            indice_actual = (indice_actual - 1) % tamaño_lista
            mensaje = Menu.PREV.encode()
            sock.sendall(mensaje)

            respuesta = obtener_datos()
            if respuesta:
                print(f"\n=== Pokémons de {lista_usuarios[indice_actual]} (posición {indice_actual + 1}/{tamaño_lista}) ===")
                mostrar_pokemons(respuesta.decode())
            else:
                print("No se encontraron Pokémons para este usuario")

        elif comando_principal == Menu.SHOW:
            if len(comando_partes) < 2:
                print("Debes especificar un usuario. Ejemplo: SHOW Memoni")
                continue

            usuario_objetivo = comando_partes[1].strip()

            usuario_encontrado = None
            for usuario in lista_usuarios:
                if usuario.lower() == usuario_objetivo.lower():
                    usuario_encontrado = usuario
                    break

            if usuario_encontrado is None:
                print(f"El usuario '{usuario_objetivo}' no está en la lista")
                continue

            nuevo_indice = lista_usuarios.index(usuario_encontrado)
            indice_actual = nuevo_indice

            mensaje = Menu.SHOW.encode() + Menu.SEPARADOR + usuario_encontrado.encode()
            sock.sendall(mensaje)

            respuesta = obtener_datos()
            if respuesta:
                print(f"\n=== Pokémons de {lista_usuarios[indice_actual]} (posición {indice_actual + 1}/{tamaño_lista}) ===")
                mostrar_pokemons(respuesta.decode())
            else:
                print("No se encontraron Pokémons para este usuario")

        else:
            print(f"Comando inválido. Usa: {', '.join(Menu.COMANDOS_NAVEGACION)}")
        
              
def download(datos, nombre_jugador, tipo=Menu.TIPO_SAV):
    if not os.path.exists("save_downloaded"):
        os.mkdir("save_downloaded")

    if tipo == Menu.TIPO_LOG:
        ruta_archivo = "save_downloaded/server.log"
    else:
        ruta_archivo = f"save_downloaded/{nombre_jugador}.sav"

    with open(ruta_archivo, "wb") as f:
        bytes_escritos = f.write(datos)

    print(f"Archivo descargado en: {ruta_archivo} ({bytes_escritos} bytes)")


def recibir_datos_completos(tamano):
    datos = b''
    restante = tamano
    while restante > 0:
        tam = min(4096, restante)
        trozo = sock.recv(tam)
        if not trozo:
            return None
        datos += trozo
        restante -= len(trozo)
    return datos


def recibir_descarga(nombre_jugador, tipo=Menu.TIPO_SAV):
    cab = sock.recv(4)
    if not cab:
        print("No se recibió respuesta del servidor")
        return False
    if cab.startswith(Menu.ERROR.encode()):
        resto = b''
        try:
            resto = sock.recv(4096)
        except Exception:
            pass
        mensaje = (cab + resto).decode(errors='ignore')
        print(f"Error del servidor: {mensaje}")
        return False
    if len(cab) < 4:
        falta = 4 - len(cab)
        mas = sock.recv(falta)
        if not mas:
            print("Respuesta incompleta del servidor")
            return False
        cab += mas
    tam_archivo = int.from_bytes(cab, 'big')
    datos = recibir_datos_completos(tam_archivo)
    if datos is None:
        print("Transferencia interrumpida")
        return False
    download(datos, nombre_jugador, tipo)
    return True

def listar_jugadores():
    mensaje = Menu.LIST.encode()
    sock.sendall(mensaje)
    data = obtener_datos()

    if data:
        jugadores = data.split(Menu.SEPARADOR)
        print("Jugadores disponibles:")
        for jugador in jugadores:
            if jugador:
                print(f"- {jugador.decode()}")
    else:
        print("No hay jugadores registrados")

def robarpokemon(nombre_jugador, posicion, direccion):
    sock.sendall(comando.encode()+nombre_jugador.encode()+ separador +posicion.encode()+ separador +direccion.encode())
    data=obtener_datos()
