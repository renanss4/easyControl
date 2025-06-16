from abc import ABC
from datetime import date
from .modelo_solicitacao import Solicitacao


class Pessoa(ABC):
    def __init__(
        self,
        cpf: str,
        nome: str,
        cargo: str,
        data_admissao: date,
        email: str,
        solicitacoes: list[Solicitacao] = [],
    ):
        self.cpf = cpf
        self.nome = nome
        self.cargo = cargo
        self.data_admissao = data_admissao
        self.email = email
        self.solicitacoes = solicitacoes
