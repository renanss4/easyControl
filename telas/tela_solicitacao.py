import tkinter as tk


class TelaSolicitacao(tk.Tk):
    def __init__(self, controlador_solicitacao):
        super().__init__()
        self.title("Solicitação - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#f0f0f0")
        self.__controlador_solicitacao = controlador_solicitacao

        # Centraliza a janela
        self.transient()
        self.grab_set()

        # Exemplo de conteúdo
        tk.Label(
            self, text="Área de Solicitação", font=("Arial", 16), bg="#f0f0f0"
        ).pack(pady=20)
