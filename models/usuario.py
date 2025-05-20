from dataclasses import dataclass
from .pessoa import Pessoa
from .tipos import TipoUsuario

@dataclass
class Usuario(Pessoa):
    senha: str = ""
    tipo: TipoUsuario = TipoUsuario.RH

    def pode_aprovar_solicitacao(self) -> bool:
        return self.tipo in [TipoUsuario.GESTOR, TipoUsuario.RH]