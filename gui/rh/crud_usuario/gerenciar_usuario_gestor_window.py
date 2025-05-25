import tkinter as tk
from controllers.usuario_controller import (
    buscar_gestor_por_cpf,
    atualizar_usuario,
    excluir_usuario
)
from controllers.equipe_controller import listar_equipes
from utils.check_data import valida_todos_dados

class GerenciaUsuariosGestorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciar Gestores - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        self.resizable(False, False)