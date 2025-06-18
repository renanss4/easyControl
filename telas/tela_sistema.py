import tkinter as tk
from tkinter import messagebox
from modelos.modelo_gestor import Gestor
from modelos.modelo_funcionario_rh import FuncionarioRH


class TelaSistema(tk.Tk):
    def __init__(self, controlador_sistema):
        super().__init__()
        self.__controlador_sistema = controlador_sistema

        self.title("Login - EasyControl")
        self.geometry("900x700")
        self.configure(bg="#dcdcdc")

        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.4, anchor="center")

        label_title = tk.Label(
            frame, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc"
        )
        label_title.pack(pady=(0, 20))

        tk.Label(frame, text="E-mail", bg="#dcdcdc").pack(anchor="w")
        self.entry_email = tk.Entry(frame, width=40)
        self.entry_email.pack(pady=(0, 10))

        tk.Label(frame, text="Senha", bg="#dcdcdc").pack(anchor="w")
        self.entry_senha = tk.Entry(frame, show="*", width=40)
        self.entry_senha.pack(pady=(0, 20))

        tk.Button(frame, text="Login", width=15, command=self.login).pack()

        label_solicitacoes = tk.Label(
            self,
            text="Consulte aqui suas solicitações!",
            fg="blue",
            bg="#dcdcdc",
            cursor="hand2",
        )
        label_solicitacoes.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        label_solicitacoes.bind("<Button-1>", self.consultar_solicitacoes)

    def login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "E-mail e senha são obrigatórios!")
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Erro", "E-mail inválido!")
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            return

        if len(senha) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            self.entry_senha.delete(0, tk.END)
            return

        usuario = self.__controlador_sistema.autenticar_usuario(email, senha)

        if isinstance(usuario, (Gestor, FuncionarioRH)):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")

            if isinstance(usuario, FuncionarioRH):
                self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()
                self.destroy()
            else:
                self.__controlador_sistema.controlador_gestor.abrir_tela_gestor()
                self.destroy()
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos!")

    def consultar_solicitacoes(self, event=None):
        messagebox.showinfo(
            "Consultar solicitações",
            "Funcionalidade consultar solicitações ainda não implementada.",
        )
