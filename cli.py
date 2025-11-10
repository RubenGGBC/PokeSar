import socket
import sys
import os
import cli_methods
from menu import Menu

servidor = "localhost"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((servidor, 12345))

cli_methods.sock = sock
cli_methods.separador = Menu.SEPARADOR

while True:
    try:
        Menu.mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip().upper()

        if opcion not in Menu.COMANDOS_DISPONIBLES:
            print(f"Comando inválido. Los comandos disponibles son: {', '.join(Menu.COMANDOS_DISPONIBLES)}")
            input("\nPresiona Enter para continuar...")
            continue

        cli_methods.comando = opcion

        match cli_methods.comando:
            case Menu.USER:
                nombre=input("Introduce tu nombre de usuario: ")
                mensaje = Menu.USER.encode() + Menu.SEPARADOR + nombre.encode()
                sock.sendall(mensaje)
                if(sock.recv(1024).decode() == Menu.OK):
                    print(f"Has iniciado sesion como: {nombre}")
                    cli_methods.user = nombre
                else:
                    print("Ha ocurrido un error")


            case Menu.UPLOAD:
                if cli_methods.user is None:
                    print("Debes iniciar sesión primero (USER)")
                else:
                    cli_methods.upload(cli_methods.user)

            case Menu.DOWNLOAD:
                if cli_methods.user is None:
                    print("Debes iniciar sesión primero (USER)")
                else:
                    tipo = input("Introduce el tipo de fichero a descargar (sav/log): ").strip().lower()
                    if tipo not in [Menu.TIPO_SAV, Menu.TIPO_LOG]:
                        print("Tipo inválido. Debe ser 'sav' o 'log'")
                    else:
                        mensaje = Menu.DOWNLOAD.encode() + Menu.SEPARADOR + cli_methods.user.encode() + Menu.SEPARADOR + tipo.encode()
                        sock.sendall(mensaje)

                        resultado = cli_methods.recibir_descarga(cli_methods.user, tipo)
                        if resultado:
                            print(resultado)

            case Menu.POKEMON:
                lista_jugadores = input("Introduce los nombres de los jugadores separados por comas: ")
                lista_usuarios = [nombre.strip() for nombre in lista_jugadores.split(',')]
                cli_methods.ver_pokemons_usuarios(lista_usuarios)

            case Menu.LIST:
                cli_methods.listar_jugadores()

            case "robarpokemons":
                nombre_jugador = input("Introduce el nombre del jugador al que quieres robarle el pokemon: ")
                posicion = int(input("Introduce la posicion del pokemon: "))
                direccion = input("Introduce la direccion de tu archivo de guardado: ")
                cli_methods.robarpokemon(nombre_jugador, posicion, direccion)
        
        
    except KeyboardInterrupt:
        print("\nSaliendo...")
        break
    except Exception as e:
        print(f"Error: {e}")
        input("\nPresiona Enter para continuar...")

sock.close()