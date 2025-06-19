import tkinter as tk
from tkinter import ttk, messagebox


class TelaEquipe(tk.Tk):
    """Tela de gerenciamento de equipes"""

    def __init__(self, controlador_equipe):
        super().__init__()
        self.__controlador_equipe = controlador_equipe

        # Configurações da janela
        self.title("Gerenciar Equipes - EasyControl")
        self.geometry("1000x700")
        self.configure(bg="#dcdcdc")
        self.resizable(True, True)

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

        # Frame para cadastro
        cadastro_frame = tk.LabelFrame(
            main_frame,
            text="Cadastrar Nova Equipe",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
        )
        cadastro_frame.pack(fill="x", pady=(0, 20))

        # Nome da equipe
        tk.Label(
            cadastro_frame,
            text="Nome da Equipe*:",
            bg="#dcdcdc",
            font=("Arial", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nome_entry = tk.Entry(cadastro_frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # CPF do Gestor
        tk.Label(
            cadastro_frame, text="CPF do Gestor:", bg="#dcdcdc", font=("Arial", 9)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cpf_gestor_entry = tk.Entry(cadastro_frame, width=20)
        self.cpf_gestor_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Botão para buscar gestores disponíveis
        tk.Button(
            cadastro_frame,
            text="Ver Gestores Disponíveis",
            command=self.mostrar_gestores_disponiveis,
            font=("Arial", 8),
        ).grid(row=1, column=2, padx=5, pady=5)

        # CPFs dos Colaboradores
        tk.Label(
            cadastro_frame,
            text="CPFs dos Colaboradores:",
            bg="#dcdcdc",
            font=("Arial", 9),
        ).grid(row=2, column=0, sticky="nw", padx=5, pady=5)

        # Frame para colaboradores
        colaboradores_frame = tk.Frame(cadastro_frame, bg="#dcdcdc")
        colaboradores_frame.grid(
            row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w"
        )

        # Lista para CPFs de colaboradores
        self.colaboradores_entries = []

        # Primeiro campo de colaborador
        self.adicionar_campo_colaborador(colaboradores_frame)

        # Botão para adicionar mais colaboradores
        self.btn_adicionar_colaborador = tk.Button(
            colaboradores_frame,
            text="+ Adicionar Colaborador",
            command=lambda: self.adicionar_campo_colaborador(colaboradores_frame),
            font=("Arial", 8),
        )
        self.btn_adicionar_colaborador.pack(pady=5)

        # Botão para ver colaboradores disponíveis
        tk.Button(
            colaboradores_frame,
            text="Ver Colaboradores Disponíveis",
            command=self.mostrar_colaboradores_disponiveis,
            font=("Arial", 8),
        ).pack(pady=2)

        # Botões de ação
        botoes_frame = tk.Frame(cadastro_frame, bg="#dcdcdc")
        botoes_frame.grid(row=3, column=0, columnspan=3, pady=10)

        tk.Button(
            botoes_frame,
            text="Cadastrar Equipe",
            command=self.cadastrar_equipe,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Limpar Campos",
            command=self.limpar_campos,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            width=15,
        ).pack(side="left", padx=5)

        # Frame para listagem
        listagem_frame = tk.LabelFrame(
            main_frame,
            text="Equipes Cadastradas",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
        )
        listagem_frame.pack(fill="both", expand=True)

        # Treeview para listar equipes
        colunas = ("nome", "gestor", "total_colaboradores")
        self.tree = ttk.Treeview(
            listagem_frame, columns=colunas, show="headings", height=10
        )

        # Configurar colunas
        self.tree.heading("nome", text="Nome da Equipe")
        self.tree.heading("gestor", text="Gestor")
        self.tree.heading("total_colaboradores", text="Total Colaboradores")

        self.tree.column("nome", width=300)
        self.tree.column("gestor", width=250)
        self.tree.column("total_colaboradores", width=150)

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(
            listagem_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack da tabela e scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Botões para gerenciar equipes
        gerenciar_frame = tk.Frame(main_frame, bg="#dcdcdc")
        gerenciar_frame.pack(fill="x", pady=10)

        self.btn_ver_detalhes = tk.Button(
            gerenciar_frame,
            text="Ver Detalhes",
            command=self.ver_detalhes_equipe,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=15,
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

    def adicionar_campo_colaborador(self, parent):
        """Adiciona um novo campo para CPF de colaborador"""
        frame = tk.Frame(parent, bg="#dcdcdc")
        frame.pack(fill="x", pady=2)

        entry = tk.Entry(frame, width=15)
        entry.pack(side="left", padx=2)

        # Botão para remover (só se não for o primeiro)
        if len(self.colaboradores_entries) > 0:
            btn_remover = tk.Button(
                frame,
                text="X",
                command=lambda: self.remover_campo_colaborador(frame, entry),
                font=("Arial", 8),
                bg="#F44336",
                fg="white",
                width=2,
            )
            btn_remover.pack(side="left", padx=2)

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
        janela.geometry("400x300")
        janela.configure(bg="#dcdcdc")

        tk.Label(
            janela,
            text="Gestores Disponíveis",
            font=("Arial", 12, "bold"),
            bg="#dcdcdc",
        ).pack(pady=10)

        # Lista de gestores
        frame_lista = tk.Frame(janela, bg="#dcdcdc")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = tk.Listbox(frame_lista)
        scrollbar_list = ttk.Scrollbar(
            frame_lista, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=scrollbar_list.set)

        for gestor in gestores:
            listbox.insert(tk.END, f"{gestor['nome']} - {gestor['cpf']}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar_list.pack(side="right", fill="y")

        # Botão para selecionar
        def selecionar_gestor():
            selecao = listbox.curselection()
            if selecao:
                gestor_selecionado = gestores[selecao[0]]
                self.cpf_gestor_entry.delete(0, tk.END)
                self.cpf_gestor_entry.insert(0, gestor_selecionado["cpf"])
                janela.destroy()

        tk.Button(janela, text="Selecionar", command=selecionar_gestor).pack(pady=10)

    def mostrar_colaboradores_disponiveis(self):
        """Mostra janela com colaboradores disponíveis"""
        colaboradores = self.__controlador_equipe.obter_colaboradores_sem_equipe()

        if not colaboradores:
            messagebox.showinfo("Info", "Não há colaboradores disponíveis para equipes")
            return

        # Criar janela
        janela = tk.Toplevel(self)
        janela.title("Colaboradores Disponíveis")
        janela.geometry("400x400")
        janela.configure(bg="#dcdcdc")

        tk.Label(
            janela,
            text="Colaboradores Disponíveis",
            font=("Arial", 12, "bold"),
            bg="#dcdcdc",
        ).pack(pady=10)

        # Lista de colaboradores
        frame_lista = tk.Frame(janela, bg="#dcdcdc")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        listbox = tk.Listbox(frame_lista, selectmode="multiple")
        scrollbar_list = ttk.Scrollbar(
            frame_lista, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=scrollbar_list.set)

        for colaborador in colaboradores:
            listbox.insert(tk.END, f"{colaborador['nome']} - {colaborador['cpf']}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar_list.pack(side="right", fill="y")

        # Botão para selecionar
        def selecionar_colaboradores():
            selecoes = listbox.curselection()
            if selecoes:
                # Limpar campos atuais
                for entry in self.colaboradores_entries:
                    entry.delete(0, tk.END)

                # Adicionar campos se necessário
                while len(self.colaboradores_entries) < len(selecoes):
                    self.adicionar_campo_colaborador(
                        self.colaboradores_entries[0].master.master
                    )

                # Preencher CPFs
                for i, selecao in enumerate(selecoes):
                    if i < len(self.colaboradores_entries):
                        colaborador_selecionado = colaboradores[selecao]
                        self.colaboradores_entries[i].insert(
                            0, colaborador_selecionado["cpf"]
                        )

                janela.destroy()

        tk.Button(
            janela, text="Selecionar Marcados", command=selecionar_colaboradores
        ).pack(pady=10)

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
            self.carregar_equipes()
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

            self.btn_ver_detalhes.config(state="normal")
            self.btn_excluir.config(state="normal")
        else:
            self.equipe_selecionada = None
            self.btn_ver_detalhes.config(state="disabled")
            self.btn_excluir.config(state="disabled")

    def ver_detalhes_equipe(self):
        """Mostra detalhes da equipe selecionada"""
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
        janela.title(f"Detalhes - {equipe['nome']}")
        janela.geometry("500x400")
        janela.configure(bg="#dcdcdc")

        # Título
        tk.Label(
            janela,
            text=f"Equipe: {equipe['nome']}",
            font=("Arial", 14, "bold"),
            bg="#dcdcdc",
        ).pack(pady=10)

        # Gestor
        gestor_frame = tk.Frame(janela, bg="#dcdcdc")
        gestor_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            gestor_frame, text="Gestor:", font=("Arial", 10, "bold"), bg="#dcdcdc"
        ).pack(side="left")
        tk.Label(
            gestor_frame, text=equipe.get("nome_gestor", "Sem gestor"), bg="#dcdcdc"
        ).pack(side="left", padx=10)

        # Colaboradores
        tk.Label(
            janela, text="Colaboradores:", font=("Arial", 10, "bold"), bg="#dcdcdc"
        ).pack(pady=(10, 5))

        # Lista de colaboradores
        frame_colaboradores = tk.Frame(janela, bg="#dcdcdc")
        frame_colaboradores.pack(fill="both", expand=True, padx=20, pady=10)

        listbox_colaboradores = tk.Listbox(frame_colaboradores)
        scrollbar_colaboradores = ttk.Scrollbar(
            frame_colaboradores, orient="vertical", command=listbox_colaboradores.yview
        )
        listbox_colaboradores.configure(yscrollcommand=scrollbar_colaboradores.set)

        for nome in equipe.get("colaboradores_nomes", []):
            listbox_colaboradores.insert(tk.END, nome)

        if not equipe.get("colaboradores_nomes"):
            listbox_colaboradores.insert(tk.END, "Nenhum colaborador cadastrado")

        listbox_colaboradores.pack(side="left", fill="both", expand=True)
        scrollbar_colaboradores.pack(side="right", fill="y")

        tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    def excluir_equipe(self):
        """Exclui a equipe selecionada"""
        if not self.equipe_selecionada:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente excluir a equipe '{self.equipe_selecionada}'?",
        ):
            sucesso, mensagem = self.__controlador_equipe.excluir_equipe(
                self.equipe_selecionada
            )

            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.carregar_equipes()
                self.equipe_selecionada = None
                self.btn_ver_detalhes.config(state="disabled")
                self.btn_excluir.config(state="disabled")
            else:
                messagebox.showerror("Erro", mensagem)

    def voltar(self):
        """Volta para a tela anterior"""
        self.destroy()
        self.__controlador_equipe.voltar_tela_funcionario_rh()
