from dataclasses import dataclass
from .pessoa import Pessoa
from .tipos import TipoUsuario

@dataclass
class Usuario(Pessoa):
    senha: str = ""
    tipo: TipoUsuario = TipoUsuario.RH