import os
import json
from modelos.modelo_usuario import Usuario
from datetime import date

CAMINHO_ARQUIVO = "dados/funcionarios_rh.json"


class FuncionarioRH(Usuario):
    def __init__(
        self,
        cpf: str = "",
        nome: str = "",
        email: str = "",
        data_admissao: date = date.today(),
        cargo: str = "Analista de Recursos Humanos",
        senha: str = "AnalistaRH123",
    ):
        super().__init__(cpf, nome, email, data_admissao, cargo, senha)

    @staticmethod
    def carregar_funcionarios_rh() -> list[dict]:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_funcionarios_rh(funcionarios_rh: list[dict]) -> bool:
        try:
            os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
            with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as file:
                json.dump(funcionarios_rh, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar funcionários RH: {e}")
            return False
