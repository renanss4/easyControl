import tkinter as tk
from tkinter import ttk
from controllers.solicitacao_controller import obter_solicitacoes_detalhadas

class ConsultaSolicitacoesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta de Solicitações - EasyControl")
        self.configure(bg="#dcdcdc")
        self.geometry("900x600")

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(
            main_frame,
            text="Solicitações de Férias",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc"
        ).pack(pady=15)

        # Frame para a tabela
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar Treeview
        self.tree = ttk.Treeview(table_frame, columns=(
            "protocolo", "nome", "cpf", "data_inicio", "data_fim", "status", "data_solicitacao"
        ), show="headings")

        # Definir cabeçalhos
        self.tree.heading("protocolo", text="Protocolo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("data_inicio", text="Data Início")
        self.tree.heading("data_fim", text="Data Fim")
        self.tree.heading("status", text="Status")
        self.tree.heading("data_solicitacao", text="Data Solicitação")

        # Configurar colunas
        self.tree.column("protocolo", width=150)
        self.tree.column("nome", width=200)
        self.tree.column("cpf", width=100)
        self.tree.column("data_inicio", width=100)
        self.tree.column("data_fim", width=100)
        self.tree.column("status", width=100)
        self.tree.column("data_solicitacao", width=100)

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Posicionar elementos
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botão de atualizar
        tk.Button(
            main_frame,
            text="Atualizar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.carregar_solicitacoes
        ).pack(pady=10)

        # Botão de voltar
        tk.Button(
            main_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.voltar
        ).pack(pady=5)

        # Carregar dados iniciais
        self.carregar_solicitacoes()

    def carregar_solicitacoes(self):
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Carregar novas solicitações já com datas formatadas
        solicitacoes = obter_solicitacoes_detalhadas()
        
        for solicitacao in solicitacoes:
            self.tree.insert("", "end", values=(
                solicitacao.get('protocolo', 'N/A'),
                solicitacao.get('nome_colaborador', 'N/A'),
                solicitacao.get('cpf_colaborador', 'N/A'),
                solicitacao.get('data_inicio', 'N/A'),
                solicitacao.get('data_fim', 'N/A'),
                solicitacao.get('status', 'N/A'),
                solicitacao.get('data_solicitacao', 'N/A')
            ))

    def voltar(self):
        self.destroy()
        from gui.login_window import LoginWindow
        LoginWindow().mainloop()