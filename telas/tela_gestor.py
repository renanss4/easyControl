import tkinter as tk
from tkinter import messagebox


class TelaGestor(tk.Tk):
    def __init__(self, controlador_gestor):
        super().__init__()
        self.__controlador_gestor = controlador_gestor
        self.title("Cadastrar Gestor")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Center frame within the larger window
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        label_title = tk.Label(
            frame,
            text="Cadastro de Gestor",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        )
        label_title.pack(pady=(0, 20))

        # Campos de entrada
        self.campos = [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("email", "Email"),
            ("senha", "Senha"),
            ("cargo", "Cargo"),
        ]

        # Dicionário para armazenar as entries
        self.entries = {}

        # Criar campos
        for campo_id, label in self.campos:
            # Se for o campo de senha, criar com máscara
            if campo_id == "senha":
                self.entries[campo_id] = self.gerar_campos_entrada(
                    frame, label, show="*"
                )
            else:
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
            text="Gerenciar Gestores",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.gerenciar_gestor,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.voltar,
        ).pack(side="left", padx=5)

    def gerar_campos_entrada(self, parent, text, show=None):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30, show=show)
        entry.pack(pady=(0, 10))
        return entry
    
    def valida_nome(self, dados):
        nome = dados["nome"].strip()
        if len(nome) < 3 or not all(char.isalpha() or char.isspace() for char in nome):
            messagebox.showerror("Erro", "Nome inválido. Deve conter apenas letras e espaços, mínimo 3 caracteres.")
            return False
        return True

    def valida_cpf(self, dados):
        cpf = dados["cpf"].replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            messagebox.showerror("Erro", "CPF inválido. Deve conter 11 dígitos numéricos.")
            return False
        return True

    def valida_email(self, dados):
        if "@" not in dados["email"] or "." not in dados["email"]:
            messagebox.showerror("Erro", "E-mail inválido. Formato esperado: exemplo@dominio.com")
            return False
        return True

    def valida_senha(self, dados):
        if len(dados["senha"]) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return False
        return True

    def valida_cargo(self, dados):
        cargo = dados["cargo"].strip()
        if len(cargo) < 2 or not all(char.isalpha() or char.isspace() for char in cargo):
            messagebox.showerror("Erro", "Cargo inválido. Deve conter apenas letras e espaços, mínimo 2 caracteres.")
            return False
        return True

    def concluir_cadastro(self):
        """Conclui o cadastro do gestor"""
        # Coletar dados dos campos
        dados = {
            campo_id: self.entries[campo_id].get().strip()
            for campo_id, _ in self.campos
        }
        # Valida Nome
        validador_nome = self.valida_nome(dados)
        if not validador_nome:
            return False
        # Valida CPF
        validador_cpf = self.valida_cpf(dados)
        if not validador_cpf:
            return False
        # Valida email
        validador_email = self.valida_email(dados)
        if not validador_email:
            return False
        # Valida senha
        validador_senha = self.valida_senha(dados)
        if not validador_senha:
            return False
        # Valida cargo
        validador_cargo = self.valida_cargo(dados)
        if not validador_cargo:
            return False

        try:
            # Chamar o controlador para cadastrar o gestor
            resultado = self.__controlador_gestor.cadastrar_gestor(dados)
            if resultado:
                messagebox.showinfo("Sucesso", "Gestor cadastrado com sucesso!")
                # Limpar campos após o cadastro bem-sucedido
                for entry in self.entries.values():
                    if hasattr(entry, "delete"):
                        entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar o gestor")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

    def gerenciar_gestor(self):
        """Abre a tela de gerenciamento de gestores"""
        self.destroy()
        TelaGerenciarGestor(self.__controlador_gestor)

    def voltar(self):
        """Volta para a tela do RH"""
        try:
            self.destroy()
            self.__controlador_gestor.voltar_tela_funcionario_rh()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar para tela de RH: {e}")


