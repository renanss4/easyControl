from dataclasses import dataclass
from .pessoa import Pessoa

@dataclass
class Colaborador(Pessoa):
    def pode_aprovar_solicitacao(self) -> bool:
        return False