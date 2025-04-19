import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import autenticar
from utils.check_data import check_cpf

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login - EasyControl")
        self.geometry("500x400")
        
        self.label_cpf = tk.Label(self, text="CPF:")
        self.label_cpf.pack(pady=10)
        
        self.entry_cpf = tk.Entry(self)
        self.entry_cpf.pack(pady=5)
        
        self.label_senha = tk.Label(self, text="Senha:")
        self.label_senha.pack(pady=10)
        
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack(pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        cpf = self.entry_cpf.get()
        if not check_cpf(cpf):
            messagebox.showerror("Erro", "CPF inválido!")
            return
            
        senha = self.entry_senha.get()

        if autenticar(cpf, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            # Aqui a ideia é que vá para a próxima janela
            # Seguindo a lógica abaixo
            # self.destroy()  # Fecha a janela de login
            # next_window = NextWindow()
        else:
            messagebox.showerror("Erro", "CPF ou senha inválidos!")
