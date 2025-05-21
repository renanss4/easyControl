import tkinter as tk

class ConsultaListaColaboradoresWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta da lista de Colaboradores - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")