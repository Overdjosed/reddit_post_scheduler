import gui as wt
import controller as ctrl
import wx

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

    ctrl.makeDir()
    app = wx.App()
    frame = wt.MyFrame(bot_dialog, programmer_dialog,"Base de Datos", "Reddit")
    frame.Show()
    app.MainLoop()

main()