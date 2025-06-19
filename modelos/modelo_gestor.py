import os
import json
from modelos.modelo_usuario import Usuario
from datetime import date

CAMINHO_ARQUIVO = "dados/gestores.json"


class Gestor(Usuario):
    def __init__(
        self,
        cpf: str = "",
        nome: str = "",
        email: str = "",
        data_admissao: date = date.today(),
        cargo: str = "Gestor",
        senha: str = "Gestor123",
    ):
        super().__init__(cpf, nome, email, data_admissao, cargo, senha)

    @staticmethod
    def carregar_gestores() -> list[dict]:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def salvar_gestores(gestores: list[dict]) -> bool:
        try:
            os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
            with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as file:
                json.dump(gestores, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar gestores: {e}")
            return False
