import tkinter as tk


class TelaEquipe(tk.Tk):
    def __init__(self, controlador_equipe):
        super().__init__()
        self.title("Equipe - EasyControl")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.controlador_equipe = controlador_equipe

        # Centraliza a janela
        self.transient()
        self.grab_set()

        # Exemplo de conteúdo
        tk.Label(self, text="Área da Equipe", font=("Arial", 16), bg="#f0f0f0").pack(
            pady=20
        )
