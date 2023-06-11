import os
import sqlite3
from os.path import join

def checkDir():
    # Revisa si carpeta existe
    if 'posts' in os.listdir(os.getcwd()):
        return True
    return False

def makeDir():
    if checkDir():
        return
    else:
        # Crea carpeta si no existe carpeta de posts
        os.mkdir(os.getcwd() + '\\posts')

class Controlador:

    def __init__(self, path=os.getcwd()):
        # Busca ruta de Base de datos
        self.file_path = None
        self.name = None
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".db"):
                    self.file_path = root
                    self.name = file
                    makeDir()
                    break


    def is_empty(self):
        # Si no encuentra el archivo .db, devuelve False
        return self.name is None

    def __connect(self, command, data = None, datatable = "bots"):
        conexion = sqlite3.connect(self.name)
        # Crear un cursor para ejecutar comandos SQL
        cursor = conexion.cursor()

        if command == "create":
            # Si no existe base de datos, crea Tabla Bots y tabla Scheduler
            cursor.execute('''CREATE TABLE IF NOT EXISTS Botones (
            Identificador TEXT,
            IdCliente TEXT,
            ClientSecret TEXT,
            UserAgent TEXT,
            Passw TEXT,
            Username TEXT
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Programador (
            File TEXT,
            Subreddit TEXT,
            Title TEXT,
            Url TEXT,
            Date TEXT,
            Hour TEXT,
            Minute TEXT
            )''')
            conexion.commit()

        elif command == "update":
            if datatable == "bots":
                cursor.execute("INSERT INTO Botones (Identificador, IdCliente, ClientSecret, UserAgent, Passw, Username) VALUES (?, ?, ?, ?, ?, ?)",
                        data)
            elif datatable == "programmer":
                cursor.execute("INSERT INTO Programador (File, Subreddit, Title, Url, Date, Hour, Minute) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        data)
            conexion.commit()
            cursor = conexion.cursor()

        elif command == "show":
            cursor.execute("SELECT * FROM Botones")
            registros = cursor.fetchall()

        conexion.close()
        return None if command != "show" else registros

    def get_photos(self):
        # Introduce los archivos .jpg y .png de la carpeta posts
        conexion = sqlite3.connect(self.name)
        cursor = conexion.cursor()

        photos = []
        for _, _, files in os.walk(self.file_path+"\\posts"):
                for file in files:
                    if file.endswith(".jpg") or file.endswith(".png"):
                        photos.append(file)
        return photos

    def create_db(self, name = "redditbots.db"):
        if self.is_empty():
            self.name = name
        self.__connect(command="create")

    def update_bots(self, *args):
        self.__connect(command="update", data = args[0], datatable="bots")


    def update_programmer(self, *args):
        self.__connect(command="update", data = args[0], datatable = "programmer")

    def __str__(self) -> str:
        # Muestra Bots de Upvotes
        registros = self.__connect(command="show")

        # Convertir los registros en una lista de diccionarios
        datos = []
        for registro in registros:
            diccionario = {
                'IdCliente': registro[1],
                'ClientSecret': registro[2],
                'UserAgent': registro[3],
                'Passw': registro[4],
                'Username': registro[5]
            }
            datos.append(diccionario)

        output = ""
        for diccionario in datos:
            output += "\nBot: "+ diccionario["Username"]+ "\n" + str(diccionario)+ "\n"

        return output