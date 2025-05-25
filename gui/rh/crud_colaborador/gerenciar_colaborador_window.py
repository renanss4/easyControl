import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.colaborador_controller import (
    buscar_colaborador_por_cpf,
    atualizar_colaborador,
    excluir_colaborador
)
from controllers.equipe_controller import listar_equipes
from utils.check_data import valida_todos_dados

class GerenciaColaboradoresWindow(tk.Tk):
    def __init__(self, cpf_usuario_logado=None):
        super().__init__()
        self.cpf_usuario_logado = cpf_usuario_logado
        
        # Configurações da janela
        self.title("Gerenciar Colaboradores - EasyControl")
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
            command=self.buscar_colaborador
        ).pack(side="left")
        
        # Frame dos campos
        self.campos_frame = tk.Frame(main_frame, bg="#dcdcdc")
        self.campos_frame.pack(fill="both", expand=True)
        
        # Criar campos de edição
        self.campos = {}
        self.campos_labels = [
            ("nome", "Nome"),
            ("email", "Email"),
            ("cargo", "Cargo"),
        ]
        
        for campo_id, label in self.campos_labels:
            tk.Label(
                self.campos_frame,
                text=label,
                bg="#dcdcdc"
            ).pack(anchor="w", pady=(5, 0))
            
            entry = tk.Entry(self.campos_frame, width=40)
            entry.pack(pady=(0, 10))
            entry.config(state="disabled")
            self.campos[campo_id] = entry
            
        # Campo de data_admissao
        tk.Label(
            self.campos_frame,
            text="Data de Admissão",
            bg="#dcdcdc"
        ).pack(anchor="w", pady=(5, 0))
        
        self.data_admissao = DateEntry(
            self.campos_frame,
            width=37,
            state="disabled",
            date_pattern="yyyy-mm-dd"
        )
        self.data_admissao.pack(pady=(0, 10))
            
        # Campo de equipe com Combobox
        tk.Label(
            self.campos_frame,
            text="Equipe",
            bg="#dcdcdc"
        ).pack(anchor="w", pady=(5, 0))
        
        self.equipe_combo = ttk.Combobox(
            self.campos_frame,
            width=37,
            state="disabled"
        )
        self.equipe_combo.pack(pady=(0, 10))
        
        # Carregar as equipes disponíveis
        self.carregar_equipes()
        
        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=20)
        
        self.btn_editar = tk.Button(
            botoes_frame,
            text="Salvar Alterações",
            command=self.salvar_edicao,
            state="disabled"
        )
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_excluir = tk.Button(
            botoes_frame,
            text="Excluir Colaborador",
            command=self.excluir_colaborador,
            state="disabled"
        )
        self.btn_excluir.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(
            botoes_frame,
            text="Voltar",
            command=self.voltar
        ).pack(side="left", padx=5)
        
        # Botão Gerenciar Usuário Gestor
        tk.Button(
            botoes_frame,
            text="Gerenciar Usuário Gestor",
            command=self.gerenciar_usuario_gestor
        ).pack(side="left", padx=5)
        
        # Armazenar CPF do colaborador atual
        self.cpf_atual = None
        
    def carregar_equipes(self):
        """Carrega apenas as equipes do usuário logado no Combobox"""
        from controllers.equipe_controller import obter_equipes_por_usuario
        
        if hasattr(self, 'cpf_usuario_logado') and self.cpf_usuario_logado:
            equipes = obter_equipes_por_usuario(self.cpf_usuario_logado)
        else:
            from controllers.equipe_controller import listar_equipes
            equipes = listar_equipes()
        
        nomes_equipes = [equipe.nome for equipe in equipes]
        self.equipe_combo['values'] = nomes_equipes
    
    def buscar_colaborador(self):
        cpf = self.cpf_entry.get().strip()
        
        # Validar CPF
        sucesso, mensagem = valida_todos_dados(cpf=cpf)
        if not sucesso:
            messagebox.showerror("Erro", mensagem)
            return
            
        colaborador = buscar_colaborador_por_cpf(cpf)
        
        if colaborador:
            # Armazenar CPF do colaborador encontrado
            self.cpf_atual = cpf
            
            # Habilitar campos
            for campo in self.campos.values():
                campo.config(state="normal")
            self.data_admissao.config(state="normal")
            self.equipe_combo.config(state="readonly")
            
            # Preencher campos
            self.campos["nome"].delete(0, tk.END)
            self.campos["nome"].insert(0, colaborador.nome)
            
            self.campos["email"].delete(0, tk.END)
            self.campos["email"].insert(0, colaborador.email)
            
            self.campos["cargo"].delete(0, tk.END)
            self.campos["cargo"].insert(0, colaborador.cargo)
            
            # Setar data de admissão
            self.data_admissao.set_date(colaborador.data_admissao)
            
            # Setar equipe
            self.equipe_combo.set(colaborador.equipe)
            
            # Habilitar botões
            self.btn_editar.config(state="normal")
            self.btn_excluir.config(state="normal")
            
        else:
            messagebox.showerror("Erro", "Colaborador não encontrado!")
            self.limpar_campos()
    
    def salvar_edicao(self):
        if not self.cpf_atual:
            return
            
        # Coletar dados dos campos
        dados = {
            campo: entry.get().strip()
            for campo, entry in self.campos.items()
        }
        dados["data_admissao"] = self.data_admissao.get_date()
        dados["equipe"] = self.equipe_combo.get()
        
        # Validar dados
        sucesso, mensagem = valida_todos_dados(
            nome=dados["nome"],
            email=dados["email"],
            cargo=dados["cargo"],
            equipe=dados["equipe"],
            data_admissao=dados["data_admissao"].strftime("%Y-%m-%d")
        )
        
        if not sucesso:
            messagebox.showerror("Erro de Validação", mensagem)
            return
        
        # Chamar controller para atualizar
        resultado = atualizar_colaborador(
            self.cpf_atual,
            nome=dados["nome"],
            email=dados["email"],
            cargo=dados["cargo"],
            equipe=dados["equipe"],
            data_admissao=dados["data_admissao"]
        )
        
        if isinstance(resultado, str):
            messagebox.showerror("Erro", resultado)
        else:
            messagebox.showinfo("Sucesso", "Colaborador atualizado com sucesso!")
            self.limpar_campos()
    
    def excluir_colaborador(self):
        if not self.cpf_atual:
            return
            
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este colaborador?"):
            resultado = excluir_colaborador(self.cpf_atual)
            if resultado is True:
                messagebox.showinfo("Sucesso", "Colaborador excluído com sucesso!")
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", resultado)
    
    def limpar_campos(self):
        self.cpf_atual = None
        self.cpf_entry.delete(0, tk.END)
        
        for entry in self.campos.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="disabled")
            
        self.data_admissao.config(state="disabled")
        self.equipe_combo.set('')
        self.equipe_combo.config(state="disabled")
        
        self.btn_editar.config(state="disabled")
        self.btn_excluir.config(state="disabled")

    def voltar(self):
        self.destroy()
        from gui.rh.cadastrar_colaborador_window import CadastraColaboradorWindow
        CadastraColaboradorWindow().mainloop()

    def gerenciar_usuario_gestor(self):
        self.destroy()
        from gui.rh.crud_usuario.gerenciar_usuario_gestor_window import GerenciaUsuariosGestorWindow
        GerenciaUsuariosGestorWindow(cpf_usuario_logado=self.cpf_usuario_logado)

if __name__ == "__main__":
    app = GerenciaColaboradoresWindow()
    app.mainloop()