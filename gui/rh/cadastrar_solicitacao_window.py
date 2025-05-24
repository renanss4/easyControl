import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from controllers.solicitacao_controller import (
    cadastrar_solicitacao_parcelada,
    validar_periodo_ferias,
    validar_parcelamento_ferias
)

class CadastraSolicitacaoWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Solicitação de Férias")
        self.configure(bg="#dcdcdc")
        self.geometry("900x600")

        # Criar canvas com scrollbar
        self.canvas = tk.Canvas(self, bg="#dcdcdc")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#dcdcdc")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame principal com borda
        borda_frame = tk.Frame(self.scrollable_frame, bg="#dcdcdc", bd=2, relief="groove", padx=10, pady=10)
        borda_frame.pack(padx=20, pady=(20, 10), fill="both", expand=True)

        # Título da janela
        tk.Label(
            borda_frame,
            text="Solicitação de Férias",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc"
        ).pack(pady=15)
        
        # Container dos campos
        campos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        campos_frame.pack(pady=10, fill="x")

        # CPF
        tk.Label(campos_frame, text="CPF do Colaborador", font=("Arial", 10, "bold"), 
                bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.cpf_entry = tk.Entry(campos_frame, width=30)
        self.cpf_entry.pack(padx=20)

        # Checkbox para parcelamento
        self.var_parcelamento = tk.BooleanVar()
        tk.Checkbutton(
            campos_frame, 
            text="Parcelamento de Férias",
            variable=self.var_parcelamento,
            bg="#dcdcdc",
            font=("Arial", 10),
            command=self.toggle_parcelamento
        ).pack(pady=10)

        # Adicionar contador de dias
        self.label_total_dias = tk.Label(
            campos_frame,
            text="Total de dias: 0/30",
            font=("Arial", 10, "bold"),
            bg="#dcdcdc"
        )
        self.label_total_dias.pack(pady=5)

        # Frame para períodos
        self.periodos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        self.periodos_frame.pack(fill="x", padx=20, pady=10)
        
        # Lista para armazenar os widgets de período
        self.periodos = []
        
        # Adicionar primeiro período
        self.adicionar_periodo()

        # Botão para adicionar mais períodos
        self.btn_adicionar_periodo = tk.Button(
            borda_frame,
            text="Adicionar Período",
            command=self.adicionar_periodo,
            state="disabled"
        )
        self.btn_adicionar_periodo.pack(pady=5)

        # Frame para os botões principais
        botoes_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        botoes_frame.pack(pady=(10, 20), side="bottom")

        tk.Button(
            botoes_frame,
            text="Enviar solicitação",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.concluir_solicitacao
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Gerenciar Solicitações",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.gerenciar_solicitacao
        ).pack(side="left", padx=5)

        tk.Button(
            botoes_frame,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=20,
            command=self.voltar
        ).pack(side="left", padx=5)

        # Configurar pack do canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
            bg="#dcdcdc"
        ).pack(pady=5)

        # Container para as datas
        datas_frame = tk.Frame(frame, bg="#dcdcdc")
        datas_frame.pack(pady=5)

        # Data início - com data mínima de hoje + 30 dias
        tk.Label(datas_frame, text="Início:", bg="#dcdcdc").pack(side="left", padx=5)
        data_minima = datetime.today() + timedelta(days=30)
        data_inicio = DateEntry(
            datas_frame,
            width=12,
            background='darkblue',
            foreground='white',
            date_pattern='yyyy-mm-dd',
            mindate=data_minima
        )
        data_inicio.pack(side="left", padx=5)

        # Data fim
        tk.Label(datas_frame, text="Fim:", bg="#dcdcdc").pack(side="left", padx=5)
        data_fim = DateEntry(
            datas_frame,
            width=12,
            background='darkblue',
            foreground='white',
            date_pattern='yyyy-mm-dd',
            mindate=data_minima
        )
        data_fim.pack(side="left", padx=5)

        # Label para dias do período
        label_dias = tk.Label(
            frame,
            text="Dias: 0",
            bg="#dcdcdc"
        )
        label_dias.pack(pady=2)

        # Bind para atualizar dias quando as datas mudarem
        data_inicio.bind("<<DateEntrySelected>>", 
                        lambda e: self.atualizar_dias(data_inicio, data_fim, label_dias))
        data_fim.bind("<<DateEntrySelected>>", 
                     lambda e: self.atualizar_dias(data_inicio, data_fim, label_dias))

        # Botão remover
        btn_remover = tk.Button(
            frame,
            text="Remover",
            command=lambda: self.remover_periodo(frame)
        )
        btn_remover.pack(pady=5)

        return frame, data_inicio, data_fim

    def atualizar_dias(self, data_inicio, data_fim, label_dias):
        """Atualiza o contador de dias para um período"""
        try:
            inicio = datetime.strptime(data_inicio.get(), "%Y-%m-%d").date()
            fim = datetime.strptime(data_fim.get(), "%Y-%m-%d").date()
            
            # Validar período individual
            dias = (fim - inicio).days + 1
            
            if not self.var_parcelamento.get() and dias != 30:
                label_dias.config(text=f"Dias: {dias}", fg="red")
            else:
                label_dias.config(text=f"Dias: {dias}", fg="black")
            
            # Atualizar total de dias
            total = self.calcular_total_dias()
            self.label_total_dias.config(
                text=f"Total de dias: {total}/30",
                fg="red" if total > 30 else "black"
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
                "Limite atingido",
                "Máximo de 3 períodos permitidos."
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
                    if isinstance(widget, tk.Label) and "Período" in widget.cget("text"):
                        widget.config(text=f"Período {i}")

    def concluir_solicitacao(self):
        """Processa e envia a solicitação"""
        cpf = self.cpf_entry.get().strip()
        if not cpf:
            messagebox.showerror("Erro", "Por favor, preencha o CPF.")
            return

        # Verificar se há solicitação pendente
        from controllers.solicitacao_controller import buscar_solicitacoes_por_cpf
        solicitacoes = buscar_solicitacoes_por_cpf(cpf)
        
        # Verificar se existe alguma solicitação pendente
        if any(sol["status"] == "pendente" for sol in solicitacoes):
            messagebox.showerror(
                "Erro", 
                "Este colaborador já possui uma solicitação pendente.\n"
                "Não é possível cadastrar uma nova solicitação."
            )
            return

        periodos = []
        for _, data_inicio, data_fim in self.periodos:
            try:
                inicio = datetime.strptime(data_inicio.get(), "%Y-%m-%d").date()
                fim = datetime.strptime(data_fim.get(), "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Erro", "Datas inválidas")
                return

            # Validar período individual
            valido, msg = validar_periodo_ferias(inicio, fim)
            if not valido:
                messagebox.showerror("Erro", msg)
                return

            periodos.append((inicio, fim))

        # Validar se não é parcelamento
        if not self.var_parcelamento.get():
            if len(periodos) > 1:
                messagebox.showerror("Erro", "Sem parcelamento, deve haver apenas um período")
                return
            valido, msg = self.validar_periodo_nao_parcelado(periodos[0][0], periodos[0][1])
            if not valido:
                messagebox.showerror("Erro", msg)
                return
        else:
            # Validar ordem cronológica dos períodos
            valido, msg = self.validar_periodos_sequenciais(periodos)
            if not valido:
                messagebox.showerror("Erro", msg)
                return

            # Validar parcelamento
            valido, msg = validar_parcelamento_ferias(periodos)
            if not valido:
                messagebox.showerror("Erro", msg)
                return

        try:
            resultado = cadastrar_solicitacao_parcelada(
                cpf_colaborador=cpf,
                periodos=periodos,
                parcelamento=self.var_parcelamento.get()
            )
            
            messagebox.showinfo(
                "Sucesso", 
                f"Solicitação cadastrada com sucesso!\nProtocolo: {resultado['protocolo']}"
            )
            self.voltar()
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def validar_periodos_sequenciais(self, periodos):
        """Valida se os períodos estão em ordem cronológica e atendem às regras"""
        for i, (inicio, fim) in enumerate(periodos):
            # Validar dia útil no início da semana
            dia_semana = inicio.weekday()
            if dia_semana in [4, 5, 6]:  # 4=sexta, 5=sábado, 6=domingo
                if dia_semana == 4:
                    return False, "As férias não podem iniciar em uma sexta-feira"
                else:
                    return False, "As férias devem iniciar em um dia útil"
                
            # Validar antecedência mínima
            if (inicio - date.today()).days < 30:
                return False, "A solicitação deve ser feita com no mínimo 30 dias de antecedência"
                
            # Para parcelamento, validar primeiro período de 14 dias
            if self.var_parcelamento.get() and i == 0:
                dias = (fim - inicio).days + 1
                if dias != 14:
                    return False, "O primeiro período do parcelamento deve ter exatamente 14 dias"
                
            # Validar sequência
            if i < len(periodos)-1:
                if periodos[i][1] >= periodos[i+1][0]:
                    return False, "Os períodos devem ser sequenciais e não podem se sobrepor"
                
        return True, ""

    def validar_periodo_nao_parcelado(self, inicio, fim):
        """Valida se o período único tem exatamente 30 dias e atende às regras"""
        dias = (fim - inicio).days + 1
        
        # Validar quantidade de dias
        if dias != 30:
            return False, "Para férias não parceladas, o período deve ser de exatamente 30 dias"
            
        # Validar dia útil no início da semana
        dia_semana = inicio.weekday()
        if dia_semana in [4, 5, 6]:  # 4=sexta, 5=sábado, 6=domingo
            if dia_semana == 4:
                return False, "As férias não podem iniciar em uma sexta-feira"
            else:
                return False, "As férias devem iniciar em um dia útil"
            
        # Validar antecedência
        if (inicio - date.today()).days < 30:
            return False, "A solicitação deve ser feita com no mínimo 30 dias de antecedência"
            
        return True, ""

    def gerenciar_solicitacao(self):
        self.destroy()
        from gui.rh.crud_solicitacao.gerenciar_solicitacao_window import GerenciaSolicitacoesWindow
        GerenciaSolicitacoesWindow().mainloop()

    def voltar(self):
        self.destroy()
        from gui.rh.principal_rh_window import PrincipalRhWindow
        PrincipalRhWindow().mainloop()
