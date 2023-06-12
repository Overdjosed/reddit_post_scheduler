from os import listdir, getcwd, walk, mkdir
from praw import Reddit
from sqlite3 import connect
from time import sleep
from random import sample
from os.path import join

def checkDir():
    # Revisa si carpeta existe
    if 'posts' in listdir(getcwd()):
        return True
    return False

def makeDir():
    if checkDir():
        return
    else:
        # Crea carpeta si no existe carpeta de posts
        mkdir(getcwd() + '\\posts')

class Controlador:

    def __init__(self, path = getcwd()):
        # Busca ruta de Base de datos
        self.file_path = None
        self.data = None
        self.name = None
        for root, _, files in walk(path):
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
        conexion = connect(self.name)
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
        conexion = connect(self.name)
        cursor = conexion.cursor()

        photos = []
        for _, _, files in walk(self.file_path+"\\posts"):
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

    def sorted_data(self):
        if not self.data:
            # Muestra Bots de Upvotes
            registros = self.__connect(command="show")

            # Convertir los registros en una lista de diccionarios
            self.data = []
            for registro in registros:
                diccionario = {
                    'IdCliente': registro[1],
                    'ClientSecret': registro[2],
                    'UserAgent': registro[3],
                    'Passw': registro[4],
                    'Username': registro[5]
                }
                self.data.append(diccionario)

    def __str__(self) -> str:
        # Muestra Bots de Upvotes
        self.sorted_data()

        output = ""
        for diccionario in self.data:
            output += "\nBot: "+ diccionario["Username"]+ "\n" + str(diccionario)+ "\n"

        return output


    def upvote(self, total_upvotes, url, timeframe):

        self.sorted_data()

        if len(self.data) < total_upvotes:
            random_elements = sample(self.data, total_upvotes)
            for bot in random_elements:
                reddit = Reddit(
                    client_id= bot[1],
                    client_secret= bot[2],
                    user_agent= bot[3],
                    username= bot[5],
                    password= bot[4]
                )
                sleep(timeframe)

            target_url = url
            post_id = target_url.split('/')[-3]

            target = reddit.submission(id=post_id)
            target.upvote()