from datetime import date
from enum import Enum


class StatusSolicitacao(Enum):
    PENDENTE = "PENDENTE"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"
    CANCELADA = "CANCELADA"


class PeriodoFerias(Enum):
    DATA_INICIO = date
    DATA_FIM = date
