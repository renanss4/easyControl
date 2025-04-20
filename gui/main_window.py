import tkinter as tk
from tkinter import messagebox

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Home - EasyControl")
        self.geometry("600x500")
        self.configure(bg="#dcdcdc")

        # Barra de título azul (mas acho desnecessário)
        barra_superior = tk.Frame(self, bg="blue", height=30)
        barra_superior.pack(fill="x")
        tk.Label(barra_superior, text="Home", fg="white", bg="blue", font=("Arial", 10, "bold"), padx=10).pack(side="left", anchor="w")

        tk.Label(self, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc").pack(pady=20)

        quadro_botoes = tk.Frame(self, bg="#dcdcdc", bd=1, relief="solid", padx=20, pady=20)
        quadro_botoes.pack(pady=10)

        tk.Button(quadro_botoes, text="Cadastrar Colaborador", width=25, height=2).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(quadro_botoes, text="Cadastrar Gestor", width=25, height=2).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(quadro_botoes, text="Cadastrar Funcionário RH", width=25, height=2).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(quadro_botoes, text="Registro de Solicitações", width=25, height=2).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(quadro_botoes, text="Consultar Solicitações", width=25, height=2).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(quadro_botoes, text="Gerar Relatório de Férias", width=25, height=2).grid(row=2, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(rodape, text="Sair", width=20, height=2, command=self.sair).grid(row=0, column=0, padx=20)
        tk.Button(rodape, text="Calendário", width=20, height=2).grid(row=0, column=1, padx=20)

    def sair(self):
        confirm = messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()
