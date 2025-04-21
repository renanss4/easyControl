from models.person import Pessoa

class Colaborador(Pessoa):
    def __init__(self, nome=None, cpf=None, email=None, dataAdmissao=None, cargo=None, equipe=None):
        super().__init__(nome, cpf, email, dataAdmissao, cargo, equipe)

    # Representação técnica/debug
    def __repr__(self):
        return f"<Colaborador nome={self.nome}, cpf={self.cpf}, email={self.email}>"

    # Representação legível para humanos
    def __str__(self):
        return f"Colaborador: {self.nome} - Cargo: {self.cargo} - Equipe: {self.equipe}"