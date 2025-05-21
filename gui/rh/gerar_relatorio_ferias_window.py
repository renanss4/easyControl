import tkinter as tk

class GeraRelatorioFeriasWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerar Relatório de Férias - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")