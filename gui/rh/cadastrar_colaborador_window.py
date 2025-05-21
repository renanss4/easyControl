import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Adicionar esta importação
from controllers.colaborador_controller import criar_colaborador
from controllers.equipe_controller import listar_equipes
from utils.check_data import valida_todos_dados

class CadastraColaboradorWindow(tk.Tk): 
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Cadastro de Colaborador")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        
        # Frame central
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        label_title = tk.Label(frame, text="Cadastro de Colaborador", font=("Arial", 16, "bold"), bg="#dcdcdc")
        label_title.pack(pady=(0, 20))
        
        # Campos de entrada (removendo equipe e data_admissao pois serão tratados separadamente)
        self.campos = [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("cargo", "Cargo"),
            ("email", "Email")
        ]
        
        # Dicionário para armazenar as entries
        self.entries = {}
        
        # Criar campos
        for campo_id, label in self.campos:
            self.entries[campo_id] = self.create_label_and_entry(frame, label)
            
        # Criando o campo de data_admissao separadamente com DateEntry
        tk.Label(frame, text="Data de admissão", bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        self.entries["data_admissao"] = DateEntry(
            frame, 
            date_pattern="yyyy-mm-dd",
            width=27,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.entries["data_admissao"].pack(pady=(0, 10))
            
        # Criando o campo de equipe separadamente com Combobox
        tk.Label(frame, text="Equipe", bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        self.equipe_combo = ttk.Combobox(frame, width=27, state="readonly")
        self.equipe_combo.pack(pady=(0, 10))
        
        # Carregar as equipes disponíveis
        self.carregar_equipes()
        
        # Frame para os botões
        botoes_frame = tk.Frame(frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(20, 0))

        # Botões existentes...
        tk.Button(
            botoes_frame,
            text="Concluir cadastro",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.concluir_cadastro
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar
        ).pack(side="left", padx=5)

    def carregar_equipes(self):
        """Carrega as equipes disponíveis no Combobox"""
        equipes = listar_equipes()
        nomes_equipes = [equipe.nome for equipe in equipes]
        self.equipe_combo['values'] = nomes_equipes
        if nomes_equipes:
            self.equipe_combo.set(nomes_equipes[0])  # Seleciona a primeira equipe por padrão

    def create_label_and_entry(self, parent, text):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=(0, 10))
        return entry

    def concluir_cadastro(self):
        # Coletar dados dos campos
        dados = {
            campo_id: self.entries[campo_id].get().strip()
            for campo_id, _ in self.campos
        }
        
        # Adicionar a data de admissão
        dados['data_admissao'] = self.entries['data_admissao'].get()
        
        # Adicionar a equipe selecionada
        dados['equipe'] = self.equipe_combo.get()
        
        if not dados['equipe']:
            messagebox.showerror("Erro", "Por favor, selecione uma equipe.")
            return
        
        # Validar todos os dados
        sucesso, mensagem = valida_todos_dados(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            data_admissao=dados['data_admissao'],
            cargo=dados['cargo'],
            equipe=dados['equipe'],
            solicitacoes_protocolos=[]  # Adiciona lista vazia de solicitações
        )
        
        if not sucesso:
            messagebox.showerror("Erro de Validação", mensagem)
            return
        
        # Chamar o controller para criar o colaborador
        resultado = criar_colaborador(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            data_admissao=dados['data_admissao'],
            cargo=dados['cargo'],
            equipe=dados['equipe']
        )
        
        if isinstance(resultado, str):
            # Se for uma string, é uma mensagem de erro
            messagebox.showerror("Erro", resultado)
        else:
            # Se não for string, é o objeto colaborador criado
            messagebox.showinfo("Sucesso", "Colaborador cadastrado com sucesso!")
            self.voltar()

    def voltar(self):
        self.destroy()
        from gui.rh.principal_rh_window import PrincipalRhWindow
        PrincipalRhWindow()

if __name__ == "__main__":
    app = CadastraColaboradorWindow()
    app.mainloop()