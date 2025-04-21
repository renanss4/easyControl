import json
import os
from models.hr_employee import RH
from datetime import datetime
from utils.check_data import check_cpf, check_email, check_password

def cadastrar_rh(nome, cpf, email, senha, dataAdmissao, cargo="RH", equipe=None):
    caminho_arquivo = 'data/users.json'
    if isinstance(dataAdmissao, datetime):
        dataAdmissao = dataAdmissao.strftime("%Y-%m-%d")
    if not check_cpf(cpf):
        return "CPF inválido. Deve conter 11 dígitos numéricos."
    if not check_email(email):
        return "E-mail inválido. Verifique o formato (ex: exemplo@dominio.com)."
    if not check_password(senha):
        return "Senha fraca. Deve ter ao menos 8 caracteres, incluindo letra maiúscula, minúscula e número."
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    for u in usuarios:
        if u['cpf'] == cpf:
            return "Erro: CPF já cadastrado."
        if u['email'] == email:
            return "Erro: E-mail já cadastrado."

    novo_rh = RH(
        nome=nome,
        cpf=cpf,
        email=email,
        senha=senha,
        dataAdmissao=dataAdmissao,
        cargo=cargo,
        equipe=equipe
    )

    usuarios.append({
        "cpf": novo_rh.cpf,
        "nome": novo_rh.nome,
        "cargo": novo_rh.cargo,
        "equipe": novo_rh.equipe,
        "dataAdmissao": novo_rh.dataAdmissao,
        "email": novo_rh.email,
        "senha": novo_rh.senha
    })

    with open(caminho_arquivo, 'w') as f:
        json.dump(usuarios, f, indent=4)

    return novo_rh