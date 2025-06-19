import os
import json
from modelos.modelo_pessoa import Pessoa
from modelos.tipos_enum import PeriodoFerias, StatusSolicitacao
from datetime import date

CAMINHO_ARQUIVO = "dados/solicitacoes.json"


class Solicitacao:
    def __init__(
        self,
        protocolo: str = "",
        pessoa: Pessoa = None,
        data_solicitacao: date = date.today(),
        periodos: list[PeriodoFerias] = [],
        parcelamento: bool = False,
        status: StatusSolicitacao = StatusSolicitacao.PENDENTE,
    ):
        self.__protocolo = protocolo
        self.__pessoa = pessoa
        self.__data_solicitacao = data_solicitacao
        self.__periodos = periodos if periodos else []
        self.__parcelamento = parcelamento
        self.__status = status

    @property
    def protocolo(self) -> str:
        return self.__protocolo

    @protocolo.setter
    def protocolo(self, protocolo: str):
        self.__protocolo = protocolo

    @property
    def pessoa(self) -> Pessoa:
        return self.__pessoa

    @pessoa.setter
    def pessoa(self, pessoa: Pessoa):
        self.__pessoa = pessoa

    @property
    def data_solicitacao(self) -> date:
        return self.__data_solicitacao

    @data_solicitacao.setter
    def data_solicitacao(self, data_solicitacao: date):
        self.__data_solicitacao = data_solicitacao

    @property
    def periodos(self) -> list[PeriodoFerias]:
        return self.__periodos

    @periodos.setter
    def periodos(self, periodos: list[PeriodoFerias]):
        self.__periodos = periodos

    @property
    def parcelamento(self) -> bool:
        return self.__parcelamento

    @parcelamento.setter
    def parcelamento(self, parcelamento: bool):
        self.__parcelamento = parcelamento

    @property
    def status(self) -> StatusSolicitacao:
        return self.__status

    @status.setter
    def status(self, status: StatusSolicitacao):
        self.__status = status

    def adicionar_periodo(self, periodo: PeriodoFerias) -> bool:
        if len(self.__periodos) >= 3:
            return False

        if periodo.DATA_INICIO > periodo.DATA_FIM:
            return False

        self.__periodos.append(periodo)
        return True

    def adicionar_pessoa(self, pessoa: Pessoa) -> bool:
        if isinstance(pessoa, Pessoa):
            self.__pessoa = pessoa
            return True
        return False

    def aprovar_solicitacao(self) -> bool:
        if self.__status == StatusSolicitacao.PENDENTE:
            self.__status = StatusSolicitacao.APROVADA
            return True
        return False

    def rejeitar_solicitacao(self) -> bool:
        if self.__status == StatusSolicitacao.PENDENTE:
            self.__status = StatusSolicitacao.REJEITADA
            return True
        return False

    def cancelar_solicitacao(self) -> bool:
        if self.__status == StatusSolicitacao.PENDENTE:
            self.__status = StatusSolicitacao.CANCELADA
            return True
        return False

    def carregar_solicitacoes(self) -> list[dict]:
        """Carrega as solicitações do arquivo JSON"""
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []

        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def salvar_solicitacoes(self, solicitacoes: list[dict]) -> bool:
        """Salva as solicitações no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
            with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as file:
                json.dump(solicitacoes, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar solicitações: {e}")
            return False
