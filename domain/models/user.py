import os


class User:
    def __init__(self, nombre: str, base_path: str = "./saves_server"):
        self.nombre = nombre
        self.path = os.path.join(base_path, nombre)

    def crear_directorio(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
            return True
        return False

    def existe(self):
        return os.path.exists(self.path)

    def get_save_path(self):
        return os.path.join(self.path, "save.sav")

    def tiene_save(self):
        return os.path.exists(self.get_save_path())

    def __str__(self):
        return f"User(nombre={self.nombre}, path={self.path})"

    def __repr__(self):
        return self.__str__()
