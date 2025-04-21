import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from controllers.rh_controller import cadastrar_rh


class CadastroRHWindow(tk.Tk):
    def __init__(self, tela_anterior=None):
        super().__init__()
        self.title("Cadastro de RH")
        self.configure(bg="#dcdcdc")
        self.geometry("700x600")
        self.tela_anterior = tela_anterior

        # Frame principal com borda
        borda_frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=10, pady=10)
        borda_frame.pack(padx=20, pady=(20, 10), fill="both", expand=False)

        # Título da janela
        tk.Label(
            borda_frame,
            text="Cadastro de RH",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc"
        ).pack(pady=15)
        
        # Container dos campos
        campos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        campos_frame.pack(pady=10)

        self.campos = {}

        # Nome
        tk.Label(campos_frame, text="Nome", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["nome"] = tk.Entry(campos_frame, width=30)
        self.campos["nome"].pack(padx=20)

        # CPF
        tk.Label(campos_frame, text="CPF", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["cpf"] = tk.Entry(campos_frame, width=30)
        self.campos["cpf"].pack(padx=20)

        # Data de admissão
        tk.Label(campos_frame, text="Data de admissão", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["dataAdmissao"] = DateEntry(campos_frame, date_pattern="yyyy-mm-dd", width=27, background='darkblue', foreground='white', borderwidth=2)
        self.campos["dataAdmissao"].pack(padx=20)

        # Equipe
        tk.Label(campos_frame, text="Equipe", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["equipe"] = tk.Entry(campos_frame, width=30)
        self.campos["equipe"].pack(padx=20)

        # Cargo
        tk.Label(campos_frame, text="Cargo", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["cargo"] = tk.Entry(campos_frame, width=30)
        self.campos["cargo"].pack(padx=20)

        # Email
        tk.Label(campos_frame, text="Email", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["email"] = tk.Entry(campos_frame, width=30)
        self.campos["email"].pack(padx=20)

        # Senha
        tk.Label(campos_frame, text="Senha", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["senha"] = tk.Entry(campos_frame, width=30, show="*")
        self.campos["senha"].pack(padx=20)

        # Botão de conclusão
        tk.Button(
            self,
            text="Concluir cadastro",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=25,
            command=self.concluir_cadastro
        ).pack(pady=(10, 20))

    def concluir_cadastro(self):
        dados = {chave: campo.get().strip() for chave, campo in self.campos.items()}
        if not all(dados.values()):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        try:
            data_formatada = datetime.strptime(dados["dataAdmissao"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "A data deve estar no formato YYYY-MM-DD.")
            return
        try:
            equipe_int = int(dados["equipe"])
        except ValueError:
            messagebox.showerror("Erro", "Equipe deve ser um número inteiro.")
            return

        resultado = cadastrar_rh(
            nome=dados["nome"],
            cpf=dados["cpf"],
            email=dados["email"],
            senha=dados["senha"],
            dataAdmissao=data_formatada,
            cargo=dados["cargo"],
            equipe=equipe_int
        )

        if isinstance(resultado, str):
            messagebox.showerror("Erro", resultado)
        else:
            messagebox.showinfo("Sucesso", "Funcionário RH cadastrado com sucesso!")
            self.destroy()
            
            if self.tela_anterior == "login":
                from gui.login_window import LoginWindow
                LoginWindow().mainloop()
            elif self.tela_anterior == "main":
                from gui.main_window import MainWindow
                MainWindow().mainloop()
