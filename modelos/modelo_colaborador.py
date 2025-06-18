import os
import json

from modelos.modelo_pessoa import Pessoa
from datetime import date

CAMINHO_ARQUIVO = "dados/colaboradores.json"


class Colaborador(Pessoa):
    def __init__(
        self,
        cpf: str = "",
        nome: str = "",
        cargo: str = "",
        data_admissao: date = date.today(),
        email: str = "",
    ):
        super().__init__(cpf, nome, cargo, data_admissao, email)

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
