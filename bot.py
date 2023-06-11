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
        frame.Close()

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
            controlador.update_programmer(file + data)
            # Mensaje de Aviso (Opcional)
            # frame.warning_message("Los datos se han subido correctamente")

        frame.Close()

    def upvote_dialog(event):
        controlador = ctrl.Controlador()
        if controlador.is_empty():
            controlador.create_db()
        controlador.sorted_data()
        lenght = len(controlador.data)
        upvotes = [int(lenght) * 0.25, int(lenght) * 0.5, int(lenght)* 0.75, int(lenght)]
        choice = frame.choose_element(f"{lenght} Bots.\nTotal upvotes:",
                                [f"{upvotes[2]}/h --- 20m", f"{upvotes[1]}/h --- 10m", f"{upvotes[0]}/h --- 7m"])

        url = frame.text_question(dbase = "")
        total = findall(r'\d+', choice[:4])
        tf = findall(r'\d+', choice[3:])
        controlador.upvote(total, url, tf / total)

        frame.close()

    ctrl.makeDir()
    app = wx.App()
    funciones = [(bot_dialog, "Entrar en la Base"),(programmer_dialog, "Base de datos de Publicaciones"),(upvote_dialog, "Upvote a URL")]
    frame = wt.MyFrame(funcs = funciones, titulo = "Base de Datos", subtitulo = "Reddit")
    frame.Show()
    app.MainLoop()

main()