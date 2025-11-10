import os
import socket
import sys
import signal
import json
from domain.services.pokemon_service import get_pokemon_boxes
from domain.services.pokemon_service import clone_pokemon
from menu import Menu

def recibir_datos_completos(dialogo, tamaño_total):
    datos = b''
    bytes_restantes = tamaño_total

    while bytes_restantes > 0:
        chunk_size = min(4096, bytes_restantes)
        chunk = dialogo.recv(chunk_size)
        if not chunk:
            return None
        datos += chunk
        bytes_restantes -= len(chunk)

    return datos

def recibir_mensaje_completo(dialogo):
    data = b''
    try:
        while True:
            chunk = dialogo.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break
    except Exception as e:
        print(f"Error recibiendo mensaje: {e}")
    return data

def sendError(dialogo, mensaje):
    dialogo.send(f"{Menu.ERROR}: {mensaje}".encode())

def sendOk(dialogo):
    dialogo.send(Menu.OK.encode())

PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', PORT))
sock.listen(5)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
    dialogo, _ = sock.accept()

    if os.fork():
        dialogo.close()
    else:
        sock.close()

        usuario_sesion = None

        while True:
            mensaje_completo = recibir_mensaje_completo(dialogo)
            if not mensaje_completo:
                print(f"Cliente desconectado: {usuario_sesion if usuario_sesion else 'desconocido'}")
                dialogo.close()
                exit(0)

            partes = mensaje_completo.split(Menu.SEPARADOR, 1)
            if len(partes) < 1:
                sendError(dialogo, "Mensaje vacío")
                continue

            comando = partes[0].decode().strip()

            match comando:
                case Menu.USER:
                    if len(partes) < 2:
                        sendError(dialogo, "No se recibio el nombre de usuario")
                        continue

                    nombre = partes[1].decode().strip()

                    if not os.path.exists("./saves_server"):
                        os.mkdir("./saves_server")

                    player_dir = f"./saves_server/{nombre}"
                    if not os.path.exists(player_dir):
                        os.mkdir(player_dir)
                        print(f"Directorio creado para nuevo usuario: {nombre}")
                    else:
                        print(f"Usuario existente conectado: {nombre}")

                    usuario_sesion = nombre
                    sendOk(dialogo)
                    print(f"Sesión iniciada para: {nombre}")

                case Menu.UPLOAD:
                    if len(partes) < 2:
                        sendError(dialogo, "No se recibieron los datos completos")
                        continue

                    partes_upload = partes[1].split(Menu.SEPARADOR, 1)
                    if len(partes_upload) < 2:
                        sendError(dialogo, "No se recibieron los datos completos")
                        continue

                    nombre = partes_upload[0].decode().strip()
                    save_data = partes_upload[1]

                    if not save_data:
                        sendError(dialogo, "No se recibieron datos del archivo")
                        continue

                    print(f"Tamaño del archivo recibido de {nombre}: {len(save_data)} bytes")

                    if not os.path.exists("./saves_server"):
                        os.mkdir("./saves_server")

                    player_dir = f"./saves_server/{nombre}"
                    if not os.path.exists(player_dir):
                        os.mkdir(player_dir)

                    save_path = f"{player_dir}/save.sav"
                    bytes_escritos = 0
                    with open(save_path, "wb") as f:
                        bytes_escritos = f.write(save_data)

                    print(f"Save subido para {nombre}: {bytes_escritos} bytes escritos")
                    dialogo.send(str(bytes_escritos).encode())

                case Menu.DOWNLOAD:
                    if len(partes) < 2:
                        sendError(dialogo, "Formato incorrecto")
                        continue

                    partes_download = partes[1].split(Menu.SEPARADOR)
                    if len(partes_download) < 2:
                        sendError(dialogo, "Formato incorrecto")
                        continue

                    nombre = partes_download[0].decode().strip()
                    tipo = partes_download[1].decode().strip()

                    if tipo == Menu.TIPO_SAV:
                        ruta_archivo = f"./saves_server/{nombre}/save.sav"
                        if os.path.exists(ruta_archivo):
                            with open(ruta_archivo, "rb") as f:
                                datos = f.read()

                            tamaño_archivo = len(datos)
                            tamaño_bytes = tamaño_archivo.to_bytes(4, 'big')
                            dialogo.sendall(tamaño_bytes)
                            dialogo.sendall(datos)
                            print(f"Save descargado de: {nombre} ({tamaño_archivo} bytes)")
                        else:
                            sendError(dialogo, "No se ha encontrado el archivo de guardado")
                            print(f"No se ha encontrado la save de: {nombre}")
                    elif tipo == Menu.TIPO_LOG:
                        ruta_archivo = "./server.log"
                        if os.path.exists(ruta_archivo):
                            with open(ruta_archivo, "rb") as f:
                                datos = f.read()

                            tamaño_archivo = len(datos)
                            tamaño_bytes = tamaño_archivo.to_bytes(4, 'big')
                            dialogo.sendall(tamaño_bytes)
                            dialogo.sendall(datos)
                            print(f"Log descargado por: {nombre} ({tamaño_archivo} bytes)")
                        else:
                            sendError(dialogo, "No se ha encontrado el archivo de log")
                            print(f"No se ha encontrado el archivo de log")
                    else:
                        sendError(dialogo, "Tipo de archivo invalido")
                        print(f"Tipo invalido recibido: {tipo}")

                case Menu.POKEMON:
                    if len(partes) < 2:
                        sendError(dialogo, "No se recibieron datos para PKMN")
                        continue

                    partes_pokemon = partes[1].split(Menu.SEPARADOR)
                    lista_usuarios = [p.decode().strip() for p in partes_pokemon if p]

                    if not lista_usuarios:
                        sendError(dialogo, "Lista de usuarios vacia")
                        continue

                    tamaño_lista = len(lista_usuarios)

                    def enviar_pokemons_usuario(nombre_usr):
                        save_path = f"./saves_server/{nombre_usr}/save.sav"
                        if not os.path.exists(save_path):
                            dialogo.send(b"Jugador no encontrado")
                            return

                        box_pokemons = get_pokemon_boxes(save_path)
                        if not box_pokemons:
                            dialogo.send(b"No hay pokemons en las cajas")
                            return

                        lista = [p.pokemon.to_dict() for p in box_pokemons]
                        payload = json.dumps(lista).encode()
                        dialogo.sendall(payload)

                    if tamaño_lista == 1:
                        enviar_pokemons_usuario(lista_usuarios[0])
                        continue

                    indice_actual = 0
                    enviar_pokemons_usuario(lista_usuarios[indice_actual])

                    while True:
                        cmd_mensaje = recibir_mensaje_completo(dialogo)
                        if not cmd_mensaje:
                            break

                        cmd_partes = cmd_mensaje.split(Menu.SEPARADOR, 1)
                        if len(cmd_partes) < 1:
                            continue

                        cmd_text = cmd_partes[0].decode().strip()

                        if cmd_text == Menu.STOP:
                            break
                        if cmd_text == Menu.NEXT:
                            indice_actual = (indice_actual + 1) % len(lista_usuarios)
                            enviar_pokemons_usuario(lista_usuarios[indice_actual])
                            continue
                        if cmd_text == Menu.PREV:
                            indice_actual = (indice_actual - 1) % len(lista_usuarios)
                            enviar_pokemons_usuario(lista_usuarios[indice_actual])
                            continue
                        if cmd_text == Menu.SHOW:
                            if len(cmd_partes) < 2:
                                dialogo.send(b"SHOW requiere un usuario")
                                continue
                            objetivo = cmd_partes[1].decode().strip()
                            if objetivo in lista_usuarios:
                                indice_actual = lista_usuarios.index(objetivo)
                                enviar_pokemons_usuario(objetivo)
                            else:
                                dialogo.send(b"Usuario no en lista")
                            continue
                        continue

                case Menu.LIST:
                    if os.path.exists("./saves_server"):
                        nombres_dirs = os.listdir("./saves_server")
                        mensaje = b""
                        for nombre in nombres_dirs:
                            if os.path.isdir(f"./saves_server/{nombre}"):
                                if mensaje:
                                    mensaje += Menu.SEPARADOR + nombre.encode()
                                else:
                                    mensaje = nombre.encode()
                        dialogo.sendall(mensaje)
                    else:
                        dialogo.sendall(b"")
                case Menu.CLONAR:
                    if len(partes) < 2:
                        sendError(dialogo, "No se recibieron datos para CLON")
                        continue

                    partes_clonar = partes[1].split(Menu.SEPARADOR)
                    if len(partes_clonar) < 2:
                        sendError(dialogo, "CLON requiere jugador y posicion")
                        continue

                    jugador = str(partes_clonar[0].decode().strip())
                    try:
                        posicion = int(partes_clonar[1].decode().strip())
                    except ValueError:
                        sendError(dialogo, "Posicion debe ser un numero")
                        continue

                    save_path = str(f"./saves_server/{jugador}/save.sav")
                    if not os.path.exists(save_path):
                        sendError(dialogo, "Jugador no encontrado")
                        print(f"No se encontro el save de: {jugador}")
                        continue

                    try:
                        box_pokemons = get_pokemon_boxes(save_path)
                        if not box_pokemons:
                            sendError(dialogo, "No hay pokemons en las cajas")
                            continue

                        print(f"\033[93m{'='*80}\033[0m")
                        print(f"\033[93mCAJAS ANTES DE CLONAR - {jugador}\033[0m")
                        print(f"\033[93m{'='*80}\033[0m")
                        for p in box_pokemons:
                            if int(p.box_position) == posicion:
                                print(f"\033[96m>>> Posicion {p.box_position}: {p.pokemon.nickname} (Lv.{p.pokemon.level}) - {p.pokemon.species_name} <<<\033[0m")
                            else:
                                print(f"\033[94mPosicion {p.box_position}: {p.pokemon.nickname} (Lv.{p.pokemon.level}) - {p.pokemon.species_name}\033[0m")
                        print(f"\033[93m{'='*80}\033[0m")
                        print(f"\033[93mTotal: {len(box_pokemons)} Pokemons\033[0m\n")

                        pokemon_a_clonar = None
                        for p in box_pokemons:
                            if int(p.box_position) == posicion:
                                pokemon_a_clonar = p.pokemon
                                break

                        if pokemon_a_clonar is None:
                            sendError(dialogo, f"No hay pokemon en la posicion {posicion}")
                            print(f"\033[91mNo se encontro pokemon en posicion {posicion} para {jugador}\033[0m")
                            continue

                        clone_path = str(f"./saves_server/{jugador}/save.sav")
                        clone_pokemon(save_path, save_path, posicion, clone_path)

                        box_pokemons_despues = get_pokemon_boxes(clone_path)
                        pokemon_clonado_nuevo = None
                        for p in box_pokemons_despues:
                            if int(p.box_position) not in [int(pb.box_position) for pb in box_pokemons]:
                                pokemon_clonado_nuevo = int(p.box_position)
                                break

                        print(f"\033[92m{'='*80}\033[0m")
                        print(f"\033[92mCAJAS DESPUES DE CLONAR - {jugador}\033[0m")
                        print(f"\033[92m{'='*80}\033[0m")
                        for p in box_pokemons_despues:
                            if int(p.box_position) == posicion:
                                print(f"\033[96m>>> Posicion {p.box_position}: {p.pokemon.nickname} (Lv.{p.pokemon.level}) - {p.pokemon.species_name} (ORIGINAL) <<<\033[0m")
                            elif pokemon_clonado_nuevo and int(p.box_position) == pokemon_clonado_nuevo:
                                print(f"\033[95m>>> Posicion {p.box_position}: {p.pokemon.nickname} (Lv.{p.pokemon.level}) - {p.pokemon.species_name} (CLONADO) <<<\033[0m")
                            else:
                                print(f"\033[94mPosicion {p.box_position}: {p.pokemon.nickname} (Lv.{p.pokemon.level}) - {p.pokemon.species_name}\033[0m")
                        print(f"\033[92m{'='*80}\033[0m")
                        print(f"\033[92mTotal: {len(box_pokemons_despues)} Pokemons\033[0m\n")

                        pokemon_dict = pokemon_a_clonar.to_dict()
                        payload = bytes(json.dumps(pokemon_dict).encode())
                        dialogo.sendall(payload)
                        print(f"\033[92mPokemon clonado exitosamente para {jugador} en posicion {posicion}\033[0m")

                    except Exception as e:
                        sendError(dialogo, f"Error al clonar pokemon: {str(e)}")
                        print(f"\033[91mError al clonar pokemon para {jugador}: {e}\033[0m")
                        continue
