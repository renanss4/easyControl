import tkinter as tk
from tkinter import messagebox
from controllers.colaborador_controller import criar_colaborador

class CadastroColaboradorWindow(tk.Tk): 
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Cadastro de Colaborador")
        self.geometry("700x600")
        self.configure(bg="#dcdcdc")
        
        # Frame central
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        label_title = tk.Label(frame, text="Cadastro de Colaborador", font=("Arial", 16, "bold"), bg="#dcdcdc")
        label_title.pack(pady=(0, 20))
        
        # Dicionário para armazenar as entries
        self.entries = {}
        
        # Campos de entrada
        self.entries["Nome"] = self.create_label_and_entry(frame, "Nome")
        self.entries["CPF"] = self.create_label_and_entry(frame, "CPF")
        self.entries["Data de admissão"] = self.create_label_and_entry(frame, "Data de admissão")
        self.entries["Equipe"] = self.create_label_and_entry(frame, "Equipe")
        self.entries["Cargo"] = self.create_label_and_entry(frame, "Cargo")
        self.entries["Email"] = self.create_label_and_entry(frame, "Email")
        
        # Botão de cadastro
        btn_cadastrar = tk.Button(frame, text="Concluir cadastro", command=self.concluir_cadastro)
        btn_cadastrar.pack(pady=(20, 0))

        self.mainloop()  # Adicionado no final do método __init__

    def create_label_and_entry(self, parent, text):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=(0, 10))
        return entry

    def concluir_cadastro(self):
        # Obter valores dos campos
        nome = self.entries["Nome"].get()
        cpf = self.entries["CPF"].get()
        data_admissao = self.entries["Data de admissão"].get()
        equipe = self.entries["Equipe"].get()
        cargo = self.entries["Cargo"].get()
        email = self.entries["Email"].get()
        
        # Validar se os campos não estão vazios
        if not nome or not cpf or not data_admissao or not email:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        # Chamar o controller para criar o colaborador
        resultado = criar_colaborador(
            nome=nome,
            cpf=cpf,
            email=email,
            data_admissao=data_admissao,
            cargo=cargo,
            equipe=equipe
        )
        
        # Verificar o resultado
        if isinstance(resultado, str):
            # Se for uma string, é uma mensagem de erro
            messagebox.showerror("Erro", resultado)
        else:
            # Se não for string, é o objeto colaborador criado
            messagebox.showinfo("Sucesso", "Colaborador cadastrado com sucesso!")
            self.destroy()  # Fecha a janela de cadastro