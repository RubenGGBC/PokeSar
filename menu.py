class Menu:

    USER = "USER"
    UPLOAD = "UPLD"
    DOWNLOAD = "DWLD"
    POKEMON = "PKMN"
    LIST = "LIST"
    CLONAR = "CLON"
    RECIBIR_MT = "RECMT"
    SALIR = "0"

    NEXT = "NEXT"
    PREV = "PREV"
    SHOW = "SHOW"
    STOP = "STOP"

    TIPO_SAV = "sav"
    TIPO_LOG = "log"

    OK = "OK"
    ERROR = "ERR"

    SEPARADOR = b"@"
    SEPARADOR_LINEA = "\r\n"

    COMANDOS_DISPONIBLES = (USER, UPLOAD, DOWNLOAD, POKEMON, PREV, NEXT,
                            "ALL", CLONAR, RECIBIR_MT, LIST, SALIR)

    COMANDOS_NAVEGACION = (NEXT, PREV, SHOW, STOP)

    @staticmethod
    def mostrar_menu():
        print("\n" + "="*50)
        print("            POKESAR CLIENT")
        print("="*50)
        print("┌─────────────────────────────────────────────────┐")
        print("│                  COMANDOS                       │")
        print("├─────────────────────────────────────────────────┤")
        print("│  USER   - Registrarte/Iniciar sesión           │")
        print("│  UPLD   - Subir fichero de guardado            │")
        print("│  DWLD   - Descargar fichero (sav/log)          │")
        print("│  PKMN   - Listar pokemon de usuario            │")
        print("│  PREV   - Mostrar anteriores pokemon           │")
        print("│  NEXT   - Mostrar siguientes pokemon           │")
        print("│  STOP   - Dejar de mostrar pokemons            │")
        print("│  SHOW   - Mostrar pokemon de usuario específico│")
        print("│  CLON   - Clonar pokemon                        │")
        print("│  RECMT  - Recibir máquina técnica aleatoria    │")
        print("│  LIST   - Listar jugadores con save            │")
        print("│  0      - Salir                                 │")
        print("└─────────────────────────────────────────────────┘")

    @staticmethod
    def mostrar_menu_navegacion():
        print("\n[Comandos: NEXT, PREV, SHOW <usuario>, STOP]")
