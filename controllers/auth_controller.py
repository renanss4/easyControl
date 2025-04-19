import json
from models.user import Usuario

def autenticar(cpf, senha):
    # Carrega os dados dos usuários do arquivo JSON
    with open('data/users.json', 'r') as f:
        usuarios = json.load(f)

    for u in usuarios:
        if u['cpf'] == cpf and u['senha'] == senha:
            return Usuario(cpf=u['cpf'], senha=u['senha'])
    
    return None
