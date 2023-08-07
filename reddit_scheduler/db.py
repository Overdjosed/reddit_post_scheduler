from os import listdir, getcwd, walk, mkdir
from praw import Reddit
from sqlite3 import connect
from random import sample

class Empty(Exception):
    pass

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
        self.__arch = {"Users":("IdCliente TEXT, ClientSecret TEXT, UserAgent TEXT, Passw TEXT, Username TEXT",5, "Username"),
                       "Subreddits": ("Subreddit TEXT",1, "Subreddit"),
                       "Scheduler": ("File TEXT,Subreddit TEXT,Title TEXT,Url TEXT,Date TEXT,Hour TEXT, User TEXT, Checkbox TEXT",8, "Date")}
        # Busca ruta de Base de datos
        self.file_path = None
        self.data = None
        self.name = None
        # Busca si existe la base de datos
        # y la carpeta de posts
        for root, _, files in walk(path):
            for file in files:
                if file.endswith(".db"):
                    self.file_path = root
                    self.name = file
                    makeDir()
                    self.connection  = connect(self.name)
                    self.cursor = self.connection.cursor()
                    break

            if self.is_empty():
                self.name = "reddit.db"
                self.connection  = connect(self.name)
                self.cursor = self.connection.cursor()
                # Create Users db, Subreddits db and Scheduler
                for name, data in self.__arch.items():
                    self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({data[0]})")
                self.connection.commit()

    def is_empty(self):
        # Si no encuentra el archivo .db, devuelve False
        return self.name is None

    def add_element(self, data, type = None):
        if type == "Subreddits":
            num = "?, "*(self.__arch[type][1])
            args = self.__arch[type][0].replace(" TEXT","")
            print(f"INSERT INTO {type} ({args}) VALUES ({num[:-2]})", data)
            self.cursor.execute(f"INSERT INTO Subreddits (Subreddit) VALUES (?)", (data,))
            self.connection.commit()
            return

        num = "?, "*(self.__arch[type][1])
        args = self.__arch[type][0].replace(" TEXT","")
        print(data)
        print(f"INSERT INTO {type} ({args}) VALUES ({num[:-2]})", data)
        self.cursor.execute(f"INSERT INTO {type} ({args}) VALUES ({num[:-2]})",data)
        self.connection.commit()

    def get_element(self, value, type):
        self.cursor.execute("SELECT  * FROM {} WHERE {} = ?".format(type,self.__arch[type][2]),(value,))
        self.connection.commit()
        tuplas = self.cursor.fetchall()[0]
        return {"client_id": tuplas[0], "client_secret": tuplas[1], "username": tuplas[2], "password": tuplas[3], "user_agent": tuplas[4]}

    def delete_element(self, value, type):
        print("DELETE FROM {} WHERE {} = ?".format(type,self.__arch[type][2]),(value,))
        self.cursor.execute("DELETE FROM {} WHERE {} = ?".format(type,self.__arch[type][2]),(value,))
        self.connection.commit()

    def show_database(self, type, all = False):
        data = []
        if type == "Users":
            self.cursor.execute(f"SELECT Username FROM Users")
        elif type == "Subreddits":
            self.cursor.execute(f"SELECT Subreddit FROM Subreddits")
        elif type == "Scheduler":
            if all == True:
                self.cursor.execute(f"SELECT * FROM Scheduler")
                tuplas = self.cursor.fetchall()
                return tuplas
            else:
                self.cursor.execute(f"SELECT Date, Title FROM Scheduler")

        tuplas = self.cursor.fetchall()
        if len(tuplas) == 1:
            if type == "Scheduler":
                data.append(f"Date : {tuplas[0][0]}, Title: {tuplas[0][1]}")
            else:
                data.append(tuplas[0][0])
        else:
            for element in tuplas:
                if type == "Scheduler":
                    data.append(f"Date : {element[0]}, Title: {element[1]}")
                else:
                    data.append(element[0])

        return data

    def get_photos(self):
        photos = []
        for _, _, files in walk(self.file_path+"\\posts"):
                for file in files:
                    if file.endswith(".jpg") or file.endswith(".png"):
                        photos.append(file)
        return photos

