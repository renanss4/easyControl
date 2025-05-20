from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class Pessoa(ABC):
    cpf: str
    nome: str
    cargo: str
    equipe: str
    data_admissao: date
    email: str
    solicitacoes_protocolos: List[str] = field(default_factory=list)

    def adicionar_solicitacao(self, protocolo: str) -> None:
        if protocolo not in self.solicitacoes_protocolos:
            self.solicitacoes_protocolos.append(protocolo)

    @abstractmethod
    def pode_aprovar_solicitacao(self) -> bool:
        pass