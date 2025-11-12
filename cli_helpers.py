
class Menu:

    User,Upload,Download,MostrarPokemon,ListarJugadores,Clonar,RecibirMt,Salir = range(1,9)
    Next,Prev,Show,Stop = range(1,5)
    opciones_menu = ("Iniciar sesion", "Subir fichero", "Descargar fichero", "Mostrar pokemons", "Listar jugadores", "Clonar Pokemon", "Recibir MT", "Salir")
    opciones_pokemons = ("Siguiente", "Anterior","Mostrar jugador", "Salir")


    @staticmethod
    def mostrar_menu():
        print("+{}+".format('-' * 30))
        for i,opcion in enumerate(Menu.opciones_menu,1):
            print( "| {}.- {:<25}|".format( i, opcion ) )
        print("+{}+".format('-' * 30))

    @staticmethod
    def pedir_opcion_menu():
        while True:
            try:
                opcion = int(input("Selecciona una opción: "))
            except:
                print("Opción no válida.")
                continue
            if 0 < opcion <= len(Menu.opciones_menu):
                return opcion
            else:
                print("Opción no válida.")

    @staticmethod
    def mostrar_menu_navegacion():
        print("+{}+".format('-' * 30))
        for i, opcion in enumerate(Menu.opciones_pokemons, 1):
            print("| {}.- {:<25}|".format(i, opcion))
        print("+{}+".format('-' * 30))

    @staticmethod
    def pedir_opcion_menu_navegacion():
        while True:
            try:
                opcion = int(input("Selecciona una opción: "))
            except:
                print("Opción no válida.")
                continue
            if 0 < opcion <= len(Menu.opciones_pokemons):
                return opcion
            else:
                print("Opción no válida.")



