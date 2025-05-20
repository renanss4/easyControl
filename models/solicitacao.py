from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from .tipos import StatusSolicitacao, PeriodoFerias

@dataclass
class Solicitacao:
    protocolo: str
    cpf_colaborador: str
    data_solicitacao: date = field(default_factory=date.today)
    parcelamento: bool = False
    status: StatusSolicitacao = StatusSolicitacao.PENDENTE
    periodos: List[PeriodoFerias] = field(default_factory=list)
    aprovado_por: Optional[str] = None
    data_aprovacao: Optional[date] = None

    def adicionar_periodo(self, periodo: PeriodoFerias) -> bool:
        if len(self.periodos) >= 3:
            return False
        
        if periodo.data_inicio > periodo.data_fim:
            return False

        self.periodos.append(periodo)
        return True

    def aprovar(self, cpf_aprovador: str) -> None:
        self.status = StatusSolicitacao.APROVADO
        self.aprovado_por = cpf_aprovador
        self.data_aprovacao = date.today()

    def rejeitar(self) -> None:
        self.status = StatusSolicitacao.REJEITADO