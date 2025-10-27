import os
import socket
import sys
import signal

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

        comando_byte = dialogo.recv(1)
        if not comando_byte:
            dialogo.close()
            exit(0)

        comando = comando_byte

        match comando:
            case b'1':
                data = b''
                while True:
                    chunk = dialogo.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b'|||' in data:
                        break

                if not os.path.exists("./saves_server"):
                    os.mkdir("./saves_server")

                separator_pos = data.rfind(b'|||')
                if separator_pos == -1:
                    print("no hay nombre de jugador")
                    dialogo.close()
                    sys.exit(1)

                save_data = data[:separator_pos]
                nombre = data[separator_pos + 3:].decode()
                player_dir = f"./saves_server/{nombre}"
                if not os.path.exists(player_dir):
                    os.mkdir(player_dir)

                save_path = f"{player_dir}/save.sav"
                with open(save_path, "wb") as f:
                    f.write(save_data)
                print(f"Save subida, nombre del player:: {nombre}")
                dialogo.send(b"Upload finalizada correctamente")

            case b'2':
                remaining_data = dialogo.recv(1024)
                nombre = remaining_data.decode().strip()
                save_path = f"./saves_server/{nombre}/save.sav"
                if os.path.exists(save_path):
                    with open(save_path, "rb") as f:
                        save_data = f.read()
                    dialogo.send(save_data)
                    print(f"Save descargada de : {nombre}")
                else:
                    dialogo.send(b"Error no se ha encontrado el jugador")
                    print(f"No sea ha encontrado la save de: {nombre}")

            case b'6':
                if os.path.exists("./saves_server"):
                    nombres_dirs = os.listdir("./saves_server")
                    mensaje = b""
                    for nombre in nombres_dirs:
                        if os.path.isdir(f"./saves_server/{nombre}"):
                            if mensaje:
                                mensaje += b'!!!' + nombre.encode()
                            else:
                                mensaje = nombre.encode()
                    dialogo.sendall(mensaje)
                else:
                    dialogo.sendall(b"")

        dialogo.close()
        sys.exit(0)