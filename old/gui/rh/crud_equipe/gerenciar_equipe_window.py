import tkinter as tk
from tkinter import ttk, messagebox
from utils.check_data import valida_todos_dados

class GerenciaSolicitacoesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciar Equipes - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        self.resizable(False, False)