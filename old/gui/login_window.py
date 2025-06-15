import tkinter as tk
from controllers.usuario_controller import autenticar
from utils.check_data import valida_todos_dados
from gui.gestor.principal_gestor_window import PrincipalGestorWindow
from gui.rh.principal_rh_window import PrincipalRhWindow
from gui.consultar_solicitacoes_window import ConsultaSolicitacoesWindow

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # PARTE VISUAL

        # Título da janela
        self.title("Login - EasyControl")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")

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

        label_solicitacoes = tk.Label(self, text="Consulte aqui suas solicitações!", fg="blue", bg="#dcdcdc", cursor="hand2")
        label_solicitacoes.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        label_solicitacoes.bind("<Button-1>", self.consultar_solicitacoes)

    # PARTE LÓGICA

    # UC01
    def login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        # Valida os campos usando valida_todos_dados
        sucesso, mensagem = valida_todos_dados(
            email=email,
            senha=senha
        )
        
        if not sucesso:
            tk.messagebox.showerror("Erro", mensagem)
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            return

        usuario = autenticar(email, senha)

        if usuario:
            tk.messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.destroy()
            
            # Redireciona baseado no tipo de usuário
            if usuario.tipo.value == "rh":
                window = PrincipalRhWindow()
            else:  # Gestor
                window = PrincipalGestorWindow(usuario.cpf)
            
            window.mainloop()
        else:
            tk.messagebox.showerror("Erro", "E-mail ou senha inválidos!")
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)


    # UC09
    def consultar_solicitacoes(self, event=None):
        tk.messagebox.showinfo("Consultar solicitações", "Funcionalidade consultar solicitações ainda não implementada.")

        # self.destroy()
        # ConsultaSolicitacoesWindow()
