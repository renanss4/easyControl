import os
import json
from .modelo_solicitacao import Solicitacao
from .modelo_usuario import Usuario
from datetime import date

CAMINHO_ARQUIVO = "dados/funcionarios_rh.json"


class FuncionarioRH(Usuario):
    def __init__(
        self,
        cpf: str,
        nome: str,
        email: str,
        data_admissao: date,
        cargo: str = "Analista de Recursos Humanos",
        solicitacoes: list[Solicitacao] = [],
        senha: str = "AnalistaRH123",
    ):
        super().__init__(cpf, nome, email, data_admissao, cargo, solicitacoes, senha)

    def adicionar_solicitacao(self, solicitacao: Solicitacao) -> bool:
        if solicitacao not in self.solicitacoes:
            self.solicitacoes.append(solicitacao)
            return True
        return False

    @staticmethod
    def carregar_funcionarios_rh() -> list:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_funcionarios_rh(funcionarios_rh: list) -> bool:
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        try:
            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(funcionarios_rh, f, indent=4)
            return True
        except IOError:
            return False
