import os
import json
from .modelo_colaborador import Colaborador
from .modelo_gestor import Gestor
from .modelo_funcionario_rh import FuncionarioRH

CAMINHO_ARQUIVO = "dados/equipes.json"


class Equipe:
    def __init__(
        self,
        nome: str,
        gestor: Gestor = None,
        colaboradores: list[Colaborador | FuncionarioRH] = [],
    ):
        self.nome = nome
        self.gestor = gestor
        self.colaboradores = colaboradores

    def adicionar_colaborador(self, colaborador: Colaborador | FuncionarioRH) -> bool:
        if (
            isinstance(colaborador, (Colaborador, FuncionarioRH))
            and colaborador not in self.colaboradores
        ):
            self.colaboradores.append(colaborador)
            return True
        return False

    def remover_colaborador(self, colaborador: Colaborador | FuncionarioRH) -> bool:
        if (
            isinstance(colaborador, (Colaborador, FuncionarioRH))
            and colaborador in self.colaboradores
        ):
            self.colaboradores.remove(colaborador)
            return True
        return False

    def adicionar_gestor(self, gestor: Gestor) -> bool:
        if isinstance(gestor, Gestor) and not self.gestor:
            self.gestor = gestor
            return True
        return False

    def remover_gestor(self) -> bool:
        if self.gestor:
            self.gestor = None
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
