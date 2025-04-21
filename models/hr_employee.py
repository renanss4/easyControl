from models.user import Usuario

class RH(Usuario):
    def __init__(self, nome=None, cpf=None, email=None, senha=None, dataAdmissao=None, cargo=None, equipe=None):
        super().__init__(nome, cpf, email, senha, dataAdmissao, cargo, equipe)
