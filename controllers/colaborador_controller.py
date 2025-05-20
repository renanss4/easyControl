import json
import os
from models.colaborador import Colaborador
from datetime import datetime
from utils.check_data import check_cpf, check_email

CAMINHO_ARQUIVO = "data/colaboradores.json"


def criar_colaborador(nome, cpf, email, data_admissao, cargo, equipe):
    # deve funcionar apenas se o usuario logado for do tipo RH
    """
    Cria um novo colaborador após validar os dados.
    Retorna o colaborador criado ou uma mensagem de erro.
    """
    if isinstance(data_admissao, datetime):
        data_admissao = data_admissao.strftime("%Y-%m-%d")

    if not check_cpf(cpf):
        return "CPF inválido. Deve conter 11 dígitos numéricos."

    if not check_email(email):
        return "E-mail inválido. Verifique o formato (ex: exemplo@dominio.com)."

    colaboradores = []
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r") as f:
            try:
                colaboradores = json.load(f)
            except json.JSONDecodeError:
                colaboradores = []

    for c in colaboradores:
        if c.get("cpf") == cpf:
            return "Erro: CPF já cadastrado."
        if c.get("email") == email:
            return "Erro: E-mail já cadastrado."

    novo_colaborador = Colaborador(
        nome=nome,
        cpf=cpf,
        email=email,
        dataAdmissao=data_admissao,
        cargo=cargo,
        equipe=equipe,
    )

    colaborador_dict = {
        "cpf": novo_colaborador.cpf,
        "nome": novo_colaborador.nome,
        "cargo": novo_colaborador.cargo,
        "equipe": novo_colaborador.equipe,
        "dataAdmissao": novo_colaborador.dataAdmissao,
        "email": novo_colaborador.email,
    }

    colaboradores.append(colaborador_dict)

    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(colaboradores, f, indent=4)

    return novo_colaborador


def listar_colaboradores():
    """Retorna a lista de todos os colaboradores."""
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r") as f:
            try:
                colaboradores_json = json.load(f)
                colaboradores = []
                for c in colaboradores_json:
                    colaborador = Colaborador(
                        nome=c.get("nome"),
                        cpf=c.get("cpf"),
                        email=c.get("email"),
                        dataAdmissao=c.get("dataAdmissao"),
                        cargo=c.get("cargo"),
                        equipe=c.get("equipe"),
                    )
                    colaboradores.append(colaborador)
                return colaboradores
            except json.JSONDecodeError:
                return []
    return []


def buscar_colaborador_por_cpf(cpf):
    """Busca um colaborador pelo CPF."""
    colaboradores = listar_colaboradores()
    for colaborador in colaboradores:
        if colaborador.cpf == cpf:
            return colaborador
    return None


def atualizar_colaborador(
    cpf, nome=None, email=None, data_admissao=None, cargo=None, equipe=None
):
    # deve funcionar apenas se o usuario logado for do tipo RH
    """Atualiza os dados de um colaborador existente."""
    if not check_cpf(cpf):
        return "CPF inválido. Deve conter 11 dígitos numéricos."

    if email and not check_email(email):
        return "E-mail inválido. Verifique o formato (ex: exemplo@dominio.com)."

    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r") as f:
            try:
                colaboradores = json.load(f)
            except json.JSONDecodeError:
                return "Erro ao ler o arquivo de colaboradores."
    else:
        return "Arquivo de colaboradores não encontrado."

    encontrado = False
    for i, c in enumerate(colaboradores):
        if c.get("cpf") == cpf:
            encontrado = True
            if nome:
                colaboradores[i]["nome"] = nome
            if email:
                colaboradores[i]["email"] = email
            if data_admissao:
                if isinstance(data_admissao, datetime):
                    data_admissao = data_admissao.strftime("%Y-%m-%d")
                colaboradores[i]["dataAdmissao"] = data_admissao
            if cargo:
                colaboradores[i]["cargo"] = cargo
            if equipe:
                colaboradores[i]["equipe"] = equipe

    if not encontrado:
        return "Colaborador não encontrado."

    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(colaboradores, f, indent=4)

    return buscar_colaborador_por_cpf(cpf)


def excluir_colaborador(cpf):
    # deve funcionar apenas se o usuario logado for do tipo RH
    """Remove um colaborador do banco de dados pelo CPF."""
    if not check_cpf(cpf):
        return "CPF inválido. Deve conter 11 dígitos numéricos."

    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r") as f:
            try:
                colaboradores = json.load(f)
            except json.JSONDecodeError:
                return "Erro ao ler o arquivo de colaboradores."
    else:
        return "Arquivo de colaboradores não encontrado."

    colaboradores_filtrados = [c for c in colaboradores if c.get("cpf") != cpf]

    if len(colaboradores) == len(colaboradores_filtrados):
        return "Colaborador não encontrado."

    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(colaboradores_filtrados, f, indent=4)

    return True