class TelaGestorLogado(tk.Tk):
    """Tela para o gestor que fez login - funcionalidades do gestor"""

    def __init__(self, controlador_gestor):
        super().__init__()
        self.title("Gestor - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")
        self.__controlador_gestor = controlador_gestor

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
            text="Analisar Solicitação",
            width=25,
            height=2,
            command=self.abrir_tela_analisar_solicitacao,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            quadro_botoes,
            text="Consultar Colaboradores",
            width=25,
            height=2,
            command=self.consultar_lista_colaboradores,
        ).grid(row=0, column=1, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(rodape, text="Sair", width=20, height=2, command=self.sair).grid(
            row=0, column=0, padx=20
        )

    def sair(self):
        confirm = tk.messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()
            self.__controlador_gestor.voltar_para_tela_sistema()

    def abrir_tela_analisar_solicitacao(self):
        """Abre a tela para analisar solicitações"""
        try:
            self.destroy()
            self.__controlador_gestor.abrir_tela_solicitacao()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir análise de solicitações: {e}")
            TelaGestorLogado(self.__controlador_gestor)

    def consultar_lista_colaboradores(self):
        """Consulta a lista de colaboradores da equipe"""
        try:
            self.destroy()
            self.__controlador_gestor.abrir_tela_equipe()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar colaboradores: {e}")
            TelaGestorLogado(self.__controlador_gestor)


class TelaGerenciarGestor(tk.Tk):
    def __init__(self, controlador_gestor):
        super().__init__()
        self.__controlador_gestor = controlador_gestor
        self.title("Gerenciar Gestores - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(search_frame, text="CPF do gestor:", bg="#dcdcdc").pack(
            side="left", padx=(0, 10)
        )

        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Buscar", command=self.buscar_gestor).pack(
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
            ("senha", "Senha"),
            ("cargo", "Cargo"),
        ]

        for campo_id, label in self.campos_labels:
            tk.Label(self.campos_frame, text=label, bg="#dcdcdc").pack(
                anchor="w", pady=(5, 0)
            )

            # Se for o campo de senha, criar com máscara
            if campo_id == "senha":
                entry = tk.Entry(self.campos_frame, width=40, show="*")
            else:
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
            text="Excluir Gestor",
            command=self.excluir_gestor,
            state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(botoes_frame, text="Voltar", command=self.voltar).pack(
            side="left", padx=5
        )

        # Armazenar CPF do gestor atual
        self.cpf_atual = None

    def buscar_gestor(self):
        """Busca um gestor pelo CPF"""
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar")
            return

        # Validar formato do CPF
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos numéricos!")
            return

        try:
            # Buscar gestor pelo CPF usando o controlador
            gestor = self.__controlador_gestor.buscar_gestor_por_cpf(cpf)

            if gestor:
                # Armazenar CPF do gestor encontrado
                self.cpf_atual = cpf

                # Habilitar campos
                for campo in self.campos.values():
                    campo.config(state="normal")

                # Preencher campos com dados do gestor
                self.campos["nome"].delete(0, tk.END)
                self.campos["nome"].insert(0, gestor.nome)

                self.campos["email"].delete(0, tk.END)
                self.campos["email"].insert(0, gestor.email)

                # Deixar o campo senha vazio para permitir alteração
                self.campos["senha"].delete(0, tk.END)
                self.campos["senha"].insert(0, "")  # Vazio para segurança

                self.campos["cargo"].delete(0, tk.END)
                self.campos["cargo"].insert(0, gestor.cargo)

                # Habilitar botões
                self.btn_editar.config(state="normal")
                self.btn_excluir.config(state="normal")
            else:
                messagebox.showerror("Erro", "Gestor não encontrado!")
                self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar gestor: {str(e)}")

    def valida_nome(self, dados):
        nome = dados["nome"].strip()
        if len(nome) < 3 or not all(char.isalpha() or char.isspace() for char in nome):
            messagebox.showerror("Erro", "Nome inválido. Deve conter apenas letras e espaços, mínimo 3 caracteres.")
            return False
        return True

    def valida_email(self, dados):
        if "@" not in dados["email"] or "." not in dados["email"]:
            messagebox.showerror("Erro", "E-mail inválido. Formato esperado: exemplo@dominio.com")
            return False
        return True

    def valida_senha(self, dados):
        if len(dados["senha"]) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return False
        return True

    def valida_cargo(self, dados):
        cargo = dados["cargo"].strip()
        if len(cargo) < 2 or not all(char.isalpha() or char.isspace() for char in cargo):
            messagebox.showerror("Erro", "Cargo inválido. Deve conter apenas letras e espaços, mínimo 2 caracteres.")
            return False
        return True

    def salvar_edicao(self):
        """Salva as alterações feitas no gestor"""
        if not self.cpf_atual:
            return

        # Coletar dados dos campos
        dados = {campo: entry.get().strip() for campo, entry in self.campos.items()}
        dados["cpf"] = self.cpf_atual  # Incluir o CPF nos dados para o controlador

        validador_nome = self.valida_nome(dados)
        if not validador_nome:
            return False

        validador_email = self.valida_email(dados)
        if not validador_email:
            return False
        
        validador_senha = self.valida_senha(dados)
        if not validador_senha:
            return False
        
        validador_cargo = self.valida_cargo(dados)
        if not validador_cargo:
            return False
        
        try:
            # Chamar controlador para atualizar
            resultado = self.__controlador_gestor.atualizar_gestor(
                self.cpf_atual, dados
            )
            if resultado:
                messagebox.showinfo("Sucesso", "Gestor atualizado com sucesso!")
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o gestor")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    def excluir_gestor(self):
        """Exclui um gestor"""
        if not self.cpf_atual:
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este gestor?"):
            try:
                resultado = self.__controlador_gestor.excluir_gestor(self.cpf_atual)
                if resultado:
                    messagebox.showinfo("Sucesso", "Gestor excluído com sucesso!")
                    self.limpar_campos()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o gestor")
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
        """Volta para a tela de cadastro de gestor"""
        self.destroy()
        TelaGestor(self.__controlador_gestor)
