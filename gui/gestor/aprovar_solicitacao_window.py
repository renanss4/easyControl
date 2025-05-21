import tkinter as tk

class AprovaSolicitacaoWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aprovação de Solicitações - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")