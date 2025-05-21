import tkinter as tk
from controllers.usuario_controller import (
    buscar_usuario_por_cpf,
    atualizar_usuario,
    excluir_usuario
)
from controllers.equipe_controller import listar_equipes
from utils.check_data import valida_todos_dados

class GerenciaUsuariosWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Gerenciar Usuários - EasyControl")
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
            text="CPF do usuário:", 
            bg="#dcdcdc"
        ).pack(side="left", padx=(0, 10))
        
        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="Buscar",
            command=self.buscar_usuario
        ).pack(side="left")
        
        # Frame dos campos
        self.campos_frame = tk.Frame(main_frame, bg="#dcdcdc")
        self.campos_frame.pack(fill="both", expand=True)
        
        # Criar campos de edição (inicialmente desabilitados)
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
            
        # Criando o campo de equipe separadamente com Combobox
        tk.Label(
            self.campos_frame,
            text="Equipe",
            bg="#dcdcdc"
        ).pack(anchor="w", pady=(5, 0))
        
        self.equipe_combo = tk.ttk.Combobox(
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
            text="Excluir Usuário",
            command=self.excluir_usuario,
            state="disabled"
        )
        self.btn_excluir.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(
            botoes_frame,
            text="Voltar",
            command=self.voltar
        ).pack(side="left", padx=5)
        
        # Armazenar CPF do usuário atual
        self.cpf_atual = None
        
    def carregar_equipes(self):
        """Carrega as equipes disponíveis no Combobox"""
        equipes = listar_equipes()
        nomes_equipes = [equipe.nome for equipe in equipes]
        self.equipe_combo['values'] = nomes_equipes
    
    def buscar_usuario(self):
        cpf = self.cpf_entry.get().strip()
        
        # Validar CPF
        sucesso, mensagem = valida_todos_dados(cpf=cpf)
        if not sucesso:
            tk.messagebox.showerror("Erro", mensagem)
            return
            
        usuario = buscar_usuario_por_cpf(cpf)
        
        if usuario:
            # Armazenar CPF do usuário encontrado
            self.cpf_atual = cpf
            
            # Habilitar campos
            for campo in self.campos.values():
                campo.config(state="normal")
            self.equipe_combo.config(state="readonly")
            
            # Preencher campos com dados do usuário
            self.campos["nome"].delete(0, tk.END)
            self.campos["nome"].insert(0, usuario.nome)
            
            self.campos["email"].delete(0, tk.END)
            self.campos["email"].insert(0, usuario.email)
            
            self.campos["cargo"].delete(0, tk.END)
            self.campos["cargo"].insert(0, usuario.cargo)
            
            # Setar equipe no combobox
            self.equipe_combo.set(usuario.equipe)
            
            # Habilitar botões
            self.btn_editar.config(state="normal")
            self.btn_excluir.config(state="normal")
            
        else:
            tk.messagebox.showerror("Erro", "Usuário não encontrado!")
            self.limpar_campos()
    
    def salvar_edicao(self):
        if not self.cpf_atual:
            return
            
        # Coletar dados dos campos
        dados = {
            campo: entry.get().strip()
            for campo, entry in self.campos.items()
        }
        dados["equipe"] = self.equipe_combo.get()
        
        # Validar dados
        sucesso, mensagem = valida_todos_dados(
            nome=dados["nome"],
            email=dados["email"],
            cargo=dados["cargo"],
            equipe=dados["equipe"]
        )
        
        if not sucesso:
            tk.messagebox.showerror("Erro de Validação", mensagem)
            return
        
        # Chamar controller para atualizar
        resultado = atualizar_usuario(
            self.cpf_atual,
            nome=dados["nome"],
            email=dados["email"],
            cargo=dados["cargo"],
            equipe=dados["equipe"]
        )
        
        if resultado:
            tk.messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            self.limpar_campos()
        else:
            tk.messagebox.showerror("Erro", "Não foi possível atualizar o usuário.")
    
    def excluir_usuario(self):
        if not self.cpf_atual:
            return
            
        if tk.messagebox.askyesno("Confirmar", "Deseja realmente excluir este usuário?"):
            if excluir_usuario(self.cpf_atual):
                tk.messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.limpar_campos()
            else:
                tk.messagebox.showerror("Erro", "Não foi possível excluir o usuário.")
    
    def limpar_campos(self):
        self.cpf_atual = None
        self.cpf_entry.delete(0, tk.END)
        
        for entry in self.campos.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="disabled")
            
        self.equipe_combo.set('')
        self.equipe_combo.config(state="disabled")
        
        self.btn_editar.config(state="disabled")
        self.btn_excluir.config(state="disabled")

    def voltar(self):
        self.destroy()
        from gui.rh.cadastrar_rh_window import CadastraRhWindow
        CadastraRhWindow().mainloop()

if __name__ == "__main__":
    app = GerenciaUsuariosWindow()
    app.mainloop()