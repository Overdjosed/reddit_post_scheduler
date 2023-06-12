
import wx



class MyDialog(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        # Botones usados para borrar la pantalla de dialogo
        self._buttons = []
        # Eleccion de elemento
        self._selected = None

    def __insert_in_button_sizer(self, b_sizer, button):
        # Adicion de boton generico a sizer
        b_sizer.Add(button, 0, wx.ALL, 10)
        self._buttons.append(button)
        return b_sizer

    def __create_button(self, label = "Sí", button_sizer = None):

        if label == "Sí":
            button = wx.Button(self, label = label)

            # Asignación de Funciones de Botones
            button.Bind(wx.EVT_BUTTON, self.on_yes)

        elif label == "No":
            button = wx.Button(self, label = label)
            button.Bind(wx.EVT_BUTTON, self.on_no)

        else:
            button = wx.Button(self, label = label)
            button.Bind(wx.EVT_BUTTON, self.on_button_click)

        if not button_sizer:
            # Creacion de Button Sizer
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            button_sizer.AddStretchSpacer()

        # Añade botones al sizer y a lista de botones por eliminar
        button_sizer = self.__insert_in_button_sizer(button_sizer, button)
        return button_sizer


    def Binary_question(self, question):
        sizer = wx.BoxSizer(wx.VERTICAL)
        question_label = wx.StaticText(self, label = question)

        self._buttons.append(question_label)
        sizer.Add(question_label, 0, wx.ALL, 10)

        # Botones y textos de Botones
        button_sizer = self.__create_button()
        button_sizer = self.__create_button(label="No", button_sizer = button_sizer)

        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)
        self._buttons.append(button_sizer)
        self.SetSizerAndFit(sizer)

    def __text_label (self,sizer, label_text):
        # Funcion genérica que crea elementos para insertar texto
        label_t = wx.StaticText(self, label = label_text , style=wx.ALIGN_CENTER)
        sizer.Add(label_t, 0, wx.ALL, 3)
        user_input = wx.TextCtrl(self, size = (400,20))
        sizer.Add(user_input, 0, wx.EXPAND | wx.ALL, 3)
        self._buttons.append(label_t)
        self._buttons.append(user_input)
        return user_input

    def warning(self, text, size = 10, type_ = "Normal"):
        # Funcion que muestra texto de aviso en pantalla
        sizer = wx.BoxSizer(wx.VERTICAL)
        warning_label = wx.StaticText(self, label=text)

        # Titulo: Color and Font
        if type_.lower() == "title":
            font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            warning_label.SetFont(font)
            warning_label.SetForegroundColour(wx.Colour(255, 0, 0))  # Cambiar el color del texto a rojo

        sizer.Add(warning_label, 0, wx.ALL, size)
        self._buttons.append(warning_label)

        yes_button = wx.Button(self, label="Aceptar")
        yes_button.Bind(wx.EVT_BUTTON, self.on_yes)
        sizer.Add(yes_button, 0, wx.ALIGN_CENTER)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        self._buttons.append(yes_button)
        self._buttons.append(button_sizer)
        self.SetSizerAndFit(sizer)

    def text_question(self, database="bots"):
        sizer = wx.BoxSizer(wx.VERTICAL)

        output = []
        if database == "bots":
            # Argumentos de Método praw
            for element in ["identificador:", "idCliente:", "ClientSecret:", "UserAgent:", "Password:", "Username:"]:
                output.append(self.__text_label(sizer, element))

        elif database == "programmer":
            # Argumentos para subir posts a Reddit
            for element in ["Subreddit:", "Title:", "Url:", "Date:", "Hour:", "Minute:"]:
                output.append(self.__text_label(sizer, element))

        elif database == None:
            output.append(self.__text_label(sizer, "Url:"))

        # Creacion y adición de boton de aceptar
        yes_button = wx.Button(self, label="Aceptar")
        yes_button.Bind(wx.EVT_BUTTON, self.on_yes)
        sizer.Add(yes_button, 0, wx.ALIGN_CENTER)
        self._buttons.append(yes_button)

        self.SetSizerAndFit(sizer, deleteOld= False)
        return output

    def choose_element(self, question, elements):
        # Eleccion de elementos por su nombre o texto

        sizer = wx.BoxSizer(wx.VERTICAL)
        question_label = wx.StaticText(self, label = question, size = (100, 30))
        sizer.Add(question_label, 0, wx.ALIGN_CENTER, 3)
        button_sizer = None

        # Creacion de botones con ayuda de función generica
        for element in elements:
            button_sizer = self.__create_button(element, button_sizer)

        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)
        self._buttons.append(button_sizer)
        self._buttons.append(question_label)
        self.SetSizerAndFit(sizer)


    def clear_window(self):
        # Limpiar la lista de botones, por consiguiente, limpia la ventana de dialogo
        for button in self._buttons:
            button.Destroy()
        self._buttons = []

    def on_yes(self, event):
        # Boton Afirmativo
        self._selected = True
        self.EndModal(wx.ID_YES)

    def on_button_click(self, event):
        # Boton de eleccion por elemento
        button = event.GetEventObject()
        self._selected = button.GetLabel()
        self.EndModal(wx.ID_YES)

    @property
    def selected(self):
        # Muestreo de seleccion de elemento
        return self._selected

    def on_no(self, event):
        # Botón Negativo
        self._selected = False
        self.EndModal(wx.ID_NO)

class MyFrame(wx.Frame):

    def __init__(self, funcs = None, titulo = "Base de Datos", subtitulo = "Reddit"):
        # Ventana con título
        super().__init__(None, title= titulo)
        # Ventana sin título en constante reutilizacion
        self.dialog = MyDialog(self, title=subtitulo)
        panel = wx.Panel(self)

        button_sizer = wx.BoxSizer(wx.VERTICAL)

        for element in funcs:
        # Creación de ventanas principales mediante botones
            button = wx.Button(panel, label=element[1])
            button.Bind(wx.EVT_BUTTON, element[0])
            button_sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 10)

        button_sizer.AddStretchSpacer()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        panel.SetSizer(sizer)

    def warning_message(self, text, size = 10, type = "Normal"):
        # Creacion de ventana aviso desde Panel principal
        self.dialog.warning(text, size, type)
        self.dialog.ShowModal()
        self.dialog.clear_window()

    def binary_question(self, quest):
        # Creacion de ventana de respuesta Booleana desde Panel principal
        self.dialog.Binary_question(question = quest)
        result = self.dialog.ShowModal()
        self.dialog.clear_window()
        return result == wx.ID_YES

    def choose_element(self, question, elems):
        # Creacion de ventana de respuesta mediante eleccion de elementos
        self.dialog.choose_element(question, elements = elems)
        self.dialog.ShowModal()
        self.dialog.clear_window()
        return self.dialog.selected

    def text_question(self, dbase = "bots"):
        # Creacion de ventana de insercion de textos según la base de datos
        result = self.dialog.text_question(database = dbase)
        output = None
        self.dialog.ShowModal()
        if self.dialog.selected == True:
            output = [element.GetValue() for element in result]
        self.dialog.clear_window()
        return output
