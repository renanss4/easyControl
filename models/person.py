from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome=None, cpf=None, email=None, dataAdmissao=None, cargo=None, equipe=None):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.dataAdmissao = dataAdmissao
        self.cargo = cargo
        self.equipe = equipe

