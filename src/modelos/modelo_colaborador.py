import os
import json

from .modelo_pessoa import Pessoa
from .modelo_solicitacao import Solicitacao
from datetime import date

CAMINHO_ARQUIVO = "dados/colaboradores.json"


class Colaborador(Pessoa):
    def __init__(
        self,
        cpf: str,
        nome: str,
        cargo: str,
        data_admissao: date,
        email: str,
        solicitacoes: list[Solicitacao] = [],
    ):
        super().__init__(cpf, nome, cargo, data_admissao, email, solicitacoes)

    def adicionar_solicitacao(self, solicitacao: Solicitacao) -> bool:
        if (
            isinstance(solicitacao, Solicitacao)
            and solicitacao not in self.solicitacoes
        ):
            self.solicitacoes.append(solicitacao)
            return True
        return False

    @staticmethod
    def carregar_colaboradores() -> list:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_colaboradores(colaboradores: list) -> bool:
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        try:
            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(colaboradores, f, indent=4)
            return True
        except IOError:
            return False
