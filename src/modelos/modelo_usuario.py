from .modelo_pessoa import Pessoa
from .modelo_solicitacao import Solicitacao
from datetime import date


class Usuario(Pessoa):
    def __init__(
        self,
        cpf: str,
        nome: str,
        email: str,
        data_admissao: date,
        cargo: str,
        solicitacoes: list[Solicitacao],
        senha: str,
    ):
        super().__init__(cpf, nome, cargo, data_admissao, email, solicitacoes)
        self.senha = senha
