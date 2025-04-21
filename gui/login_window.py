import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import autenticar
from utils.check_data import check_email, check_password
from gui.main_window import MainWindow
from gui.cadastro_rh_window import CadastroRHWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # PARTE VISUAL

        # Título da janela
        self.title("Login - EasyControl")
        self.geometry("700x600")
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

        # Botão de login -> o parametro "command" chama a função login() quando o botão é pressionado
        tk.Button(frame, text="Login", width=15, command=self.login).pack()

        # Rodapé com links
        label_register = tk.Label(self, text="Cadastrar funcionário de RH", fg="blue", bg="#dcdcdc", cursor="hand2")
        label_register.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")
        label_register.bind("<Button-1>", self.cadastrar_rh)

        label_solicitacoes = tk.Label(self, text="Consulte aqui suas solicitações!", fg="blue", bg="#dcdcdc", cursor="hand2")
        label_solicitacoes.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        label_solicitacoes.bind("<Button-1>", self.abrir_solicitacoes)

    # PARTE LÓGICA

    def login(self):
        email = self.entry_email.get()
        if not check_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            self.entry_email.delete(0, tk.END)
            return
        
        senha = self.entry_senha.get()
        if not check_password(senha):
            messagebox.showerror("Erro", "Senha inválida!")
            self.entry_senha.delete(0, tk.END)
            return

        if autenticar(email, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.destroy()
            main_window = MainWindow()
            main_window.mainloop()
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos!")
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)


    def cadastrar_rh(self, event=None):
        CadastroRHWindow()
        
        
    def abrir_solicitacoes(self, event=None):
        messagebox.showinfo("Solicitações", "Visualização de solicitações ainda não implementada.")
