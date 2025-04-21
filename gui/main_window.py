import tkinter as tk
from tkinter import messagebox

from gui.cadastro_rh_window import CadastroRHWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Home - EasyControl")
        self.geometry("700x600")
        self.configure(bg="#dcdcdc")

        tk.Label(self, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc").pack(pady=20)

        quadro_botoes = tk.Frame(self, bg="#dcdcdc", bd=1, relief="solid", padx=20, pady=20)
        quadro_botoes.pack(pady=10)

        tk.Button(
            quadro_botoes, text="Cadastrar Colaborador", width=25, height=2, command=self.cadastrar_colaborador
        ).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes, text="Cadastrar Gestor", width=25, height=2, command=self.cadastrar_gestor
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            quadro_botoes, text="Cadastrar Funcionário RH", width=25, height=2, command=self.cadastrar_funcionario_rh
        ).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes, text="Registro de Solicitações", width=25, height=2, command=self.registrar_solicitacoes
        ).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            quadro_botoes, text="Consultar Solicitações", width=25, height=2, command=self.consultar_solicitacoes
        ).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes, text="Gerar Relatório de Férias", width=25, height=2, command=self.gerar_relatorio_ferias
        ).grid(row=2, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(
            rodape, text="Sair", width=20, height=2, command=self.sair
        ).grid(row=0, column=0, padx=20)
        tk.Button(
            rodape, text="Calendário", width=20, height=2, command=self.abrir_calendario
        ).grid(row=0, column=1, padx=20)

    def sair(self):
        confirm = messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()

    def cadastrar_colaborador(self, event=None):
        messagebox.showinfo("Cadastro colaborador", "Funcionalidade cadastro de colaborador ainda não implementada.")

    def cadastrar_gestor(self, event=None):
        messagebox.showinfo("Cadastro gestor", "Funcionalidade cadastro de gestor ainda não implementada.")

    def cadastrar_funcionario_rh(self, event=None):
        CadastroRHWindow()

    def registrar_solicitacoes(self, event=None):
        messagebox.showinfo("Registro de solicitações", "Funcionalidade registro de solicitações ainda não implementada.")

    def consultar_solicitacoes(self, event=None):
        messagebox.showinfo("Consultar solicitações", "Funcionalidade consultar solicitações ainda não implementada.")

    def gerar_relatorio_ferias(self, event=None):
        messagebox.showinfo("Gerar relatório de férias", "Funcionalidade gerar relatório de férias ainda não implementada.")

    def abrir_calendario(self, event=None):
        messagebox.showinfo("Calendário", "Funcionalidade calendário ainda não implementada.")
