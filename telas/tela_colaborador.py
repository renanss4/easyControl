import tkinter as tk
from tkinter import messagebox


class TelaColaborador(tk.Tk):
    def __init__(self, controlador_colaborador):
        super().__init__()
        self.__controlador_colaborador = controlador_colaborador
        self.title("Cadastrar Colaborador")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        label_title = tk.Label(
            frame,
            text="Cadastro de Colaborador",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        )
        label_title.pack(pady=(0, 20))

        # Campos de entrada
        self.campos = [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("cargo", "Cargo"),
            ("email", "Email"),
        ]

        # Dicionário para armazenar as entries
        self.entries = {}

        # Criar campos
        for campo_id, label in self.campos:
            self.entries[campo_id] = self.gerar_campos_entrada(frame, label)

        # Frame para os botões
        botoes_frame = tk.Frame(frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(20, 0))

        # Botões
        tk.Button(
            botoes_frame,
            text="Cadastrar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.concluir_cadastro,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Gerenciar Colaboradores",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=25,
            command=self.gerenciar_colaborador,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.voltar,
        ).pack(side="left", padx=5)

    def gerar_campos_entrada(self, parent, text):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30)
        entry.pack(pady=(0, 10))
        return entry

    def concluir_cadastro(self):
        """Conclui o cadastro do colaborador"""
        # Coletar dados dos campos
        dados = {
            campo_id: self.entries[campo_id].get().strip()
            for campo_id, _ in self.campos
        }

        if not all(dados.values()):
            messagebox.showerror(
                "Erro de Validação",
                "Todos os campos são obrigatórios e devem ser preenchidos",
            )
            return

        try:
            # Chamar o controlador para cadastrar o colaborador
            resultado = self.__controlador_colaborador.cadastrar_colaborador(
                dados["cpf"], dados["nome"], dados["cargo"], dados["email"]
            )
            if resultado:
                messagebox.showinfo("Sucesso", "Colaborador cadastrado com sucesso!")
                # Limpar campos após o cadastro bem-sucedido
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar o colaborador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

    def gerenciar_colaborador(self):
        """Abre a tela de gerenciamento de colaboradores"""
        self.destroy()
        TelaGerenciarColaborador(self.__controlador_colaborador)

    def voltar(self):
        """Volta para a tela do RH"""
        try:
            self.destroy()
            self.__controlador_colaborador.voltar_tela_funcionario_rh()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar para tela de rh: {e}")


class TelaGerenciarColaborador(tk.Tk):
    def __init__(self, controlador_colaborador):
        super().__init__()
        self.__controlador_colaborador = controlador_colaborador
        self.title("Gerenciar Colaboradores - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(search_frame, text="CPF do colaborador:", bg="#dcdcdc").pack(
            side="left", padx=(0, 10)
        )

        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Buscar", command=self.buscar_colaborador).pack(
            side="left"
        )

        # Frame dos campos
        self.campos_frame = tk.Frame(main_frame, bg="#dcdcdc")
        self.campos_frame.pack(fill="both", expand=True)

        # Criar campos de edição (inicialmente desabilitados)
        self.campos = {}
        self.campos_labels = [
            ("nome", "Nome"),
            ("email", "Email"),
            ("cargo", "Cargo"),
        ]

        for campo_id, label in self.campos_labels:
            tk.Label(self.campos_frame, text=label, bg="#dcdcdc").pack(
                anchor="w", pady=(5, 0)
            )

            entry = tk.Entry(self.campos_frame, width=40)
            entry.pack(pady=(0, 10))
            entry.config(state="disabled")
            self.campos[campo_id] = entry

        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=20)

        self.btn_editar = tk.Button(
            botoes_frame,
            text="Salvar Alterações",
            command=self.salvar_edicao,
            state="disabled",
        )
        self.btn_editar.pack(side="left", padx=5)

        self.btn_excluir = tk.Button(
            botoes_frame,
            text="Excluir Colaborador",
            command=self.excluir_colaborador,
            state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(botoes_frame, text="Voltar", command=self.voltar).pack(
            side="left", padx=5
        )

        # Armazenar CPF do colaborador atual
        self.cpf_atual = None

    def buscar_colaborador(self):
        """Busca um colaborador pelo CPF"""
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar")
            return

        try:
            # Buscar colaborador pelo CPF usando o controlador
            colaborador = self.__controlador_colaborador.buscar_colaborador_por_cpf(cpf)

            if colaborador:
                # Armazenar CPF do colaborador encontrado
                self.cpf_atual = cpf

                # Habilitar campos
                for campo in self.campos.values():
                    campo.config(state="normal")

                # Preencher campos com dados do colaborador
                self.campos["nome"].delete(0, tk.END)
                self.campos["nome"].insert(0, colaborador.nome)

                self.campos["email"].delete(0, tk.END)
                self.campos["email"].insert(0, colaborador.email)

                self.campos["cargo"].delete(0, tk.END)
                self.campos["cargo"].insert(0, colaborador.cargo)

                # Habilitar botões
                self.btn_editar.config(state="normal")
                self.btn_excluir.config(state="normal")
            else:
                messagebox.showerror("Erro", "Colaborador não encontrado!")
                self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar colaborador: {str(e)}")

    def salvar_edicao(self):
        """Salva as alterações feitas no colaborador"""
        if not self.cpf_atual:
            return

        # Coletar dados dos campos
        dados = {campo: entry.get().strip() for campo, entry in self.campos.items()}
        dados["cpf"] = self.cpf_atual  # Incluir o CPF nos dados para o controlador

        # Validar dados
        if not all(dados.values()):
            messagebox.showerror(
                "Erro de Validação",
                "Todos os campos são obrigatórios e devem ser preenchidos",
            )
            return

        try:
            # Chamar controlador para atualizar
            resultado = self.__controlador_colaborador.atualizar_colaborador(
                self.cpf_atual,
                dados["nome"],
                dados["cargo"],
                dados["email"],
            )
            if resultado:
                messagebox.showinfo("Sucesso", "Colaborador atualizado com sucesso!")
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o colaborador")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    def excluir_colaborador(self):
        """Exclui um colaborador"""
        if not self.cpf_atual:
            return

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente excluir este colaborador?"
        ):
            try:
                resultado = self.__controlador_colaborador.excluir_colaborador(
                    self.cpf_atual
                )
                if resultado:
                    messagebox.showinfo("Sucesso", "Colaborador excluído com sucesso!")
                    self.limpar_campos()
                else:
                    messagebox.showerror(
                        "Erro", "Não foi possível excluir o colaborador"
                    )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    def limpar_campos(self):
        """Limpa os campos do formulário"""
        self.cpf_atual = None
        self.cpf_entry.delete(0, tk.END)

        for entry in self.campos.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="disabled")

        self.btn_editar.config(state="disabled")
        self.btn_excluir.config(state="disabled")

    def voltar(self):
        """Volta para a tela de cadastro de colaborador"""
        self.destroy()
        TelaColaborador(self.__controlador_colaborador)
