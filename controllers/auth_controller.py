import json
from models.user import Usuario

def autenticar(email, senha):
    # Carrega os dados dos usuários do arquivo JSON
    with open('data/users.json', 'r') as f:
        usuarios = json.load(f)

    for u in usuarios:
        if u['email'] == email and u['senha'] == senha:
            return Usuario(email=u['email'], senha=u['senha'])
    
    return None
