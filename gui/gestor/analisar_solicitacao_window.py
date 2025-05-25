import tkinter as tk
from tkinter import ttk, messagebox
from controllers.solicitacao_controller import (
    buscar_solicitacoes_por_cpf,
    obter_solicitacoes,
    obter_solicitacoes_detalhadas,
    aprovar_solicitacao as aprovar_sol,
    rejeitar_solicitacao as rejeitar_sol
)
from controllers.equipe_controller import listar_equipes, listar_colaboradores_equipe
from controllers.usuario_controller import _carregar_usuarios


class AnalisarSolicitacaoWindow(tk.Tk):
    def __init__(self, cpf_gestor=None):
        super().__init__()
        self.cpf_gestor = cpf_gestor
        
        # Obter informações da equipe do gestor
        self.equipe_gestor = self.obter_equipe_do_gestor()
        
        # Configurações da janela
        self.title("Analisar Solicitação")
        self.geometry("700x500")
        self.configure(bg="#dcdcdc")
        self.resizable(True, True)
        
        # Frame de busca
        busca_frame = tk.Frame(self, bg="#dcdcdc", padx=10, pady=10)
        busca_frame.pack(fill="x")
        
        tk.Label(busca_frame, text="CPF do Colaborador", bg="#dcdcdc").pack(side="left", padx=5)
        self.cpf_entry = tk.Entry(busca_frame, width=15)
        self.cpf_entry.pack(side="left", padx=5)
        
        tk.Button(
            busca_frame, 
            text="Buscar", 
            command=self.buscar_solicitacoes
        ).pack(side="left", padx=5)
        
        tk.Button(
            busca_frame,
            text="Mostrar Todos",
            command=self.mostrar_todas_solicitacoes
        ).pack(side="left", padx=5)
        
        # Frame da tabela
        tabela_frame = tk.Frame(self, padx=10)
        tabela_frame.pack(fill="both", expand=True)
        
        # Criar tabela de solicitações
        colunas = ('protocolo', 'nome', 'cpf', 'data_solicitacao', 'periodos', 'status')
        self.tabela = ttk.Treeview(tabela_frame, columns=colunas, show='headings', selectmode='browse')
        
        # Definir cabeçalhos
        self.tabela.heading('protocolo', text='Protocolo')
        self.tabela.heading('nome', text='Nome')
        self.tabela.heading('cpf', text='CPF')
        self.tabela.heading('data_solicitacao', text='Data Solicitação')
        self.tabela.heading('periodos', text='Períodos')
        self.tabela.heading('status', text='Status')
        
        # Definir larguras das colunas
        self.tabela.column('protocolo', width=120)
        self.tabela.column('nome', width=150)
        self.tabela.column('cpf', width=100)
        self.tabela.column('data_solicitacao', width=100)
        self.tabela.column('periodos', width=180)
        self.tabela.column('status', width=80)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)
        
        # Vincular evento de seleção
        self.tabela.bind('<<TreeviewSelect>>', self.selecionar_solicitacao)
        
        # Frame para informações da equipe
        info_equipe_frame = tk.Frame(self, bg="#dcdcdc", padx=10, pady=10, relief="groove", bd=1)
        info_equipe_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_equipe_label = tk.Label(
            info_equipe_frame, 
            text="Carregando informações da equipe...",
            bg="#dcdcdc",
            font=("Arial", 11, "bold")
        )
        self.info_equipe_label.pack(pady=10)
        
        # Frame dos botões de ação
        acoes_frame = tk.Frame(self, bg="#dcdcdc", padx=10, pady=10)
        acoes_frame.pack(fill="x")
        
        self.btn_aprovar = tk.Button(
            acoes_frame,
            text="Aprovar solicitação",
            command=self.aprovar_solicitacao,
            state="disabled"
        )
        self.btn_aprovar.pack(side="left", padx=10)
        
        tk.Button(
            acoes_frame,
            text="Voltar",
            command=self.voltar
        ).pack(side="left", padx=10)
        
        self.btn_reprovar = tk.Button(
            acoes_frame,
            text="Reprovar Solicitação",
            command=self.reprovar_solicitacao,
            state="disabled"
        )
        self.btn_reprovar.pack(side="left", padx=10)
        
        # Atualizar o label com a porcentagem da equipe em férias
        self.atualizar_porcentagem_equipe()
        
        # Carregar solicitações ao iniciar
        self.mostrar_todas_solicitacoes()
    
    def obter_equipe_do_gestor(self):
        equipes = listar_equipes()
        for equipe in equipes:
            if equipe.gestor_cpf == self.cpf_gestor:
                return equipe.nome
    
    def obter_membros_da_equipe(self):
        """Retorna uma lista de CPFs dos membros da equipe do gestor"""
        if not self.equipe_gestor:
            return []
            
        colaboradores = listar_colaboradores_equipe(self.equipe_gestor)
        
        return colaboradores
    
    def calcular_porcentagem_equipe_ferias(self):
        """Calcula a porcentagem de membros da equipe que estão de férias"""
        if not self.equipe_gestor:
            return 0
            
        # Obter CPFs dos membros da equipe
        membros_cpf = self.obter_membros_da_equipe()
        
        if not membros_cpf:
            return 0
            
        # Obter todas as solicitações aprovadas
        solicitacoes = obter_solicitacoes()
        membros_em_ferias = set()
        
        for sol in solicitacoes:
            if sol.get("status") == "aprovado" and sol.get("cpf_colaborador") in membros_cpf:
                membros_em_ferias.add(sol.get("cpf_colaborador"))
        
        # Calcular porcentagem
        porcentagem = (len(membros_em_ferias) / len(membros_cpf)) * 100
        return int(porcentagem)
    
    def atualizar_porcentagem_equipe(self):
        """Atualiza o texto do label com a porcentagem da equipe em férias"""
        porcentagem = self.calcular_porcentagem_equipe_ferias()
        
        if not self.equipe_gestor:
            self.info_equipe_label.config(text="Não foi possível obter informações da equipe.")
        else:
            self.info_equipe_label.config(
                text=f"A sua equipe atualmente está com {porcentagem}% dos Colaboradores de férias!!"
            )
    
    def buscar_solicitacoes(self):
        cpf = self.cpf_entry.get().strip()
        
            
        # Verificar se o colaborador é da equipe do gestor
        if not self.verificar_colaborador_na_equipe(cpf):
            messagebox.showwarning("Aviso", "Este colaborador não pertence à sua equipe.")
            return
            
        self.limpar_tabela()
        solicitacoes = buscar_solicitacoes_por_cpf(cpf)
        self.preencher_tabela(solicitacoes)
    
    def verificar_colaborador_na_equipe(self, cpf):
        """Verifica se um colaborador pertence à equipe do gestor"""
        if not self.equipe_gestor:
            return False
            
        membros_cpf = self.obter_membros_da_equipe()
        return cpf in membros_cpf
    
    def mostrar_todas_solicitacoes(self):
        """Mostra apenas as solicitações dos membros da equipe do gestor"""
        # self.limpar_tabela()
        if not self.equipe_gestor:
            messagebox.showinfo("Informação", "Não foi possível identificar sua equipe.")
            return
        
        # Obter CPFs dos membros da equipe
        membros_cpf = self.obter_membros_da_equipe()
        
        if not membros_cpf:
            messagebox.showinfo("Informação", "Não há colaboradores na sua equipe.")
            return
        
        # Obter todas as solicitações
        todas_solicitacoes = obter_solicitacoes_detalhadas()
        
        # Filtrar apenas solicitações da equipe
        solicitacoes_equipe = [s for s in todas_solicitacoes if s.get("cpf_colaborador") in membros_cpf]
        
        self.preencher_tabela(solicitacoes_equipe)
    
    def preencher_tabela(self, solicitacoes):
        self.limpar_tabela()
        for sol in solicitacoes:
            # Para solicitações que usam o formato de períodos
            if "periodos" in sol and isinstance(sol["periodos"], list):
                periodos_texto = " | ".join([
                    f"{p.get('data_inicio', 'N/A')} a {p.get('data_fim', 'N/A')}" 
                    for p in sol.get("periodos", [])
                ])
            else:
                # Para formato antigo com data_inicio e data_fim diretamente
                periodos_texto = f"{sol.get('data_inicio', 'N/A')} a {sol.get('data_fim', 'N/A')}"
            
            # Corrigindo o problema da tag - primeiro verificar se status existe
            status = sol.get("status", "")
            
            self.tabela.insert(
                "", 
                "end", 
                values=(
                    sol.get("protocolo", ""),
                    sol.get("nome_colaborador", ""),
                    sol.get("cpf_colaborador", ""),
                    sol.get("data_solicitacao", ""),
                    periodos_texto,
                    status
                ),
                tags=(status,) if status else ()  # Corrigido para passar uma tupla vazia se não houver status
            )
        
        # Configurar cores para status
        self.tabela.tag_configure("pendente", background="#FFFFCC")
        self.tabela.tag_configure("aprovado", background="#CCFFCC")
        self.tabela.tag_configure("rejeitado", background="#FFCCCC")
        self.tabela.tag_configure("cancelada", background="#E0E0E0")
    
    def limpar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
    
    def selecionar_solicitacao(self, event):
        """Ação ao selecionar uma solicitação na tabela"""
        selecionados = self.tabela.selection()
        
        if selecionados:
            item = self.tabela.item(selecionados[0])
            status = item['values'][5]
            
            # Habilitar/desabilitar botões com base no status
            if status == "pendente":
                self.btn_aprovar.config(state="normal")
                self.btn_reprovar.config(state="normal")
            else:
                self.btn_aprovar.config(state="disabled")
                self.btn_reprovar.config(state="disabled")
    
    def aprovar_solicitacao(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            return
            
        item = self.tabela.item(selecionados[0])
        protocolo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Deseja realmente APROVAR esta solicitação de férias?"):
            if aprovar_sol(protocolo):
                messagebox.showinfo("Sucesso", "Solicitação aprovada com sucesso!")
                self.mostrar_todas_solicitacoes()
                self.atualizar_porcentagem_equipe()  # Atualiza a porcentagem após aprovar
            else:
                messagebox.showerror("Erro", "Não foi possível aprovar a solicitação.")
    
    def reprovar_solicitacao(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            return
            
        item = self.tabela.item(selecionados[0])
        protocolo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "Deseja realmente REPROVAR esta solicitação de férias?"):
            if rejeitar_sol(protocolo):
                messagebox.showinfo("Sucesso", "Solicitação reprovada com sucesso!")
                self.mostrar_todas_solicitacoes()
            else:
                messagebox.showerror("Erro", "Não foi possível reprovar a solicitação.")
    
    def voltar(self):
        self.destroy()