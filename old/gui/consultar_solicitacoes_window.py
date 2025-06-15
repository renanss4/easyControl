import tkinter as tk
from tkinter import ttk
from controllers.solicitacao_controller import obter_solicitacoes_detalhadas

class ConsultaSolicitacoesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta de Solicitações - EasyControl")
        self.configure(bg="#dcdcdc")
        self.geometry("900x600")
