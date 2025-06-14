import tkinter as tk
from tkinter import messagebox

from gui.rh.cadastrar_colaborador_window import CadastraColaboradorWindow
from gui.rh.cadastrar_solicitacao_window import CadastraSolicitacaoWindow
from gui.rh.cadastrar_rh_window import CadastraRhWindow
from gui.rh.cadastrar_gestor_window import CadastraGestorWindow

class PrincipalRhWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Principal RH - EasyControl")
        self.geometry("900x600")
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
            quadro_botoes, text="Cadastrar Funcionário RH", width=25, height=2, command=self.cadastrar_rh
        ).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes, text="Cadastrar Solicitações", width=25, height=2, command=self.cadastrar_solicitacao
        ).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            quadro_botoes, text="Cadastrar Equipe", width=25, height=2, command=self.cadastrar_equipe
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
            from gui.login_window import LoginWindow
            LoginWindow().mainloop()


    # UC02
    def consultar_lista_colaboradores(self):
        # vai ser só a consulta mesmo, mostrando tudo e podendo buscar pelo cpf
        messagebox.showinfo("Consultar lista de colaboradores", "Funcionalidade consultar lista de colaboradores ainda não implementada.")

    # UC04
    def cadastrar_colaborador(self, event=None):
        # aqui, quando entra na tela de cadastro, deve ter botões do crud
        self.destroy()
        CadastraColaboradorWindow()

    # UC05
    def cadastrar_gestor(self, event=None):
        # aqui, quando entra na tela de cadastro, deve ter botões do crud
        self.destroy()
        CadastraGestorWindow()

    # UC06
    def cadastrar_rh(self, event=None):
        # aqui, quando entra na tela de cadastro, deve ter botões do crud
        self.destroy()
        CadastraRhWindow()

    # UC07
    def cadastrar_solicitacao(self, event=None):
        # aqui, quando entra na tela de cadastro, deve ter botões do crud
        self.destroy()
        CadastraSolicitacaoWindow()

    # UC08
    def gerar_relatorio_ferias(self, event=None):
        # tem que entender como vai ser a tela
        messagebox.showinfo("Gerar relatório de férias", "Funcionalidade gerar relatório de férias ainda não implementada.")

    # UC10
    def abrir_calendario(self, event=None):
        # só mostra um calendário, para futuras funcionalidades
        messagebox.showinfo("Calendário", "Funcionalidade calendário ainda não implementada.")

    # UC11
    def cadastrar_equipe(self, event=None):
        # aqui, quando entra na tela de cadastro, deve ter botões do crud
        messagebox.showinfo("Cadastro equipe", "Funcionalidade cadastro de equipe ainda não implementada.")
