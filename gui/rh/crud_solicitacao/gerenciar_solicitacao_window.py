import tkinter as tk
from tkinter import ttk, messagebox
from controllers.solicitacao_controller import (
    buscar_solicitacoes_por_cpf,
    cancelar_solicitacao
)
from utils.check_data import valida_todos_dados

class GerenciaSolicitacoesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciar Solicitações - EasyControl")
        self.geometry("900x600")
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
            bg="#dcdcdc"
        ).pack(side="left", padx=(0, 10))
        
        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="Buscar",
            command=self.buscar_solicitacoes
        ).pack(side="left")
        
        # Frame da tabela
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar Treeview
        self.tree = ttk.Treeview(
            table_frame, 
            columns=("protocolo", "data_solicitacao", "data_inicio", "data_fim", "status"),
            show="headings"
        )

        # Configurar colunas
        self.tree.heading("protocolo", text="Protocolo")
        self.tree.heading("data_solicitacao", text="Data Solicitação")
        self.tree.heading("data_inicio", text="Data Início")
        self.tree.heading("data_fim", text="Data Fim")
        self.tree.heading("status", text="Status")

        self.tree.column("protocolo", width=150)
        self.tree.column("data_solicitacao", width=150)
        self.tree.column("data_inicio", width=150)
        self.tree.column("data_fim", width=150)
        self.tree.column("status", width=100)

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Posicionar elementos
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=20)
        
        self.btn_cancelar = tk.Button(
            botoes_frame,
            text="Cancelar Solicitação",
            command=self.cancelar_solicitacao,
            state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(
            botoes_frame,
            text="Voltar",
            command=self.voltar
        ).pack(side="left", padx=5)

        # Bind para seleção na tabela
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Armazenar protocolo selecionado
        self.protocolo_selecionado = None
    
    def on_select(self, event):
        """Callback quando uma linha é selecionada na tabela"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.protocolo_selecionado = item['values'][0]
            self.btn_cancelar.config(state="normal")
        else:
            self.protocolo_selecionado = None
            self.btn_cancelar.config(state="disabled")
    
    def buscar_solicitacoes(self):
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
            for sol in solicitacoes:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        sol["protocolo"],
                        sol["data_solicitacao"],
                        sol["data_inicio"],
                        sol["data_fim"],
                        sol["status"]
                    )
                )
        else:
            messagebox.showinfo("Info", "Nenhuma solicitação encontrada para este CPF.")
    
    def cancelar_solicitacao(self):
        if not self.protocolo_selecionado:
            return
            
        if messagebox.askyesno("Confirmar", "Deseja realmente cancelar esta solicitação?"):
            if cancelar_solicitacao(self.protocolo_selecionado):
                messagebox.showinfo("Sucesso", "Solicitação cancelada com sucesso!")
                # Atualizar a tabela
                self.buscar_solicitacoes()
            else:
                messagebox.showerror("Erro", "Não foi possível cancelar a solicitação.")

    def voltar(self):
        self.destroy()
        from gui.rh.cadastrar_solicitacao_window import CadastraSolicitacaoWindow
        CadastraSolicitacaoWindow().mainloop()

if __name__ == "__main__":
    app = GerenciaSolicitacoesWindow()
    app.mainloop()