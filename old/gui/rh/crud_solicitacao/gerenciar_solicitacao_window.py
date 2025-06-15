import tkinter as tk
from tkinter import ttk, messagebox
from controllers.solicitacao_controller import (
    buscar_solicitacoes_por_cpf,
    cancelar_solicitacao,
    obter_solicitacoes_detalhadas
)
from controllers.colaborador_controller import buscar_colaborador_por_cpf
from controllers.usuario_controller import buscar_usuario_por_cpf
from utils.check_data import valida_todos_dados

class GerenciaSolicitacoesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciar Solicitações - EasyControl")
        self.geometry("1200x700")
        self.configure(bg="#dcdcdc")
        self.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            search_frame, 
            text="CPF do colaborador:", 
            bg="#dcdcdc",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=(0, 10))
        
        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="Buscar",
            command=self.buscar_solicitacoes
        ).pack(side="left")
        
        tk.Button(
            search_frame,
            text="Mostrar Todas",
            command=self.mostrar_todas_solicitacoes
        ).pack(side="left", padx=10)
        
        # Frame da tabela
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar Treeview
        self.tree = ttk.Treeview(
            table_frame, 
            columns=("protocolo", "nome", "cpf", "data_solicitacao", "periodos", "status"),
            show="headings",
            selectmode="browse"
        )

        # Configurar colunas
        self.tree.heading("protocolo", text="Protocolo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("data_solicitacao", text="Data Solicitação")
        self.tree.heading("periodos", text="Períodos")
        self.tree.heading("status", text="Status")

        self.tree.column("protocolo", width=150)
        self.tree.column("nome", width=200)
        self.tree.column("cpf", width=120)
        self.tree.column("data_solicitacao", width=120)
        self.tree.column("periodos", width=300)
        self.tree.column("status", width=100)

        # Adicionar scrollbars
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=20)
        
        self.btn_cancelar = tk.Button(
            botoes_frame,
            text="Cancelar Solicitação",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.cancelar_solicitacao,
            state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar
        ).pack(side="left", padx=5)

        # Bind para seleção na tabela
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Carregar dados iniciais
        self.mostrar_todas_solicitacoes()
        
        # Armazenar protocolo selecionado
        self.protocolo_selecionado = None
    
    def formatar_periodos(self, solicitacao):
        """Formata os períodos de uma solicitação para exibição"""
        if "periodos" in solicitacao:
            periodos = solicitacao["periodos"]
            return " | ".join(
                f"{p['data_inicio']} a {p['data_fim']}"
                for p in periodos
            )
        return f"{solicitacao['data_inicio']} a {solicitacao['data_fim']}"
    
    def on_select(self, event):
        """Callback quando uma linha é selecionada na tabela"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            status = item['values'][5]
            self.btn_cancelar.config(
                state="normal" if status == "pendente" else "disabled"
            )
        else:
            self.btn_cancelar.config(state="disabled")
    
    def mostrar_todas_solicitacoes(self):
        """Exibe todas as solicitações na tabela"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        solicitacoes = obter_solicitacoes_detalhadas()
        
        for sol in solicitacoes:
            periodos = self.formatar_periodos(sol)
            self.tree.insert(
                "",
                "end",
                values=(
                    sol["protocolo"],
                    sol["nome_colaborador"],
                    sol["cpf_colaborador"],
                    sol["data_solicitacao"],
                    periodos,
                    sol["status"]
                )
            )
    
    def buscar_solicitacoes(self):
        """Busca e exibe solicitações de um colaborador específico"""
        cpf = self.cpf_entry.get().strip()
        
        # Validar CPF
        sucesso, mensagem = valida_todos_dados(cpf=cpf)
        if not sucesso:
            messagebox.showerror("Erro", mensagem)
            return
            
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Buscar solicitações
        solicitacoes = buscar_solicitacoes_por_cpf(cpf)
        
        if solicitacoes:
            # Buscar informações do colaborador e usuário
            colaborador = buscar_colaborador_por_cpf(cpf)
            usuario = buscar_usuario_por_cpf(cpf)
            
            # Determinar o nome a ser exibido
            nome_exibicao = None
            if colaborador:
                nome_exibicao = colaborador.nome
            if usuario:
                nome_exibicao = usuario.nome if not nome_exibicao else nome_exibicao
            
            if not nome_exibicao:
                nome_exibicao = "Nome não encontrado"
            
            for sol in solicitacoes:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        sol["protocolo"],
                        nome_exibicao,
                        sol["cpf_colaborador"],
                        sol["data_solicitacao"],
                        sol.get("periodos_formatados", "N/A"),  # Usando o novo campo formatado
                        sol["status"]
                    )
                )
        else:
            messagebox.showinfo("Info", "Nenhuma solicitação encontrada para este CPF.")
    
    def cancelar_solicitacao(self):
        """Cancela a solicitação selecionada"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        protocolo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Deseja realmente cancelar esta solicitação?"):
            if cancelar_solicitacao(protocolo):
                messagebox.showinfo("Sucesso", "Solicitação cancelada com sucesso!")
                self.mostrar_todas_solicitacoes()
            else:
                messagebox.showerror("Erro", "Não foi possível cancelar a solicitação.")

    def voltar(self):
        self.destroy()
        from gui.rh.cadastrar_solicitacao_window import CadastraSolicitacaoWindow
        CadastraSolicitacaoWindow().mainloop()

if __name__ == "__main__":
    app = GerenciaSolicitacoesWindow()
    app.mainloop()