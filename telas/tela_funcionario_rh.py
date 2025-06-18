import tkinter as tk
from tkinter import messagebox


class TelaRH(tk.Tk):
    def __init__(self, controlador_funcionario_rh):
        super().__init__()
        self.controlador_funcionario_rh = controlador_funcionario_rh

        self.title("RH - EasyControl")
        self.geometry("800x600")
        self.configure(bg="#dcdcdc")

        # Centraliza a janela
        self.transient()
        self.grab_set()

        tk.Label(
            self, text="EASY CONTROL", font=("Arial", 18, "bold"), bg="#dcdcdc"
        ).pack(pady=20)

        quadro_botoes = tk.Frame(
            self, bg="#dcdcdc", bd=1, relief="solid", padx=20, pady=20
        )
        quadro_botoes.pack(pady=10)

        tk.Button(
            quadro_botoes,
            text="Cadastrar Colaborador",
            width=25,
            height=2,
            command=self.abrir_cadastro_colaborador,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Cadastrar Gestor",
            width=25,
            height=2,
            command=self.abrir_cadastro_gestor,
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Cadastrar Funcionário RH",
            width=25,
            height=2,
            command=self.abrir_cadastro_funcionario_rh,
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Cadastrar Solicitações",
            width=25,
            height=2,
            command=self.abrir_cadastro_solicitacao,
        ).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Cadastrar Equipe",
            width=25,
            height=2,
            command=self.abrir_cadastro_equipe,
        ).grid(row=2, column=0, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Gerar Relatório de Férias",
            width=25,
            height=2,
            command=self.gerar_relatorio_ferias,
        ).grid(row=2, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(rodape, text="Sair", width=20, height=2, command=self.sair).grid(
            row=0, column=0, padx=20
        )

    def abrir_cadastro_colaborador(self):
        """Abre a tela de cadastro de colaborador"""
        try:
            self.controlador_funcionario_rh.abrir_tela_cadastro_colaborador()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de colaborador: {e}")

    def abrir_cadastro_gestor(self):
        """Abre a tela de cadastro de gestor"""
        try:
            self.controlador_funcionario_rh.abrir_tela_cadastro_gestor()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de gestor: {e}")

    def abrir_cadastro_funcionario_rh(self):
        """Abre a tela de cadastro de funcionário RH"""
        try:
            self.controlador_funcionario_rh.abrir_tela_cadastro_funcionario_rh()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de RH: {e}")

    def abrir_cadastro_solicitacao(self):
        """Abre a tela de cadastro de solicitação"""
        try:
            self.controlador_funcionario_rh.abrir_tela_solicitacao()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de solicitação: {e}")

    def abrir_cadastro_equipe(self):
        """Abre a tela de cadastro de equipe"""
        try:
            self.controlador_funcionario_rh.abrir_tela_equipe()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de equipe: {e}")

    def consultar_lista_colaboradores(self):
        """Abre a consulta de colaboradores"""
        try:
            self.controlador_funcionario_rh.consultar_lista_colaboradores()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar colaboradores: {e}")

    def gerar_relatorio_ferias(self):
        """Gera relatório de férias"""
        try:
            self.controlador_funcionario_rh.gerar_relatorio_ferias()
            messagebox.showinfo(
                "Info", "Funcionalidade de relatório ainda não implementada"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

    def sair(self):
        confirm = messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()
            # Volta para a tela de login através do controlador sistema
            self.controlador_funcionario_rh.controlador_sistema.abre_tela_sistema()
