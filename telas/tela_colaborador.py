import tkinter as tk
from tkinter import ttk, messagebox


class TelaColaborador(tk.Tk):
    def __init__(self, controlador_colaborador):
        super().__init__()
        self.controlador_colaborador = controlador_colaborador

        # Configurações da janela
        self.title("Colaborador - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Centraliza a janela
        self.center_window()

        # Variáveis de controle
        self.modo_atual = "menu"  # menu, cadastro, gerenciamento
        self.colaborador_atual = None

        # Criar interface
        self.criar_interface()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def criar_interface(self):
        """Cria a interface principal"""
        # Frame principal que será limpo e recriado conforme o modo
        self.main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Mostrar menu inicial
        self.mostrar_menu()

    def limpar_tela(self):
        """Limpa todos os widgets da tela"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        """Mostra o menu principal"""
        self.modo_atual = "menu"
        self.limpar_tela()

        # Título
        tk.Label(
            self.main_frame,
            text="Área do Colaborador",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(20, 40))

        # Frame dos botões
        botoes_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        botoes_frame.pack(expand=True)

        # Botões do menu
        tk.Button(
            botoes_frame,
            text="Cadastrar Colaborador",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=25,
            height=2,
            command=self.mostrar_cadastro,
        ).pack(pady=15)

        tk.Button(
            botoes_frame,
            text="Gerenciar Colaboradores",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=25,
            height=2,
            command=self.mostrar_gerenciamento,
        ).pack(pady=15)

        tk.Button(
            botoes_frame,
            text="Sair",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=25,
            height=2,
            command=self.destroy,
        ).pack(pady=15)

    def mostrar_cadastro(self):
        """Mostra a tela de cadastro"""
        self.modo_atual = "cadastro"
        self.limpar_tela()

        # Título
        tk.Label(
            self.main_frame,
            text="Cadastro de Colaborador",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(10, 30))

        # Frame do formulário
        form_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        form_frame.pack(expand=True)

        # Criar campos
        self.entries = {}
        campos = [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("cargo", "Cargo"),
            ("email", "Email"),
        ]

        for campo_id, label in campos:
            self.entries[campo_id] = self.criar_campo(form_frame, label)

        # Campo de equipe
        tk.Label(form_frame, text="Equipe", bg="#f0f0f0").pack(anchor="w", pady=(5, 5))
        self.equipe_combo = ttk.Combobox(form_frame, width=37, state="readonly")
        self.equipe_combo.pack(pady=(0, 20))

        # Carregar equipes
        self.carregar_equipes()

        # Botões
        botoes_frame = tk.Frame(form_frame, bg="#f0f0f0")
        botoes_frame.pack(pady=20)

        tk.Button(
            botoes_frame,
            text="Cadastrar",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.cadastrar_colaborador,
        ).pack(side="left", padx=10)

        tk.Button(
            botoes_frame,
            text="Limpar",
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            width=15,
            command=self.limpar_campos_cadastro,
        ).pack(side="left", padx=10)

        tk.Button(
            botoes_frame,
            text="Voltar ao Menu",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            width=15,
            command=self.mostrar_menu,
        ).pack(side="left", padx=10)

    def mostrar_gerenciamento(self):
        """Mostra a tela de gerenciamento"""
        self.modo_atual = "gerenciamento"
        self.limpar_tela()

        # Título
        tk.Label(
            self.main_frame,
            text="Gerenciar Colaboradores",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(10, 20))

        # Frame de busca
        search_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            search_frame, text="CPF do colaborador:", bg="#f0f0f0", font=("Arial", 10)
        ).pack(side="left", padx=(0, 10))
        self.cpf_entry = tk.Entry(search_frame, width=20, font=("Arial", 10))
        self.cpf_entry.pack(side="left", padx=(0, 10))

        tk.Button(
            search_frame,
            text="Buscar",
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            command=self.buscar_colaborador,
        ).pack(side="left")

        # Frame do formulário
        form_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        form_frame.pack(expand=True, fill="both")

        # Criar campos de edição
        self.entries_edit = {}
        campos = [("nome", "Nome"), ("email", "Email"), ("cargo", "Cargo")]

        for campo_id, label in campos:
            tk.Label(form_frame, text=label, bg="#f0f0f0").pack(
                anchor="w", pady=(10, 5)
            )
            entry = tk.Entry(form_frame, width=40, state="disabled", font=("Arial", 10))
            entry.pack(pady=(0, 10))
            self.entries_edit[campo_id] = entry

        # Campo de equipe
        tk.Label(form_frame, text="Equipe", bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
        self.equipe_combo_edit = ttk.Combobox(form_frame, width=37, state="disabled")
        self.equipe_combo_edit.pack(pady=(0, 20))

        # Carregar equipes
        self.carregar_equipes_edit()

        # Botões
        botoes_frame = tk.Frame(form_frame, bg="#f0f0f0")
        botoes_frame.pack(pady=20)

        self.btn_salvar = tk.Button(
            botoes_frame,
            text="Salvar Alterações",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            command=self.salvar_alteracoes,
            state="disabled",
        )
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_excluir = tk.Button(
            botoes_frame,
            text="Excluir",
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            command=self.excluir_colaborador,
            state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Limpar",
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            command=self.limpar_campos_gerenciamento,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar ao Menu",
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            command=self.mostrar_menu,
        ).pack(side="left", padx=5)

    def criar_campo(self, parent, label):
        """Cria um campo de entrada com label"""
        tk.Label(parent, text=label, bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
        entry = tk.Entry(parent, width=40, font=("Arial", 10))
        entry.pack(pady=(0, 10))
        return entry

    def carregar_equipes(self):
        """Carrega as equipes disponíveis para cadastro"""
        try:
            if self.controlador_colaborador:
                # Usar método do controlador para obter equipes
                equipes = []  # self.controlador_colaborador.obter_equipes()
                nomes_equipes = (
                    [equipe.nome for equipe in equipes]
                    if equipes
                    else ["Equipe Padrão", "Equipe Alpha", "Equipe Beta"]
                )
            else:
                nomes_equipes = ["Equipe Padrão", "Equipe Alpha", "Equipe Beta"]

            self.equipe_combo["values"] = nomes_equipes
            if nomes_equipes:
                self.equipe_combo.set(nomes_equipes[0])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar equipes: {e}")

    def carregar_equipes_edit(self):
        """Carrega as equipes disponíveis para edição"""
        try:
            if self.controlador_colaborador:
                # Usar método do controlador para obter equipes
                equipes = []  # self.controlador_colaborador.obter_equipes()
                nomes_equipes = (
                    [equipe.nome for equipe in equipes]
                    if equipes
                    else ["Equipe Padrão", "Equipe Alpha", "Equipe Beta"]
                )
            else:
                nomes_equipes = ["Equipe Padrão", "Equipe Alpha", "Equipe Beta"]

            self.equipe_combo_edit["values"] = nomes_equipes
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar equipes: {e}")

    def cadastrar_colaborador(self):
        """Realiza o cadastro do colaborador"""
        try:
            # Coletar dados
            dados = {}
            for campo, entry in self.entries.items():
                    dados[campo] = entry.get().strip()

            dados["equipe"] = self.equipe_combo.get()

            # Validar campos obrigatórios
            if not all(dados.values()):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return

            # Chamar controlador para cadastrar
            if self.controlador_colaborador:
                resultado = self.controlador_colaborador.cadastrar_colaborador(dados)
                if resultado:
                    messagebox.showinfo(
                        "Sucesso", "Colaborador cadastrado com sucesso!"
                    )
                    self.limpar_campos_cadastro()
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar colaborador!")
            else:
                messagebox.showinfo("Info", f"Dados coletados: {dados}")
                self.limpar_campos_cadastro()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cadastro: {e}")

    def limpar_campos_cadastro(self):
        """Limpa os campos de cadastro"""
        for entry in self.entries.values():
            if hasattr(entry, "delete"):
                entry.delete(0, tk.END)
            else:
                entry.set_date(None)

        if hasattr(self, "equipe_combo"):
            self.equipe_combo.set("")

    def buscar_colaborador(self):
        """Busca colaborador por CPF"""
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar!")
            return

        try:
            if self.controlador_colaborador:
                colaborador = self.controlador_colaborador.buscar_por_cpf(cpf)
                if colaborador:
                    self.preencher_campos_edicao(colaborador)
                    self.habilitar_edicao()
                else:
                    messagebox.showinfo("Info", "Colaborador não encontrado!")
                    self.limpar_campos_gerenciamento()
            else:
                # Simulação para teste
                colaborador_fake = {
                    "nome": "João Silva",
                    "email": "joao@email.com",
                    "cargo": "Desenvolvedor",
                    "data_admissao": "2023-01-15",
                    "equipe": "Equipe Alpha",
                }
                self.preencher_campos_edicao(colaborador_fake)
                self.habilitar_edicao()
                messagebox.showinfo("Info", "Colaborador encontrado (simulação)!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro na busca: {e}")

    def preencher_campos_edicao(self, colaborador):
        """Preenche os campos com dados do colaborador"""
        self.colaborador_atual = colaborador

        # Se for um objeto, usar atributos; se for dict, usar chaves
        if hasattr(colaborador, "nome"):
            # É um objeto
            dados = {
                "nome": colaborador.nome,
                "email": colaborador.email,
                "cargo": colaborador.cargo,
                "data_admissao": colaborador.data_admissao,
                "equipe": colaborador.equipe,
            }
        else:
            # É um dict
            dados = colaborador

        # Preencher campos
        for campo, valor in dados.items():
            if campo in self.entries_edit:
                entry = self.entries_edit[campo]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, valor)
            elif campo == "data_admissao":
                self.data_admissao_edit.config(state="normal")
                if isinstance(valor, str):
                    from datetime import datetime

                    data = datetime.strptime(valor, "%Y-%m-%d").date()
                    self.data_admissao_edit.set_date(data)
                else:
                    self.data_admissao_edit.set_date(valor)
            elif campo == "equipe":
                self.equipe_combo_edit.config(state="readonly")
                self.equipe_combo_edit.set(valor)

    def habilitar_edicao(self):
        """Habilita os campos para edição"""
        for entry in self.entries_edit.values():
            entry.config(state="normal")

        self.equipe_combo_edit.config(state="readonly")

        self.btn_salvar.config(state="normal")
        self.btn_excluir.config(state="normal")

    def limpar_campos_gerenciamento(self):
        """Limpa todos os campos de gerenciamento"""
        self.colaborador_atual = None

        for entry in self.entries_edit.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="disabled")

        self.equipe_combo_edit.set("")
        self.equipe_combo_edit.config(state="disabled")

        self.btn_salvar.config(state="disabled")
        self.btn_excluir.config(state="disabled")

        # Limpar campo de busca
        self.cpf_entry.delete(0, tk.END)

    def salvar_alteracoes(self):
        """Salva as alterações do colaborador"""
        if not self.colaborador_atual:
            return

        try:
            # Coletar dados
            dados = {
                campo: entry.get().strip() for campo, entry in self.entries_edit.items()
            }
            dados["equipe"] = self.equipe_combo_edit.get()

            # Validar campos
            if not all(dados.values()):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return

            # Chamar controlador para atualizar
            if self.controlador_colaborador:
                cpf = (
                    self.colaborador_atual.cpf
                    if hasattr(self.colaborador_atual, "cpf")
                    else self.cpf_entry.get()
                )
                resultado = self.controlador_colaborador.atualizar_colaborador(
                    cpf, dados
                )
                if resultado:
                    messagebox.showinfo(
                        "Sucesso", "Colaborador atualizado com sucesso!"
                    )
                    self.limpar_campos_gerenciamento()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar colaborador!")
            else:
                messagebox.showinfo("Info", f"Dados atualizados: {dados}")
                self.limpar_campos_gerenciamento()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def excluir_colaborador(self):
        """Exclui o colaborador atual"""
        if not self.colaborador_atual:
            return

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir este colaborador?"
        ):
            try:
                if self.controlador_colaborador:
                    cpf = (
                        self.colaborador_atual.cpf
                        if hasattr(self.colaborador_atual, "cpf")
                        else self.cpf_entry.get()
                    )
                    resultado = self.controlador_colaborador.excluir_colaborador(cpf)
                    if resultado:
                        messagebox.showinfo(
                            "Sucesso", "Colaborador excluído com sucesso!"
                        )
                        self.limpar_campos_gerenciamento()
                    else:
                        messagebox.showerror("Erro", "Erro ao excluir colaborador!")
                else:
                    messagebox.showinfo("Info", "Colaborador excluído (simulação)!")
                    self.limpar_campos_gerenciamento()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")


if __name__ == "__main__":
    app = TelaColaborador()
    app.mainloop()
