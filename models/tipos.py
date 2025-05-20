from enum import Enum
from datetime import date
from dataclasses import dataclass
from typing import Optional, List

class TipoUsuario(Enum):
    GESTOR = "gestor"
    RH = "rh"

class StatusSolicitacao(Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"

@dataclass
class PeriodoFerias:
    data_inicio: date
    data_fim: date