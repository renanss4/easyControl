import tkinter as tk


class TelaGestor(tk.Tk):
    def __init__(self, controlador_gestor):
        super().__init__()
        self.title("Gestor - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")
        self.__controlador_gestor = controlador_gestor

        # Centraliza a janela
        self.transient()
        self.grab_set()

        tk.Label(
            self, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc"
        ).pack(pady=20)

        quadro_botoes = tk.Frame(
            self, bg="#dcdcdc", bd=1, relief="solid", padx=20, pady=20
        )
        quadro_botoes.pack(pady=10)

        tk.Button(
            quadro_botoes,
            text="Analisar Solicitação",
            width=25,
            height=2,
            command=self.aprovar_solicitacao,
        ).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(
            quadro_botoes,
            text="Consultar Colaboradores",
            width=25,
            height=2,
            command=self.consultar_lista_colaboradores,
        ).grid(row=0, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(rodape, text="Sair", width=20, height=2, command=self.sair).grid(
            row=0, column=0, padx=20
        )

    def sair(self):
        confirm = tk.messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            pass

    # UC03
    def abrir_tela_analisar_solicitacao(self):
        pass

    # UC02
    def consultar_lista_colaboradores(self):
        # para o gestor, vai só a consulta mesmo
        tk.messagebox.showinfo(
            "Consultar listagem de colaboradores",
            "Funcionalidade consultar listagem de colaboradores ainda não implementada.",
        )

    def voltar(self):
        pass
