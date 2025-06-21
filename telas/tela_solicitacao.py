import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import timedelta, date, datetime


class TelaSolicitacao(tk.Tk):
    """Tela inicial de solicitação - direcionamento baseado no tipo de usuário"""

    def __init__(self, controlador_solicitacao):
        super().__init__()
        self.title("Solicitação - EasyControl")
        self.geometry("800x700")
        self.configure(bg="#dcdcdc")
        self.__controlador_solicitacao = controlador_solicitacao

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

        # Verificar se é RH ou Gestor logado para mostrar opções diferentes
        usuario_logado = (
            self.__controlador_solicitacao.controlador_sistema.usuario_logado
        )

        if hasattr(usuario_logado, "__class__") and "FuncionarioRH" in str(
            usuario_logado.__class__
        ):
            # Opções para RH
            tk.Button(
                quadro_botoes,
                text="Cadastrar Solicitação",
                width=25,
                height=2,
                command=self.abrir_cadastro_solicitacao,
            ).grid(row=0, column=0, padx=10, pady=5)

            tk.Button(
                quadro_botoes,
                text="Gerenciar Solicitações",
                width=25,
                height=2,
                command=self.abrir_gerenciar_solicitacoes,
            ).grid(row=0, column=1, padx=10, pady=5)
        else:
            # Opções para Gestor
            tk.Button(
                quadro_botoes,
                text="Analisar Solicitações",
                width=25,
                height=2,
                command=self.abrir_analisar_solicitacoes,
            ).grid(row=0, column=0, padx=10, pady=5)

        rodape = tk.Frame(self, bg="#dcdcdc")
        rodape.pack(pady=20)

        tk.Button(rodape, text="Voltar", width=20, height=2, command=self.voltar).grid(
            row=0, column=0, padx=20
        )

    def abrir_cadastro_solicitacao(self):
        """Abre a tela de cadastro de solicitação (RH)"""
        self.destroy()
        TelaCadastrarSolicitacao(self.__controlador_solicitacao)

    def abrir_gerenciar_solicitacoes(self):
        """Abre a tela de gerenciamento de solicitações (RH)"""
        self.destroy()
        TelaGerenciarSolicitacoes(self.__controlador_solicitacao)

    def abrir_analisar_solicitacoes(self):
        """Abre a tela de análise de solicitações (Gestor)"""
        self.destroy()
        TelaAnalisarSolicitacao(self.__controlador_solicitacao)

    def voltar(self):
        """Volta para a tela anterior baseado no tipo de usuário"""
        usuario_logado = (
            self.__controlador_solicitacao.controlador_sistema.usuario_logado
        )

        if hasattr(usuario_logado, "__class__") and "FuncionarioRH" in str(
            usuario_logado.__class__
        ):
            self.destroy()
            self.__controlador_solicitacao.voltar_tela_funcionario_rh()
        else:
            self.destroy()
            self.__controlador_solicitacao.voltar_tela_gestor()


