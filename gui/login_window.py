import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import autenticar
from utils.check_data import check_email
from gui.main_window import MainWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # PARTE VISUAL

        # Título da janela
        self.title("Login - EasyControl")
        self.geometry("500x400")
        self.configure(bg="#dcdcdc")  # Cor de fundo clara

        # Frame central
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        # Título
        label_title = tk.Label(frame, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc")
        label_title.pack(pady=(0, 20))

        # E-mail
        tk.Label(frame, text="E-mail", bg="#dcdcdc").pack(anchor="w")
        self.entry_email = tk.Entry(frame, width=40)
        self.entry_email.pack(pady=(0, 10))

        # Senha
        tk.Label(frame, text="Senha", bg="#dcdcdc").pack(anchor="w")
        self.entry_senha = tk.Entry(frame, show="*", width=40)
        self.entry_senha.pack(pady=(0, 20))

        # Botão de login
        tk.Button(frame, text="Login", width=15, command=self.login).pack()

        # Rodapé com links
        label_register = tk.Label(self, text="Ainda não tem uma conta? Cadastre-se aqui!", fg="blue", bg="#dcdcdc", cursor="hand2")
        label_register.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")
        label_register.bind("<Button-1>", self.abrir_cadastro)

        label_solicitacoes = tk.Label(self, text="Consulte aqui suas solicitações!", fg="blue", bg="#dcdcdc", cursor="hand2")
        label_solicitacoes.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        label_solicitacoes.bind("<Button-1>", self.abrir_solicitacoes)

    # PARTE LÓGICA

    def login(self):
        email = self.entry_email.get()
        if not check_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return
        
        senha = self.entry_senha.get()

        if autenticar(email, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")

            # Quando queremos ir para outra janela, devemos destruir a janela atual
            # e chamar a nova janela. 
            
            self.destroy()
            main_window = MainWindow()
            main_window.mainloop()
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos!")

    def abrir_cadastro(self, event=None):
        messagebox.showinfo("Cadastro", "Funcionalidade de cadastro ainda não implementada.")

    def abrir_solicitacoes(self, event=None):
        messagebox.showinfo("Solicitações", "Visualização de solicitações ainda não implementada.")
