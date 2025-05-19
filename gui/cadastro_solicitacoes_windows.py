import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from controllers.solicitacoes_controller import cadastrar_solicitacao

class CadastroSolicitacoesWindow(tk.Tk):
    def __init__(self, tela_anterior=None):
        super().__init__()
        self.title("Cadastro de Solicitação de Férias")
        self.configure(bg="#dcdcdc")
        self.geometry("700x600")
        self.tela_anterior = tela_anterior

        # Frame principal com borda
        borda_frame = tk.Frame(self, bg="#dcdcdc", bd=2, relief="groove", padx=10, pady=10)
        borda_frame.pack(padx=20, pady=(20, 10), fill="both", expand=False)

        # Título da janela
        tk.Label(
            borda_frame,
            text="Solicitação de Férias",
            font=("Arial", 16, "bold"),
            bg="#dcdcdc"
        ).pack(pady=15)
        
        # Container dos campos
        campos_frame = tk.Frame(borda_frame, bg="#dcdcdc")
        campos_frame.pack(pady=10)

        self.campos = {}

        # CPF
        tk.Label(campos_frame, text="CPF do Colaborador", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        self.campos["cpf"] = tk.Entry(campos_frame, width=30)
        self.campos["cpf"].pack(padx=20)

        # Data de início
        tk.Label(campos_frame, text="Data de Início", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        data_inicio_frame = tk.Frame(campos_frame, bg="#dcdcdc")
        data_inicio_frame.pack(padx=20, fill="x")
        self.campos["data_inicio"] = tk.Entry(data_inicio_frame, width=25)
        self.campos["data_inicio"].pack(side="left")
        self.campos["data_inicio"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        tk.Button(data_inicio_frame, text="📅", command=lambda: self.abrir_calendario("data_inicio")).pack(side="left", padx=5)

        # Data de término
        tk.Label(campos_frame, text="Data de Término", font=("Arial", 10, "bold"), bg="#dcdcdc", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        data_fim_frame = tk.Frame(campos_frame, bg="#dcdcdc")
        data_fim_frame.pack(padx=20, fill="x")
        self.campos["data_fim"] = tk.Entry(data_fim_frame, width=25)
        self.campos["data_fim"].pack(side="left")
        self.campos["data_fim"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        tk.Button(data_fim_frame, text="📅", command=lambda: self.abrir_calendario("data_fim")).pack(side="left", padx=5)

        # Checkbox para parcelamento
        self.var_parcelamento = tk.BooleanVar()
        tk.Checkbutton(
            campos_frame, 
            text="Parcelamento",
            variable=self.var_parcelamento,
            bg="#dcdcdc",
            font=("Arial", 10),
            state="disabled"  # Desabilitado por enquanto
        ).pack(pady=10)

        # Botão de conclusão
        tk.Button(
            self,
            text="Enviar solicitação",
            font=("Arial", 10, "bold"),
            bg="#c0c0c0",
            width=25,
            command=self.concluir_solicitacao
        ).pack(pady=(10, 20))

    def abrir_calendario(self, campo):
        top = tk.Toplevel(self)
        top.title("Selecione a data")
        top.geometry("300x250")
        top.resizable(False, False)
        top.transient(self)
        top.grab_set()
        
        cal = DateEntry(
            top,
            date_pattern="yyyy-mm-dd",
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        cal.pack(padx=10, pady=10)
        
        def confirmar_data():
            self.campos[campo].delete(0, tk.END)
            self.campos[campo].insert(0, cal.get())
            top.destroy()
            
        tk.Button(top, text="Confirmar", command=confirmar_data).pack(pady=10)

    def concluir_solicitacao(self):
        cpf = self.campos["cpf"].get().strip()
        
        # Convertendo para datetime e extraindo apenas a data
        data_inicio = datetime.strptime(self.campos["data_inicio"].get(), "%Y-%m-%d").date()
        data_fim = datetime.strptime(self.campos["data_fim"].get(), "%Y-%m-%d").date()

        if not cpf:
            messagebox.showerror("Erro", "Por favor, preencha o CPF.")
            return

        resultado = cadastrar_solicitacao(
            cpf_colaborador=cpf,
            data_inicio=data_inicio,
            data_fim=data_fim,
            parcelamento=self.var_parcelamento.get()
        )

        if isinstance(resultado, str):
            messagebox.showerror("Erro", resultado)
        else:
            messagebox.showinfo(
                "Sucesso", 
                f"Solicitação cadastrada com sucesso!\nProtocolo: {resultado['protocolo']}"
            )
            self.destroy()
            
            if self.tela_anterior:
                from gui.main_window import MainWindow
                MainWindow().mainloop()