class TelaCadastrarSolicitacao(tk.Tk):
    """Tela de cadastro de solicitação de férias (RH)"""

    def __init__(self, controlador_solicitacao):
        super().__init__()
        self.__controlador_solicitacao = controlador_solicitacao
        self.title("Cadastro de Solicitação de Férias")
        self.configure(bg="#dcdcdc")
        self.geometry("900x600")

        # Criar canvas com scrollbar
        self.canvas = tk.Canvas(self, bg="#dcdcdc")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#dcdcdc")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame principal com borda - CONTEÚDO CENTRALIZADO
        borda_frame = tk.Frame(
            self.scrollable_frame, bg="#dcdcdc", bd=2, relief="groove", padx=20, pady=20
        )
        borda_frame.pack(padx=50, pady=50)

        # Título da janela - CENTRALIZADO
        tk.Label(
            borda_frame,
            text="Solicitação de Férias",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc",
        ).pack(pady=(0, 20))

        # Container dos campos
        campos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        campos_frame.pack(pady=10, fill="x")

        # CPF
        tk.Label(
            campos_frame,
            text="CPF do Colaborador",
            font=("Arial", 10, "bold"),
            bg="#dcdcdc",
            anchor="w",
        ).pack(fill="x", padx=20, pady=(10, 2))
        self.cpf_entry = tk.Entry(campos_frame, width=30, justify="center")
        self.cpf_entry.pack(padx=20)

        # Checkbox para parcelamento
        self.var_parcelamento = tk.BooleanVar()
        checkbox_frame = tk.Frame(campos_frame, bg="#dcdcdc")
        checkbox_frame.pack(pady=10)

        tk.Checkbutton(
            checkbox_frame,
            text="Parcelamento de Férias",
            variable=self.var_parcelamento,
            bg="#dcdcdc",
            font=("Arial", 10),
            command=self.toggle_parcelamento,
        ).pack()

        # Adicionar contador de dias - CENTRALIZADO
        self.label_total_dias = tk.Label(
            campos_frame,
            text="Total de dias: 0/30",
            font=("Arial", 10, "bold"),
            bg="#dcdcdc",
        )
        self.label_total_dias.pack(pady=5)

        # Frame para períodos
        self.periodos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        self.periodos_frame.pack(fill="x", padx=20, pady=10)

        # Lista para armazenar os widgets de período
        self.periodos = []

        # Adicionar primeiro período
        self.adicionar_periodo()

        # Botão para adicionar mais períodos - CENTRALIZADO
        btn_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        btn_frame.pack(pady=5)

        self.btn_adicionar_periodo = tk.Button(
            btn_frame,
            text="Adicionar Período",
            command=self.adicionar_periodo,
            state="disabled",
        )
        self.btn_adicionar_periodo.pack()

        # Frame para os botões principais - CENTRALIZADO
        botoes_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(20, 0))

        tk.Button(
            botoes_frame,
            text="Enviar solicitação",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.concluir_solicitacao,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Gerenciar Solicitações",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.gerenciar_solicitacao,
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar,
        ).pack(side="left", padx=5)

        # Configurar pack do canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def toggle_parcelamento(self):
        """Habilita/desabilita opções de parcelamento"""
        if self.var_parcelamento.get():
            self.btn_adicionar_periodo.config(state="normal")
        else:
            self.btn_adicionar_periodo.config(state="disabled")
            # Remover períodos extras de forma segura
            while len(self.periodos) > 1:
                frame, _, _ = self.periodos[-1]
                frame.destroy()
                self.periodos.pop()

    def criar_periodo_widget(self):
        """Cria um widget de período com data início e fim"""
        frame = tk.Frame(self.periodos_frame, bg="#dcdcdc", bd=1, relief="groove")
        frame.pack(fill="x", pady=5)

        # Título do período
        tk.Label(
            frame,
            text=f"Período {len(self.periodos) + 1}",
            font=("Arial", 9, "bold"),
            bg="#dcdcdc",
        ).pack(pady=5)

        # Container para as datas
        datas_frame = tk.Frame(frame, bg="#dcdcdc")
        datas_frame.pack(pady=5)

        # Data início - com data mínima de hoje + 30 dias
        tk.Label(datas_frame, text="Início:", bg="#dcdcdc").pack(side="left", padx=5)
        data_minima = date.today() + timedelta(weeks=52)  # 1 ano de antecedência
        data_inicio = DateEntry(
            datas_frame,
            width=12,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
            mindate=data_minima,
        )
        data_inicio.pack(side="left", padx=5)

        # Data fim
        tk.Label(datas_frame, text="Fim:", bg="#dcdcdc").pack(side="left", padx=5)
        data_fim = DateEntry(
            datas_frame,
            width=12,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
            mindate=data_minima,
        )
        data_fim.pack(side="left", padx=5)

        # Label para dias do período
        label_dias = tk.Label(frame, text="Dias: 0", bg="#dcdcdc")
        label_dias.pack(pady=2)

        # Bind para atualizar dias quando as datas mudarem
        data_inicio.bind(
            "<<DateEntrySelected>>",
            lambda e: self.atualizar_dias(data_inicio, data_fim, label_dias),
        )
        data_fim.bind(
            "<<DateEntrySelected>>",
            lambda e: self.atualizar_dias(data_inicio, data_fim, label_dias),
        )

        # Botão remover
        btn_remover = tk.Button(
            frame, text="Remover", command=lambda: self.remover_periodo(frame)
        )
        btn_remover.pack(pady=5)

        return frame, data_inicio, data_fim

    def atualizar_dias(self, data_inicio, data_fim, label_dias):
        """Atualiza o contador de dias para um período"""
        try:
            inicio = datetime.strptime(data_inicio.get(), "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim.get(), "%Y-%m-%d").date()

            dias = (fim - inicio).days + 1
            label_dias.config(text=f"Dias: {dias}")

            # Atualizar total de dias
            total = self.calcular_total_dias()
            self.label_total_dias.config(
                text=f"Total de dias: {total}/30", fg="red" if total > 30 else "black"
            )
        except ValueError:
            pass

    def calcular_total_dias(self) -> int:
        """Calcula o total de dias de todos os períodos"""
        total = 0
        for _, data_inicio, data_fim in self.periodos:
            try:
                inicio = datetime.strptime(data_inicio.get(), "%Y-%m-%d").date()
                fim = datetime.strptime(data_fim.get(), "%Y-%m-%d").date()
                total += (fim - inicio).days + 1
            except ValueError:
                continue
        return total

    def adicionar_periodo(self):
        """Adiciona um novo período à solicitação"""
        if len(self.periodos) >= 3:
            messagebox.showwarning(
                "Limite atingido", "Máximo de 3 períodos permitidos."
            )
            return

        periodo_widget = self.criar_periodo_widget()
        self.periodos.append(periodo_widget)

        if len(self.periodos) >= 3:
            self.btn_adicionar_periodo.config(state="disabled")

    def remover_periodo(self, frame):
        """Remove um período da solicitação"""
        if len(self.periodos) > 1:
            idx = next(i for i, (f, _, _) in enumerate(self.periodos) if f == frame)
            frame.destroy()
            self.periodos.pop(idx)
            self.btn_adicionar_periodo.config(state="normal")

            # Atualizar números dos períodos
            for i, (f, _, _) in enumerate(self.periodos, 1):
                for widget in f.winfo_children():
                    if isinstance(widget, tk.Label) and "Período" in widget.cget(
                        "text"
                    ):
                        widget.config(text=f"Período {i}")

    def concluir_solicitacao(self):
        """Processa e envia a solicitação - SEM VALIDAÇÕES"""
        cpf = self.cpf_entry.get().strip()

        # Coletar períodos
        periodos = []
        for _, data_inicio, data_fim in self.periodos:
            try:
                inicio = datetime.strptime(data_inicio.get(), "%Y-%m-%d").date()
                fim = datetime.strptime(data_fim.get(), "%Y-%m-%d").date()
                periodos.append((inicio, fim))
            except ValueError:
                messagebox.showerror("Erro", "Datas inválidas")
                return

        # Preparar dados
        dados_solicitacao = {
            "cpf_colaborador": cpf,
            "periodos": periodos,
            "parcelamento": self.var_parcelamento.get(),
        }

        # Chamar controlador - ELE FAZ TODAS AS VALIDAÇÕES
        sucesso = self.__controlador_solicitacao.cadastrar_solicitacao(
            dados_solicitacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", "Solicitação enviada com sucesso!")
            self.voltar()
        else:
            messagebox.showerror("Erro", "Erro ao enviar solicitação. Verifique os dados.")

    def gerenciar_solicitacao(self):
        """Abre a tela de gerenciamento de solicitações"""
        self.destroy()
        TelaGerenciarSolicitacoes(self.__controlador_solicitacao)

    def voltar(self):
        """Volta para a tela do funcionário RH"""
        self.destroy()
        self.__controlador_solicitacao.voltar_tela_funcionario_rh()


class TelaGerenciarSolicitacoes(tk.Tk):
    """Tela de gerenciamento de solicitações (RH)"""

    def __init__(self, controlador_solicitacao):
        super().__init__()
        self.__controlador_solicitacao = controlador_solicitacao

        # Configurações da janela
        self.title("Gerenciar Solicitações - EasyControl")
        self.geometry("1200x700")
        self.configure(bg="#dcdcdc")
        self.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(self, bg="#dcdcdc", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Frame de busca
        search_frame = tk.Frame(main_frame, bg="#dcdcdc")
        search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            search_frame,
            text="CPF do colaborador:",
            bg="#dcdcdc",
            font=("Arial", 10, "bold"),
        ).pack(side="left", padx=(0, 10))

        self.cpf_entry = tk.Entry(search_frame, width=15)
        self.cpf_entry.pack(side="left", padx=(0, 10))

        tk.Button(search_frame, text="Buscar", command=self.buscar_solicitacoes).pack(
            side="left"
        )

        tk.Button(
            search_frame, text="Mostrar Todas", command=self.mostrar_todas_solicitacoes
        ).pack(side="left", padx=10)

        # Frame da tabela
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "protocolo",
                "nome",
                "cpf",
                "data_solicitacao",
                "periodos",
                "status",
            ),
            show="headings",
            selectmode="browse",
        )

        # Configurar colunas
        self.tree.heading("protocolo", text="Protocolo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("data_solicitacao", text="Data Solicitação")
        self.tree.heading("periodos", text="Períodos")
        self.tree.heading("status", text="Status")

        self.tree.column("protocolo", width=150)
        self.tree.column("nome", width=200)
        self.tree.column("cpf", width=120)
        self.tree.column("data_solicitacao", width=120)
        self.tree.column("periodos", width=300)
        self.tree.column("status", width=100)

        # Adicionar scrollbars
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(
            table_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Frame dos botões
        botoes_frame = tk.Frame(main_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=20)

        self.btn_cancelar = tk.Button(
            botoes_frame,
            text="Cancelar Solicitação",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.cancelar_solicitacao,
            state="disabled",
        )
        self.btn_cancelar.pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar,
        ).pack(side="left", padx=5)

        # Bind para seleção na tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Carregar dados iniciais
        self.mostrar_todas_solicitacoes()

    def on_select(self, event):
        """Callback quando uma linha é selecionada na tabela"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            status = item["values"][5] if len(item["values"]) > 5 else ""
            # Habilitar botão apenas se status for pendente
            self.btn_cancelar.config(
                state="normal" if status.lower() == "pendente" else "disabled"
            )
        else:
            self.btn_cancelar.config(state="disabled")

    def mostrar_todas_solicitacoes(self):
        """Exibe todas as solicitações na tabela"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            solicitacoes = self.__controlador_solicitacao.buscar_solicitacoes()

            for sol in solicitacoes:
                periodos = self.formatar_periodos(sol)

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        sol.get("protocolo", "N/A"),
                        sol["pessoa"].get("nome", "Nome não encontrado"),
                        sol["pessoa"].get("cpf", "N/A"),
                        sol.get("data_solicitacao", "N/A"),
                        periodos,
                        sol.get("status", "N/A"),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar solicitações: {e}")

    def buscar_solicitacoes(self):
        """Busca e exibe solicitações de um colaborador específico - SEM VALIDAÇÃO"""
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar")
            return

        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            solicitacoes = self.__controlador_solicitacao.buscar_solicitacoes_por_cpf(
                cpf
            )

            if solicitacoes:
                for sol in solicitacoes:
                    periodos = self.formatar_periodos(sol)

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            sol.get("protocolo", "N/A"),
                            sol.get("nome_colaborador", "Nome não encontrado"),
                            sol.get("cpf_colaborador", "N/A"),
                            sol.get("data_solicitacao", "N/A"),
                            periodos,
                            sol.get("status", "N/A"),
                        ),
                    )
            else:
                messagebox.showinfo(
                    "Info", "Nenhuma solicitação encontrada para este CPF."
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar solicitações: {e}")

    def formatar_periodos(self, solicitacao):
        """Formata os períodos de uma solicitação para exibição"""
        if "periodos" in solicitacao and isinstance(solicitacao["periodos"], list):
            periodos_formatados = []
            for p in solicitacao["periodos"]:
                inicio = p.get("DATA_INICIO", "N/A")
                fim = p.get("DATA_FIM", "N/A")
                periodos_formatados.append(f"{inicio} a {fim}")
            return " | ".join(periodos_formatados)

        # Fallback para formato antigo
        inicio = solicitacao.get("DATA_INICIO", "N/A")
        fim = solicitacao.get("DATA_FIM", "N/A")
        return f"{inicio} a {fim}"

    def cancelar_solicitacao(self):
        """Cancela a solicitação selecionada - SEM VALIDAÇÃO"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        protocolo = item["values"][0]

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente cancelar esta solicitação?"
        ):
            # Chamar controlador - ELE FAZ TODAS AS VALIDAÇÕES
            sucesso = self.__controlador_solicitacao.cancelar_solicitacao(
                protocolo
            )

            if sucesso:
                messagebox.showinfo("Sucesso", "Cancelo de solicitação realizado com sucesso.")
                self.mostrar_todas_solicitacoes()  # Recarregar tabela
            else:
                messagebox.showerror("Erro", "Erro ao cancelar solicitação. Verifique o protocolo.")

    def voltar(self):
        """Volta para a tela de cadastro de solicitação"""
        self.destroy()
        TelaCadastrarSolicitacao(self.__controlador_solicitacao)


class TelaAnalisarSolicitacao(tk.Tk):
    """Tela de análise de solicitações (Gestor)"""

    def __init__(self, controlador_solicitacao):
        super().__init__()
        self.__controlador_solicitacao = controlador_solicitacao

        # Obter informações da equipe do gestor logado
        self.usuario_logado = (
            self.__controlador_solicitacao.controlador_sistema.usuario_logado
        )
        breakpoint()
        self.cpf_gestor = (
            getattr(self.usuario_logado, "cpf", None) if self.usuario_logado else None
        )

        # Configurações da janela
        self.title("Analisar Solicitação")
        self.geometry("900x600")
        self.configure(bg="#dcdcdc")
        self.resizable(True, True)

        # Frame de busca
        busca_frame = tk.Frame(self, bg="#dcdcdc", padx=10, pady=10)
        busca_frame.pack(fill="x")

        tk.Label(busca_frame, text="CPF do Colaborador", bg="#dcdcdc").pack(
            side="left", padx=5
        )
        self.cpf_entry = tk.Entry(busca_frame, width=15)
        self.cpf_entry.pack(side="left", padx=5)

        tk.Button(busca_frame, text="Buscar", command=self.buscar_solicitacoes).pack(
            side="left", padx=5
        )

        tk.Button(
            busca_frame, text="Mostrar Todos", command=self.mostrar_todas_solicitacoes
        ).pack(side="left", padx=5)

        # Frame da tabela
        tabela_frame = tk.Frame(self, padx=10)
        tabela_frame.pack(fill="both", expand=True)

        # Criar tabela de solicitações
        colunas = ("protocolo", "nome", "cpf", "data_solicitacao", "periodos", "status")
        self.tabela = ttk.Treeview(
            tabela_frame, columns=colunas, show="headings", selectmode="browse"
        )

        # Definir cabeçalhos
        self.tabela.heading("protocolo", text="Protocolo")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("data_solicitacao", text="Data Solicitação")
        self.tabela.heading("periodos", text="Períodos")
        self.tabela.heading("status", text="Status")

        # Definir larguras das colunas
        self.tabela.column("protocolo", width=120)
        self.tabela.column("nome", width=150)
        self.tabela.column("cpf", width=100)
        self.tabela.column("data_solicitacao", width=100)
        self.tabela.column("periodos", width=180)
        self.tabela.column("status", width=80)

        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(
            tabela_frame, orient="vertical", command=self.tabela.yview
        )
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        # Vincular evento de seleção
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_solicitacao)

        # Frame para informações da equipe
        info_equipe_frame = tk.Frame(
            self, bg="#dcdcdc", padx=10, pady=10, relief="groove", bd=1
        )
        info_equipe_frame.pack(fill="x", padx=10, pady=5)

        self.info_equipe_label = tk.Label(
            info_equipe_frame,
            text="Informações da equipe carregadas",
            bg="#dcdcdc",
            font=("Arial", 11, "bold"),
        )
        self.info_equipe_label.pack(pady=10)

        # Frame dos botões de ação
        acoes_frame = tk.Frame(self, bg="#dcdcdc", padx=10, pady=10)
        acoes_frame.pack(fill="x")

        self.btn_aprovar = tk.Button(
            acoes_frame,
            text="Aprovar solicitação",
            command=self.aprovar_solicitacao,
            state="disabled",
        )
        self.btn_aprovar.pack(side="left", padx=10)

        self.btn_reprovar = tk.Button(
            acoes_frame,
            text="Reprovar Solicitação",
            command=self.reprovar_solicitacao,
            state="disabled",
        )
        self.btn_reprovar.pack(side="left", padx=10)

        tk.Button(acoes_frame, text="Voltar", command=self.voltar).pack(
            side="left", padx=10
        )

        # Carregar dados iniciais
        self.mostrar_todas_solicitacoes()

    def mostrar_todas_solicitacoes(self):
        """Mostra todas as solicitações da equipe do gestor"""
        self.limpar_tabela()

        try:
            solicitacoes = self.__controlador_solicitacao.buscar_solicitacoes_equipe(
                self.cpf_gestor
            )
            self.preencher_tabela(solicitacoes)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar solicitações: {e}")

    def buscar_solicitacoes(self):
        """Busca solicitações de um colaborador específico - SEM VALIDAÇÃO"""
        cpf = self.cpf_entry.get().strip()

        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar")
            return

        self.limpar_tabela()

        try:
            solicitacoes = self.__controlador_solicitacao.buscar_solicitacoes_por_cpf(
                cpf
            )
            self.preencher_tabela(solicitacoes)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar solicitações: {e}")

    def preencher_tabela(self, solicitacoes):
        """Preenche a tabela com as solicitações"""
        self.limpar_tabela()

        for sol in solicitacoes:
            # Formatar períodos
            if "periodos" in sol and isinstance(sol["periodos"], list):
                periodos_formatados = []
                for p in sol["periodos"]:
                    inicio = p.get("data_inicio", "N/A")
                    fim = p.get("data_fim", "N/A")
                    periodos_formatados.append(f"{inicio} a {fim}")
                periodos_texto = " | ".join(periodos_formatados)
            else:
                inicio = sol.get("data_inicio", "N/A")
                fim = sol.get("data_fim", "N/A")
                periodos_texto = f"{inicio} a {fim}"

            status = sol.get("status", "N/A")

            self.tabela.insert(
                "",
                "end",
                values=(
                    sol.get("protocolo", "N/A"),
                    sol.get("nome_colaborador", "Nome não encontrado"),
                    sol.get("cpf_colaborador", "N/A"),
                    sol.get("data_solicitacao", "N/A"),
                    periodos_texto,
                    status,
                ),
                tags=(status,) if status else (),
            )

        # Configurar cores para status
        self.tabela.tag_configure("pendente", background="#FFFFCC")
        self.tabela.tag_configure("aprovado", background="#CCFFCC")
        self.tabela.tag_configure("rejeitado", background="#FFCCCC")
        self.tabela.tag_configure("cancelada", background="#E0E0E0")

    def limpar_tabela(self):
        """Limpa a tabela"""
        for item in self.tabela.get_children():
            self.tabela.delete(item)

    def selecionar_solicitacao(self, event):
        """Ação ao selecionar uma solicitação na tabela"""
        selecionados = self.tabela.selection()

        if selecionados:
            item = self.tabela.item(selecionados[0])
            status = item["values"][5] if len(item["values"]) > 5 else ""

            # Habilitar/desabilitar botões apenas se status for pendente
            if status.lower() == "pendente":
                self.btn_aprovar.config(state="normal")
                self.btn_reprovar.config(state="normal")
            else:
                self.btn_aprovar.config(state="disabled")
                self.btn_reprovar.config(state="disabled")
        else:
            self.btn_aprovar.config(state="disabled")
            self.btn_reprovar.config(state="disabled")

    def aprovar_solicitacao(self):
        """Aprova a solicitação selecionada - SEM VALIDAÇÃO"""
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        item = self.tabela.item(selecionados[0])
        protocolo = item["values"][0]

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente APROVAR esta solicitação de férias?"
        ):
            # Chamar controlador - ELE FAZ TODAS AS VALIDAÇÕES
            sucesso, mensagem = self.__controlador_solicitacao.aprovar_solicitacao(
                protocolo
            )

            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.mostrar_todas_solicitacoes()  # Recarregar tabela
            else:
                messagebox.showerror("Erro", mensagem)

    def reprovar_solicitacao(self):
        """Reprova a solicitação selecionada - SEM VALIDAÇÃO"""
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        item = self.tabela.item(selecionados[0])
        protocolo = item["values"][0]

        if messagebox.askyesno(
            "Confirmar", "Deseja realmente REPROVAR esta solicitação de férias?"
        ):
            # Chamar controlador - ELE FAZ TODAS AS VALIDAÇÕES
            sucesso, mensagem = self.__controlador_solicitacao.rejeitar_solicitacao(
                protocolo
            )

            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.mostrar_todas_solicitacoes()  # Recarregar tabela
            else:
                messagebox.showerror("Erro", mensagem)

    def voltar(self):
        """Volta para a tela do gestor logado"""
        self.destroy()
        self.__controlador_solicitacao.voltar_tela_gestor()
