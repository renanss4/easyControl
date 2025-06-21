import tkinter as tk
from tkinter import messagebox


class TelaRH(tk.Tk):
    def __init__(self, controlador_funcionario_rh):
        super().__init__()
        self.__controlador_funcionario_rh = controlador_funcionario_rh

        self.title("RH - EasyControl")
        self.geometry("800x700")
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
            # Destroy this window first
            self.destroy()
            self.__controlador_funcionario_rh._ControladorFuncionarioRH__tela_funcionario_rh = None
            self.__controlador_funcionario_rh.abrir_tela_colaborador()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de colaborador: {e}")
            # If there's an error, reopen this window
            TelaRH(self.__controlador_funcionario_rh)

    def abrir_cadastro_gestor(self):
        """Abre a tela de cadastro de gestor"""
        try:
            # Destroy this window first
            self.destroy()
            self.__controlador_funcionario_rh.abrir_tela_gestor()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de gestor: {e}")
            # If there's an error, reopen this window
            TelaRH(self.__controlador_funcionario_rh)

    def abrir_cadastro_funcionario_rh(self):
        """Abre a tela de cadastro de funcionário RH"""
        try:
            # Destroy this window first
            self.destroy()
            TelaCadastrarRH(self.__controlador_funcionario_rh)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de RH: {e}")
            # If there's an error, reopen this window
            TelaRH(self.__controlador_funcionario_rh)

    def abrir_cadastro_solicitacao(self):
        """Abre a tela de cadastro de solicitação"""
        try:
            # Destroy this window first
            self.destroy()
            self.__controlador_funcionario_rh.abrir_tela_solicitacao()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de solicitação: {e}")
            # If there's an error, reopen this window
            TelaRH(self.__controlador_funcionario_rh)

    def abrir_cadastro_equipe(self):
        """Abre a tela de cadastro de equipe"""
        try:
            # Destroy this window first
            self.destroy()
            self.__controlador_funcionario_rh.abrir_tela_equipe()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir cadastro de equipe: {e}")
            # If there's an error, reopen this window
            TelaRH(self.__controlador_funcionario_rh)

    def gerar_relatorio_ferias(self):
        """Gera relatório de férias"""
        try:
            messagebox.showinfo(
                "Info", "Funcionalidade de relatório ainda não implementada"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

    def sair(self):
        confirm = messagebox.askyesno("Sair", "Deseja realmente sair?")
        if confirm:
            self.destroy()
            self.__controlador_funcionario_rh.voltar_para_tela_sistema()


class TelaCadastrarRH(tk.Tk):
    def __init__(self, controlador_funcionario_rh):
        super().__init__()
        self.__controlador_funcionario_rh = controlador_funcionario_rh
        self.title("Cadastrar Funcionário RH")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Center frame within the larger window
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        label_title = tk.Label(
            frame, text="Cadastro de RH", font=("Arial", 16, "bold"), bg="#dcdcdc"
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
                self.entries[campo_id] = self.gerar_campos_entradas(
                    frame, label, show="*"
                )
            else:
                self.entries[campo_id] = self.gerar_campos_entradas(frame, label)

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
            text="Gerenciar RH",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.gerenciar_usuario_rh,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.voltar,
        ).pack(side="left", padx=5)

    def gerar_campos_entradas(self, parent, text, show=None):
        """Cria um par de label e entry e retorna o entry."""
        tk.Label(parent, text=text, bg="#dcdcdc").pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(parent, width=30, show=show)
        entry.pack(pady=(0, 10))
        return entry

    def concluir_cadastro(self):
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
            # Chamar o controller para criar o usuário RH
            self.__controlador_funcionario_rh.cadastrar_funcionario_rh(
                nome=dados["nome"],
                cpf=dados["cpf"],
                email=dados["email"],
                senha=dados["senha"],
                cargo=dados["cargo"],
            )
            messagebox.showinfo("Sucesso", "Funcionário RH cadastrado com sucesso!")
            self.voltar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

    def gerenciar_usuario_rh(self):
        # Destroy this window first, then open the management window
        self.destroy()
        TelaGerenciarRH(self.__controlador_funcionario_rh)

    def voltar(self):
        # Destroy this window and return to the RH main screen
        self.destroy()
        TelaRH(self.__controlador_funcionario_rh)


class TelaGerenciarRH(tk.Tk):
    def __init__(self, controlador_funcionario_rh):
        super().__init__()
        self.__controlador_funcionario_rh = controlador_funcionario_rh
        self.title("Gerenciar Funcionários de RH - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(search_frame, text="CPF do usuário:", bg="#dcdcdc").pack(
            side="left", padx=(0, 10)
        )

        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Buscar", command=self.buscar_usuario).pack(
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
            text="Excluir Usuário",
            command=self.excluir_usuario,
            state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=5)

        # Botão Voltar
        tk.Button(botoes_frame, text="Voltar", command=self.voltar).pack(
            side="left", padx=5
        )

        # Armazenar CPF do usuário atual
        self.cpf_atual = None

    def buscar_usuario(self):
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar")
            return

        try:
            # Implementar no controlador
            usuario = self.__controlador_funcionario_rh.buscar_funcionario_rh_por_cpf(
                cpf
            )

            if usuario:
                # Armazenar CPF do usuário encontrado
                self.cpf_atual = cpf

                # Habilitar campos
                for campo in self.campos.values():
                    campo.config(state="normal")

                # Preencher campos com dados do usuário
                self.campos["nome"].delete(0, tk.END)
                self.campos["nome"].insert(0, usuario.nome)

                self.campos["email"].delete(0, tk.END)
                self.campos["email"].insert(0, usuario.email)

                # Deixar o campo senha vazio para permitir alteração
                self.campos["senha"].delete(0, tk.END)
                self.campos["senha"].insert(0, "")  # Vazio para segurança

                self.campos["cargo"].delete(0, tk.END)
                self.campos["cargo"].insert(0, usuario.cargo)

                # Habilitar botões
                self.btn_editar.config(state="normal")
                self.btn_excluir.config(state="normal")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado!")
                self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {str(e)}")

    def salvar_edicao(self):
        if not self.cpf_atual:
            return

        # Coletar dados dos campos
        dados = {campo: entry.get().strip() for campo, entry in self.campos.items()}

        # Validar dados
        if not dados["nome"] or not dados["email"] or not dados["cargo"]:
            messagebox.showerror(
                "Erro de Validação",
                "Nome, email e cargo são obrigatórios",
            )
            return

        # Validar email básico
        if "@" not in dados["email"] or "." not in dados["email"]:
            messagebox.showerror("Erro", "Email inválido!")
            return

        # Validar senha se foi fornecida
        if dados["senha"] and len(dados["senha"]) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return

        try:
            # Implementar no controlador
            self.__controlador_funcionario_rh.atualizar_funcionario_rh(
                self.cpf_atual, dados
            )
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar usuário: {str(e)}")

    def excluir_usuario(self):
        if not self.cpf_atual:
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este usuário?"):
            try:
                # Implementar no controlador
                self.__controlador_funcionario_rh.excluir_funcionario_rh(self.cpf_atual)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")

    def limpar_campos(self):
        self.cpf_atual = None
        self.cpf_entry.delete(0, tk.END)

        for entry in self.campos.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="disabled")

        self.btn_editar.config(state="disabled")
        self.btn_excluir.config(state="disabled")

    def voltar(self):
        # Destroy this window and return to the cadastro RH screen
        self.destroy()
        TelaCadastrarRH(self.__controlador_funcionario_rh)
