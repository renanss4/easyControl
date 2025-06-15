import tkinter as tk

class ConsultaListaColaboradoresWindow(tk.Tk):
    def __init__(self, cpf_gestor):
        super().__init__()
        self.title("Consulta da lista de Colaboradores - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        self.cpf_gestor = cpf_gestor