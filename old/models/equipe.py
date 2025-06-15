from dataclasses import dataclass, field
from typing import List

@dataclass
class Equipe:
    nome: str
    gestor_cpf: str
    colaboradores_cpf: List[str] = field(default_factory=list)

    def adicionar_colaborador(self, cpf: str) -> None:
        if cpf not in self.colaboradores_cpf:
            self.colaboradores_cpf.append(cpf)

    def remover_colaborador(self, cpf: str) -> None:
        if cpf in self.colaboradores_cpf:
            self.colaboradores_cpf.remove(cpf)