import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from controllers.usuario_controller import cadastrar_rh
from utils.check_data import valida_todos_dados
from datetime import datetime

class CadastraRhWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Cadastro de RH - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        
        # Frame central
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        label_title = tk.Label(frame, text="Cadastro de RH", font=("Arial", 16, "bold"), bg="#dcdcdc")
        label_title.pack(pady=(0, 20))
        
        # Campos de entrada
        self.campos = [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("email", "Email"),
            ("senha", "Senha"),
            ("cargo", "Cargo")
        ]
        
        # Dicionário para armazenar as entries
        self.entries = {}
        
        # Criar campos
        for campo_id, label in self.campos:
            # Se for o campo de senha, criar com máscara
            if campo_id == "senha":
                self.entries[campo_id] = self.create_label_and_entry(frame, label, show="*")
            else:
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
        
        # Frame para os botões
        botoes_frame = tk.Frame(frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(20, 0))

        # Botões
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
            text="Gerenciar Usuário",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.gerenciar_usuario
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar
        ).pack(side="left", padx=5)

    def create_label_and_entry(self, parent, text, show=None):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30, show=show)
        entry.pack(pady=(0, 10))
        return entry

    def concluir_cadastro(self):
        # Coletar dados dos campos
        dados = {
            campo_id: self.entries[campo_id].get().strip()
            for campo_id, _ in self.campos
        }
        
        # Adicionar a data de admissão e converter para objeto date
        data_str = self.entries['data_admissao'].get()
        dados['data_admissao'] = datetime.strptime(data_str, "%Y-%m-%d").date()
        
        # Validar todos os dados
        sucesso, mensagem = valida_todos_dados(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            senha=dados['senha'],
            data_admissao=data_str,  # Para validação, usamos a string
            cargo=dados['cargo'],
            equipe="RH",  # Equipe fixa para RH
            solicitacoes_protocolos=[]
        )
        
        if not sucesso:
            messagebox.showerror("Erro de Validação", mensagem)
            return
        
        # Chamar o controller para criar o usuário RH
        resultado = cadastrar_rh(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            senha=dados['senha'],
            data_admissao=dados['data_admissao'],  # Aqui passamos o objeto date
            cargo=dados['cargo']  # Equipe será definida como "RH" no controller
        )
        
        if isinstance(resultado, str):
            # Se for uma string, é uma mensagem de erro
            messagebox.showerror("Erro", resultado)
        else:
            # Se não for string, é o objeto usuário criado
            messagebox.showinfo("Sucesso", "Funcionário RH cadastrado com sucesso!")
            self.voltar()

    def gerenciar_usuario(self):
        self.destroy()
        from gui.rh.crud_usuario.gerenciar_usuario_window import GerenciaUsuariosWindow
        GerenciaUsuariosWindow()

    def voltar(self):
        self.destroy()
        from gui.rh.principal_rh_window import PrincipalRhWindow
        PrincipalRhWindow()

if __name__ == "__main__":
    app = CadastraRhWindow()
    app.mainloop()