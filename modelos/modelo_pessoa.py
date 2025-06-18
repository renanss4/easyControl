from abc import ABC
from datetime import date


class Pessoa(ABC):
    def __init__(
        self,
        cpf: str,
        nome: str,
        cargo: str,
        data_admissao: date,
        email: str,
    ):
        self.__cpf = cpf
        self.__nome = nome
        self.__cargo = cargo
        self.__data_admissao = data_admissao
        self.__email = email

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def cargo(self) -> str:
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo: str):
        self.__cargo = cargo

    @property
    def data_admissao(self) -> date:
        return self.__data_admissao

    @data_admissao.setter
    def data_admissao(self, data_admissao: date):
        self.__data_admissao = data_admissao

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email
