import tkinter as tk


class PrincipalGestorWindow(tk.Tk):
    def __init__(self, cpf_gestor=None):
        super().__init__()
        
        # Armazenar o CPF do usuário logado
        self.cpf_gestor = cpf_gestor

        self.title("Principal Gestor - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")

        tk.Label(self, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc").pack(pady=20)

        quadro_botoes = tk.Frame(self, bg="#dcdcdc", bd=1, relief="solid", padx=20, pady=20)
        quadro_botoes.pack(pady=10)

        tk.Button(
            quadro_botoes, text="Analisar Solicitação", width=25, height=2, command=self.aprovar_solicitacao
        ).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes, text="Consultar Colaboradores", width=25, height=2, command=self.consultar_lista_colaboradores
        ).grid(row=0, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(
            rodape, text="Sair", width=20, height=2, command=self.sair
        ).grid(row=0, column=0, padx=20)

    def sair(self):
        confirm = tk.messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()
            from gui.login_window import LoginWindow
            LoginWindow().mainloop()

    # UC03
    def aprovar_solicitacao(self, event=None):
        self.destroy()
        from gui.gestor.analisar_solicitacao_window import AnalisarSolicitacaoWindow
        AnalisarSolicitacaoWindow(self.cpf_gestor).mainloop()

    # UC02
    def consultar_lista_colaboradores(self, event=None):
        # para o gestor, vai só a consulta mesmo
        tk.messagebox.showinfo("Consultar listagem de colaboradores", "Funcionalidade consultar listagem de colaboradores ainda não implementada.")

    
    def voltar(self):
        self.destroy()
        from gui.gestor.principal_gestor_window import PrincipalGestorWindow
        PrincipalGestorWindow().mainloop()
