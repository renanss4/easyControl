import os
import json
from .modelo_colaborador import Colaborador
from .modelo_usuario import Usuario
from .tipos_enum import PeriodoFerias, StatusSolicitacao
from datetime import date

CAMINHO_ARQUIVO = "dados/solicitacoes.json"


class Solicitacao:
    def __init__(
        self,
        protocolo: str,
        pessoa: Colaborador | Usuario,
        data_solicitacao: date,
        periodos: list[PeriodoFerias] = [],
        parcelamento: bool = False,
        status: StatusSolicitacao = StatusSolicitacao.PENDENTE,
    ):
        self.protocolo = protocolo
        self.pessoa = pessoa
        self.data_solicitacao = data_solicitacao
        self.periodos = periodos
        self.parcelamento = parcelamento
        self.status = status

    def adicionar_periodo(self, periodo: PeriodoFerias) -> bool:
        if len(self.periodos) >= 3:
            return False

        if periodo.DATA_INICIO > periodo.DATA_FIM:
            return False

        self.periodos.append(periodo)
        return True

    def adicionar_pessoa(self, pessoa: Colaborador | Usuario) -> bool:
        if isinstance(pessoa, (Colaborador, Usuario)):
            self.pessoa = pessoa
            return True
        return False

    def aprovar_solicitacao(self) -> bool:
        if self.status == StatusSolicitacao.PENDENTE:
            self.status = StatusSolicitacao.APROVADA
            return True
        return False

    def rejeitar_solicitacao(self) -> bool:
        if self.status == StatusSolicitacao.PENDENTE:
            self.status = StatusSolicitacao.REJEITADA
            return True
        return False

    def cancelar_solicitacao(self) -> bool:
        if self.status == StatusSolicitacao.PENDENTE:
            self.status = StatusSolicitacao.CANCELADA
            return True
        return False

    @staticmethod
    def carregar_solicitacoes() -> list:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []
        try:
            with open(CAMINHO_ARQUIVO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_solicitacoes(solicitacoes: list) -> bool:
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        try:
            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(solicitacoes, f, indent=4)
            return True
        except IOError:
            return False
