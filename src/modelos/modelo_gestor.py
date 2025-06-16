import os
import json
from .modelo_solicitacao import Solicitacao
from .modelo_usuario import Usuario
from datetime import date

CAMINHO_ARQUIVO = "dados/gestores.json"


class Gestor(Usuario):
    def __init__(
        self,
        cpf: str,
        nome: str,
        email: str,
        data_admissao: date,
        cargo: str = "Gestor",
        solicitacoes: list[Solicitacao] = [],
        senha: str = "Gestor123",
    ):
        super().__init__(cpf, nome, email, data_admissao, cargo, solicitacoes, senha)

    def adicionar_solicitacao(self, solicitacao: Solicitacao) -> bool:
        if solicitacao not in self.solicitacoes:
            self.solicitacoes.append(solicitacao)
            return True
        return False

    @staticmethod
    def carregar_gestores() -> list:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_gestores(gestores: list) -> bool:
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        try:
            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(gestores, f, indent=4)
            return True
        except IOError:
            return False
