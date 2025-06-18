import os
import json
from modelos.modelo_colaborador import Colaborador
from modelos.modelo_gestor import Gestor
from modelos.modelo_funcionario_rh import FuncionarioRH

CAMINHO_ARQUIVO = "dados/equipes.json"


class Equipe:
    def __init__(
        self,
        nome: str = "",
        gestor: Gestor = None,
        colaboradores: list[Colaborador | FuncionarioRH] = [],
    ):
        self.__nome = nome
        self.__gestor = gestor
        self.__colaboradores = colaboradores if colaboradores else []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def gestor(self) -> Gestor:
        return self.__gestor

    @gestor.setter
    def gestor(self, gestor: Gestor):
        self.__gestor = gestor

    @property
    def colaboradores(self) -> list[Colaborador | FuncionarioRH]:
        return self.__colaboradores

    @colaboradores.setter
    def colaboradores(self, colaboradores: list[Colaborador | FuncionarioRH]):
        self.__colaboradores = colaboradores

    def adicionar_colaborador(self, colaborador: Colaborador | FuncionarioRH) -> bool:
        if (
            isinstance(colaborador, (Colaborador, FuncionarioRH))
            and colaborador not in self.__colaboradores
        ):
            self.__colaboradores.append(colaborador)
            return True
        return False

    def remover_colaborador(self, colaborador: Colaborador | FuncionarioRH) -> bool:
        if (
            isinstance(colaborador, (Colaborador, FuncionarioRH))
            and colaborador in self.__colaboradores
        ):
            self.__colaboradores.remove(colaborador)
            return True
        return False

    def adicionar_gestor(self, gestor: Gestor) -> bool:
        if isinstance(gestor, Gestor) and not self.__gestor:
            self.__gestor = gestor
            return True
        return False

    def remover_gestor(self) -> bool:
        if self.__gestor:
            self.__gestor = None
            return True
        return False

    @staticmethod
    def carregar_equipes() -> list:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_equipes(equipes: list) -> bool:
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        try:
            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(equipes, f, indent=4)
            return True
        except IOError:
            return False
