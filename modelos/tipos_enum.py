from datetime import date
from enum import Enum


class StatusSolicitacao(Enum):
    PENDENTE = "pendente"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    CANCELADA = "cancelada"


class PeriodoFerias(Enum):
    DATA_INICIO = date
    DATA_FIM = date
