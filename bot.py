import gui as wt
import controller as ctrl
import wx
from re import findall

def main():
    """Función Main que une 2 bases de datos (Base de Upvotes, Base de Scheduler)"""
    def bot_dialog(event):
        # Base de Datos de Upvotes
        controlador = ctrl.Controlador()
        # Verifica si ya está creado el archivo de reddit
        if controlador.is_empty():
            controlador.create_db()
        decision = frame.binary_question("¿Desea añadir un nuevo Bot?")
        if decision:
            # Si la decision es Afirmativa, se añaden los elementos de el Bot
            data = frame.text_question()
            # Subida elementos a la base de datos
            controlador.update_bots(data)
            # Comprobación en terminal (Pruebas)
            # frame.warning_message("Los datos se han subido correctamente\nComprobacion en terminal:")
            # print(controlador)

    def programmer_dialog(event):
        controlador = ctrl.Controlador()
        # Verifica si ya está creado el archivo de reddit
        if controlador.is_empty():
            controlador.create_db()
        decision = frame.binary_question("¿Desea Programar una nueva publicación?")
        if decision:
            # Si la decision es Afirmativa, se añaden los elementos para programar post
            data = frame.text_question(dbase="programmer")
            # Seleccion de post
            file = frame.choose_element("Seleccionar Post", controlador.get_photos())

            # Subida de elementos a Base de datos
            elements = [None]*7
            elements[0] = file
            for i in range(len(data)): elements[i+1] = data[i]

            controlador.update_programmer(elements)
            # Mensaje de Aviso (Opcional)
            # frame.warning_message("Los datos se han subido correctamente")

    def upvote_dialog(event):
        controlador = ctrl.Controlador()
        if controlador.is_empty():
            controlador.create_db()
        controlador.sorted_data()

        lenght = len(controlador.data)
        upvotes = [int(lenght * 0.25), int(lenght * 0.5), int(lenght* 0.75), int(15)]
        choice = frame.choose_element(f"{lenght} Bots.\nTotal upvotes:",
                                [f"{upvotes[2]}/h --- 20m", f"{upvotes[1]}/h --- 10m", f"{upvotes[0]}/h --- 7m"])

        url = frame.text_question(dbase = None)
        total = int(findall(r'\d+', choice[:4])[0])
        tf = int(findall(r'\d+', choice[3:])[0])
        controlador.upvote(total, url[0], (tf / total) * 60)

    ctrl.makeDir()
    app = wx.App()
    funciones = [(bot_dialog, "Entrar en la Base"),(programmer_dialog, "Base de datos de Publicaciones"),(upvote_dialog, "Upvote a URL")]
    frame = wt.MyFrame(funcs = funciones, titulo = "Base de Datos", subtitulo = "Reddit")
    frame.Show()
    app.MainLoop()

main()