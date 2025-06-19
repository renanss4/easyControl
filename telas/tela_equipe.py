import tkinter as tk
from tkinter import ttk, messagebox


class TelaEquipe(tk.Tk):
    """Tela de cadastro de equipes"""

    def __init__(self, controlador_equipe):
        super().__init__()
        self.__controlador_equipe = controlador_equipe
        self.title("Cadastrar Equipe")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")

        # Center frame within the larger window
        frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(
            frame,
            text="Cadastro de Equipe",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        ).pack(pady=(0, 20))

        # Nome da equipe
        tk.Label(
            frame, text="Nome da Equipe*", bg="#dcdcdc", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(5, 0))
        self.nome_entry = tk.Entry(frame, width=40)
        self.nome_entry.pack(pady=(0, 10))

        # CPF do Gestor
        gestor_frame = tk.Frame(frame, bg="#dcdcdc")
        gestor_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            gestor_frame,
            text="CPF do Gestor (opcional)",
            bg="#dcdcdc",
            font=("Arial", 10),
        ).pack(anchor="w")

        cpf_gestor_frame = tk.Frame(gestor_frame, bg="#dcdcdc")
        cpf_gestor_frame.pack(fill="x", pady=(5, 0))

        self.cpf_gestor_entry = tk.Entry(cpf_gestor_frame, width=20)
        self.cpf_gestor_entry.pack(side="left", padx=(0, 10))

        tk.Button(
            cpf_gestor_frame,
            text="Ver Gestores Disponíveis",
            command=self.mostrar_gestores_disponiveis,
            font=("Arial", 8),
            bg="#2196F3",
            fg="white",
        ).pack(side="left")

        # Colaboradores
        colaboradores_label_frame = tk.Frame(frame, bg="#dcdcdc")
        colaboradores_label_frame.pack(fill="x", pady=(10, 5))

        tk.Label(
            colaboradores_label_frame,
            text="Colaboradores (opcional)",
            bg="#dcdcdc",
            font=("Arial", 10),
        ).pack(side="left")

        tk.Button(
            colaboradores_label_frame,
            text="Ver Colaboradores Disponíveis",
            command=self.mostrar_colaboradores_disponiveis,
            font=("Arial", 8),
            bg="#4CAF50",
            fg="white",
        ).pack(side="right")

        # Frame para campos de colaboradores
        self.colaboradores_frame = tk.Frame(frame, bg="#dcdcdc")
        self.colaboradores_frame.pack(fill="x", pady=(0, 10))

        # Lista para CPFs de colaboradores
        self.colaboradores_entries = []

        # Adicionar primeiro campo de colaborador
        self.adicionar_campo_colaborador()

        # Botão para adicionar mais colaboradores
        tk.Button(
            frame,
            text="+ Adicionar Colaborador",
            command=self.adicionar_campo_colaborador,
            font=("Arial", 9),
            bg="#FF9800",
            fg="white",
        ).pack(pady=5)

        # Frame para os botões
        botoes_frame = tk.Frame(frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(20, 0))

        tk.Button(
            botoes_frame,
            text="Cadastrar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.cadastrar_equipe,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Gerenciar Equipes",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.gerenciar_equipe,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=15,
            command=self.voltar,
        ).pack(side="left", padx=5)

    def adicionar_campo_colaborador(self):
        """Adiciona um novo campo para CPF de colaborador"""
        frame = tk.Frame(self.colaboradores_frame, bg="#dcdcdc")
        frame.pack(fill="x", pady=2)

        entry = tk.Entry(frame, width=20)
        entry.pack(side="left", padx=(0, 10))

        # Botão para remover (só se não for o primeiro)
        if len(self.colaboradores_entries) > 0:
            btn_remover = tk.Button(
                frame,
                text="Remover",
                command=lambda: self.remover_campo_colaborador(frame, entry),
                font=("Arial", 8),
                bg="#F44336",
                fg="white",
                width=8,
            )
            btn_remover.pack(side="left")

        self.colaboradores_entries.append(entry)

    def remover_campo_colaborador(self, frame, entry):
        """Remove um campo de colaborador"""
        if len(self.colaboradores_entries) > 1:
            self.colaboradores_entries.remove(entry)
            frame.destroy()

    def mostrar_gestores_disponiveis(self):
        """Mostra janela com gestores disponíveis"""
        gestores = self.__controlador_equipe.obter_gestores_sem_equipe()

        if not gestores:
            messagebox.showinfo("Info", "Não há gestores disponíveis para equipes")
            return

        # Criar janela
        janela = tk.Toplevel(self)
        janela.title("Gestores Disponíveis")
        janela.geometry("450x350")
        janela.configure(bg="#dcdcdc")
        janela.transient(self)
        janela.grab_set()

        tk.Label(
            janela,
            text="Gestores Disponíveis",
            font=("Arial", 14, "bold"),
            bg="#dcdcdc",
        ).pack(pady=15)

        # Lista de gestores
        frame_lista = tk.Frame(janela, bg="#dcdcdc")
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

        listbox = tk.Listbox(frame_lista, font=("Arial", 10))
        scrollbar_list = ttk.Scrollbar(
            frame_lista, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=scrollbar_list.set)

        for gestor in gestores:
            listbox.insert(tk.END, f"{gestor['nome']} - {gestor['cpf']}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar_list.pack(side="right", fill="y")

        # Botões
        botoes_frame = tk.Frame(janela, bg="#dcdcdc")
        botoes_frame.pack(pady=15)

        def selecionar_gestor():
            selecao = listbox.curselection()
            if selecao:
                gestor_selecionado = gestores[selecao[0]]
                self.cpf_gestor_entry.delete(0, tk.END)
                self.cpf_gestor_entry.insert(0, gestor_selecionado["cpf"])
                janela.destroy()
            else:
                messagebox.showwarning("Aviso", "Selecione um gestor")

        tk.Button(
            botoes_frame,
            text="Selecionar",
            command=selecionar_gestor,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Cancelar",
            command=janela.destroy,
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            width=12,
        ).pack(side="left", padx=5)

    def mostrar_colaboradores_disponiveis(self):
        """Mostra janela com colaboradores disponíveis"""
        colaboradores = self.__controlador_equipe.obter_colaboradores_sem_equipe()

        if not colaboradores:
            messagebox.showinfo("Info", "Não há colaboradores disponíveis para equipes")
            return

        # Criar janela
        janela = tk.Toplevel(self)
        janela.title("Colaboradores Disponíveis")
        janela.geometry("450x400")
        janela.configure(bg="#dcdcdc")
        janela.transient(self)
        janela.grab_set()

        tk.Label(
            janela,
            text="Colaboradores Disponíveis",
            font=("Arial", 14, "bold"),
            bg="#dcdcdc",
        ).pack(pady=15)

        tk.Label(
            janela,
            text="(Selecione múltiplos colaboradores segurando Ctrl)",
            font=("Arial", 9),
            bg="#dcdcdc",
            fg="gray",
        ).pack()

        # Lista de colaboradores
        frame_lista = tk.Frame(janela, bg="#dcdcdc")
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

        listbox = tk.Listbox(frame_lista, selectmode="multiple", font=("Arial", 10))
        scrollbar_list = ttk.Scrollbar(
            frame_lista, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=scrollbar_list.set)

        for colaborador in colaboradores:
            listbox.insert(tk.END, f"{colaborador['nome']} - {colaborador['cpf']}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar_list.pack(side="right", fill="y")

        # Botões
        botoes_frame = tk.Frame(janela, bg="#dcdcdc")
        botoes_frame.pack(pady=15)

        def selecionar_colaboradores():
            selecoes = listbox.curselection()
            if selecoes:
                # Limpar campos atuais
                for entry in self.colaboradores_entries:
                    entry.delete(0, tk.END)

                # Adicionar campos se necessário
                while len(self.colaboradores_entries) < len(selecoes):
                    self.adicionar_campo_colaborador()

                # Preencher CPFs
                for i, selecao in enumerate(selecoes):
                    if i < len(self.colaboradores_entries):
                        colaborador_selecionado = colaboradores[selecao]
                        self.colaboradores_entries[i].insert(
                            0, colaborador_selecionado["cpf"]
                        )

                janela.destroy()
            else:
                messagebox.showwarning("Aviso", "Selecione pelo menos um colaborador")

        tk.Button(
            botoes_frame,
            text="Selecionar Marcados",
            command=selecionar_colaboradores,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Cancelar",
            command=janela.destroy,
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            width=12,
        ).pack(side="left", padx=5)

    def cadastrar_equipe(self):
        """Cadastra uma nova equipe"""
        # Coletar dados
        nome = self.nome_entry.get().strip()
        cpf_gestor = self.cpf_gestor_entry.get().strip()
        colaboradores_cpf = [
            entry.get().strip()
            for entry in self.colaboradores_entries
            if entry.get().strip()
        ]

        dados = {
            "nome": nome,
            "cpf_gestor": cpf_gestor,
            "colaboradores_cpf": colaboradores_cpf,
        }

        # Chamar controlador
        sucesso, mensagem = self.__controlador_equipe.cadastrar_equipe(dados)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", mensagem)

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.nome_entry.delete(0, tk.END)
        self.cpf_gestor_entry.delete(0, tk.END)

        # Limpar colaboradores, mantendo apenas o primeiro campo
        for entry in self.colaboradores_entries:
            entry.delete(0, tk.END)

        # Remover campos extras
        while len(self.colaboradores_entries) > 1:
            entry = self.colaboradores_entries[-1]
            frame = entry.master
            self.colaboradores_entries.remove(entry)
            frame.destroy()

    def gerenciar_equipe(self):
        """Abre a tela de gerenciamento de equipes"""
        self.destroy()
        TelaGerenciaEquipe(self.__controlador_equipe)

    def voltar(self):
        """Volta para a tela do RH"""
        try:
            self.destroy()
            self.__controlador_equipe.voltar_tela_funcionario_rh()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar para tela de RH: {e}")


class TelaGerenciaEquipe(tk.Tk):
    """Tela de gerenciamento de equipes"""

    def __init__(self, controlador_equipe):
        super().__init__()
        self.__controlador_equipe = controlador_equipe
        self.title("Gerenciar Equipes - EasyControl")
        self.geometry("1000x700")
        self.configure(bg="#dcdcdc")

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Título
        tk.Label(
            main_frame,
            text="Gerenciamento de Equipes",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        ).pack(pady=(0, 20))

        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            search_frame,
            text="Nome da equipe:",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
        ).pack(side="left", padx=(0, 10))

        self.nome_entry = tk.Entry(search_frame, width=25)
        self.nome_entry.pack(side="left", padx=(0, 10))

        tk.Button(
            search_frame,
            text="Buscar",
            command=self.buscar_equipe,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
        ).pack(side="left")

        # Frame para listagem de todas as equipes
        listagem_frame = tk.LabelFrame(
            main_frame,
            text="Equipes Cadastradas",
            bg="#dcdcdc",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        listagem_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Treeview para listar equipes
        colunas = ("nome", "gestor", "total_colaboradores")
        self.tree = ttk.Treeview(
            listagem_frame, columns=colunas, show="headings", height=10
        )

        # Configurar colunas
        self.tree.heading("nome", text="Nome da Equipe")
        self.tree.heading("gestor", text="Gestor")
        self.tree.heading("total_colaboradores", text="Total Colaboradores")

        self.tree.column("nome", width=350)
        self.tree.column("gestor", width=300)
        self.tree.column("total_colaboradores", width=150)

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(
            listagem_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid da tabela e scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar expansão
        listagem_frame.grid_rowconfigure(0, weight=1)
        listagem_frame.grid_columnconfigure(0, weight=1)

        # Bind para seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Frame dos campos de edição
        self.campos_frame = tk.LabelFrame(
            main_frame,
            text="Detalhes da Equipe Selecionada",
            bg="#dcdcdc",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        self.campos_frame.pack(fill="x", pady=(0, 20))

        # Criar campos de edição (inicialmente desabilitados)
        self.campos = {}

        # Nome da equipe
        tk.Label(
            self.campos_frame,
            text="Nome da Equipe:",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.campos["nome"] = tk.Entry(self.campos_frame, width=40, state="disabled")
        self.campos["nome"].grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Gestor
        tk.Label(
            self.campos_frame, text="Gestor:", bg="#dcdcdc", font=("Arial", 10, "bold")
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.campos["gestor"] = tk.Entry(self.campos_frame, width=40, state="disabled")
        self.campos["gestor"].grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Colaboradores (como texto somente leitura)
        tk.Label(
            self.campos_frame,
            text="Colaboradores:",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
        ).grid(row=2, column=0, sticky="nw", padx=5, pady=5)

        colaboradores_frame = tk.Frame(self.campos_frame, bg="#dcdcdc")
        colaboradores_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.colaboradores_text = tk.Text(
            colaboradores_frame, width=50, height=4, state="disabled"
        )
        colaboradores_scrollbar = ttk.Scrollbar(
            colaboradores_frame,
            orient="vertical",
            command=self.colaboradores_text.yview,
        )
        self.colaboradores_text.configure(yscrollcommand=colaboradores_scrollbar.set)

        self.colaboradores_text.pack(side="left", fill="both", expand=True)
        colaboradores_scrollbar.pack(side="right", fill="y")

        # Botões de gerenciamento
        gerenciar_frame = tk.Frame(main_frame, bg="#dcdcdc")
        gerenciar_frame.pack(fill="x", pady=10)

        self.btn_ver_detalhes = tk.Button(
            gerenciar_frame,
            text="Ver Detalhes Completos",
            command=self.ver_detalhes_equipe,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=20,
            state="disabled",
        )
        self.btn_ver_detalhes.pack(side="left", padx=5)

        self.btn_excluir = tk.Button(
            gerenciar_frame,
            text="Excluir Equipe",
            command=self.excluir_equipe,
            font=("Arial", 10),
            bg="#F44336",
            fg="white",
            width=15,
            state="disabled",
        )
        self.btn_excluir.pack(side="left", padx=5)

        tk.Button(
            gerenciar_frame,
            text="Voltar",
            command=self.voltar,
            font=("Arial", 10, "bold"),
            bg="#9E9E9E",
            fg="white",
            width=15,
        ).pack(side="right", padx=5)

        # Carregar equipes iniciais
        self.carregar_equipes()

        # Variável para armazenar equipe selecionada
        self.equipe_selecionada = None

    def buscar_equipe(self):
        """Busca uma equipe pelo nome"""
        nome = self.nome_entry.get().strip()

        if not nome:
            messagebox.showerror("Erro", "Digite um nome para buscar")
            return

        try:
            equipe = self.__controlador_equipe.buscar_equipe_por_nome(nome)

            if equipe:
                # Limpar seleção atual
                self.tree.selection_remove(self.tree.selection())

                # Buscar e selecionar item na árvore
                for item in self.tree.get_children():
                    if self.tree.item(item)["values"][0] == equipe["nome"]:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break

                self.exibir_detalhes_equipe(equipe)
            else:
                messagebox.showerror("Erro", "Equipe não encontrada!")
                self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar equipe: {str(e)}")

    def carregar_equipes(self):
        """Carrega e exibe as equipes na tabela"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            equipes = self.__controlador_equipe.buscar_equipes()

            for equipe in equipes:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        equipe.get("nome", "N/A"),
                        equipe.get("nome_gestor", "N/A"),
                        equipe.get("total_colaboradores", 0),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar equipes: {e}")

    def on_select(self, event):
        """Callback quando uma equipe é selecionada"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            nome_equipe = item["values"][0]
            self.equipe_selecionada = nome_equipe

            # Buscar dados completos da equipe
            equipe = self.__controlador_equipe.buscar_equipe_por_nome(nome_equipe)
            if equipe:
                self.exibir_detalhes_equipe(equipe)

            self.btn_ver_detalhes.config(state="normal")
            self.btn_excluir.config(state="normal")
        else:
            self.limpar_campos()

    def exibir_detalhes_equipe(self, equipe):
        """Exibe os detalhes da equipe nos campos"""
        # Habilitar campos temporariamente
        for campo in self.campos.values():
            campo.config(state="normal")
        self.colaboradores_text.config(state="normal")

        # Limpar campos
        for campo in self.campos.values():
            campo.delete(0, tk.END)
        self.colaboradores_text.delete(1.0, tk.END)

        # Preencher campos
        self.campos["nome"].insert(0, equipe.get("nome", ""))
        self.campos["gestor"].insert(0, equipe.get("nome_gestor", "Sem gestor"))

        # Preencher colaboradores
        colaboradores_nomes = equipe.get("colaboradores_nomes", [])
        if colaboradores_nomes:
            colaboradores_texto = "\n".join(
                [f"• {nome}" for nome in colaboradores_nomes]
            )
        else:
            colaboradores_texto = "Nenhum colaborador cadastrado"

        self.colaboradores_text.insert(1.0, colaboradores_texto)

        # Desabilitar campos novamente
        for campo in self.campos.values():
            campo.config(state="disabled")
        self.colaboradores_text.config(state="disabled")

    def limpar_campos(self):
        """Limpa os campos do formulário"""
        self.equipe_selecionada = None
        self.nome_entry.delete(0, tk.END)

        # Habilitar campos temporariamente para limpar
        for campo in self.campos.values():
            campo.config(state="normal")
            campo.delete(0, tk.END)
            campo.config(state="disabled")

        self.colaboradores_text.config(state="normal")
        self.colaboradores_text.delete(1.0, tk.END)
        self.colaboradores_text.config(state="disabled")

        self.btn_ver_detalhes.config(state="disabled")
        self.btn_excluir.config(state="disabled")

    def ver_detalhes_equipe(self):
        """Mostra detalhes completos da equipe selecionada"""
        if not self.equipe_selecionada:
            return

        equipe = self.__controlador_equipe.buscar_equipe_por_nome(
            self.equipe_selecionada
        )
        if not equipe:
            messagebox.showerror("Erro", "Equipe não encontrada")
            return

        # Criar janela de detalhes
        janela = tk.Toplevel(self)
        janela.title(f"Detalhes Completos - {equipe['nome']}")
        janela.geometry("600x500")
        janela.configure(bg="#dcdcdc")
        janela.transient(self)
        janela.grab_set()

        # Título
        tk.Label(
            janela,
            text=f"Equipe: {equipe['nome']}",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        ).pack(pady=15)

        # Frame para informações
        info_frame = tk.Frame(janela, bg="#dcdcdc")
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Informações da equipe
        tk.Label(
            info_frame,
            text="Informações Gerais",
            font=("Arial", 12, "bold"),
            bg="#dcdcdc",
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Nome: {equipe.get('nome', 'N/A')}",
            font=("Arial", 10),
            bg="#dcdcdc",
        ).pack(anchor="w", pady=2)
        tk.Label(
            info_frame,
            text=f"Gestor: {equipe.get('nome_gestor', 'Sem gestor')}",
            font=("Arial", 10),
            bg="#dcdcdc",
        ).pack(anchor="w", pady=2)
        tk.Label(
            info_frame,
            text=f"Total de Colaboradores: {equipe.get('total_colaboradores', 0)}",
            font=("Arial", 10),
            bg="#dcdcdc",
        ).pack(anchor="w", pady=2)

        # Separador
        tk.Frame(info_frame, height=2, bg="gray").pack(fill="x", pady=10)

        # Lista de colaboradores
        tk.Label(
            info_frame,
            text="Colaboradores da Equipe",
            font=("Arial", 12, "bold"),
            bg="#dcdcdc",
        ).pack(anchor="w")

        # Frame para lista de colaboradores
        colaboradores_frame = tk.Frame(info_frame, bg="#dcdcdc")
        colaboradores_frame.pack(fill="both", expand=True, pady=5)

        listbox_colaboradores = tk.Listbox(colaboradores_frame, font=("Arial", 10))
        scrollbar_colaboradores = ttk.Scrollbar(
            colaboradores_frame, orient="vertical", command=listbox_colaboradores.yview
        )
        listbox_colaboradores.configure(yscrollcommand=scrollbar_colaboradores.set)

        # Adicionar colaboradores à lista
        colaboradores_nomes = equipe.get("colaboradores_nomes", [])
        if colaboradores_nomes:
            for nome in colaboradores_nomes:
                listbox_colaboradores.insert(tk.END, nome)
        else:
            listbox_colaboradores.insert(tk.END, "Nenhum colaborador cadastrado")

        listbox_colaboradores.pack(side="left", fill="both", expand=True)
        scrollbar_colaboradores.pack(side="right", fill="y")

        # Botão para fechar
        tk.Button(
            janela,
            text="Fechar",
            command=janela.destroy,
            font=("Arial", 10, "bold"),
            bg="#9E9E9E",
            fg="white",
            width=15,
        ).pack(pady=15)

    def excluir_equipe(self):
        """Exclui a equipe selecionada"""
        if not self.equipe_selecionada:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente excluir a equipe '{self.equipe_selecionada}'?\n\nEsta ação não pode ser desfeita.",
        ):
            try:
                sucesso, mensagem = self.__controlador_equipe.excluir_equipe(
                    self.equipe_selecionada
                )

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_equipes()
                    self.limpar_campos()
                else:
                    messagebox.showerror("Erro", mensagem)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir equipe: {str(e)}")

    def voltar(self):
        """Volta para a tela de cadastro de equipe"""
        self.destroy()
        TelaEquipe(self.__controlador_equipe)
