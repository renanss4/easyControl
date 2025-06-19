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
    def carregar_colaboradores() -> list[dict]:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def salvar_colaboradores(colaboradores: list[dict]) -> bool:
        try:
            os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
            with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as file:
                json.dump(colaboradores, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar colaboradores: {e}")
            return False
