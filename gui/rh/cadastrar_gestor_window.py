import tkinter as tk

class CadastraGestorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Gestor - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")