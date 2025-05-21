import tkinter as tk
from tkinter import messagebox


class MainWindow(tk.Tk):
    def __init__(self, tela_anterior=None):
        super().__init__()
        self.tela_anterior = tela_anterior

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
            from gui.login_window import LoginWindow
            LoginWindow().mainloop()

    # UC03
    def aprovar_solicitacao(self, event=None):
        # nessa tela não vai só a aprovação, mas também a consulta, a reprovação etc
        messagebox.showinfo("Aprovar solicitação de férias", "Funcionalidade aprovar solicitação de férias ainda não implementada.")

    # UC02
    def consultar_lista_colaboradores(self, event=None):
        # para o gestor, vai só a consulta mesmo
        messagebox.showinfo("Consultar listagem de colaboradores", "Funcionalidade consultar listagem de colaboradores ainda não implementada.")