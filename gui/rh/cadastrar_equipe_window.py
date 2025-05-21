import tkinter as tk

class CadastraEquipeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Equipe - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")