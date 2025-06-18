from modelos.modelo_pessoa import Pessoa
from datetime import date


class Usuario(Pessoa):
    def __init__(
        self,
        cpf: str,
        nome: str,
        email: str,
        data_admissao: date,
        cargo: str,
        senha: str,
    ):
        super().__init__(cpf, nome, cargo, data_admissao, email)
        self.__senha = senha

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        self.__senha = senha
