import json
import os
from datetime import date
from models.usuario import Usuario
from models.tipos import TipoUsuario
from utils.check_data import check_cpf, check_email, check_password

CAMINHO_ARQUIVO = "data/usuarios.json"


def _carregar_usuarios() -> list:
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    try:
        with open(CAMINHO_ARQUIVO, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _salvar_usuarios(usuarios: list) -> None:
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(usuarios, f, indent=4)


def _converter_dict_para_usuario(u: dict) -> Usuario:
    return Usuario(
        cpf=u["cpf"],
        nome=u["nome"],
        cargo=u["cargo"],
        equipe=u["equipe"],
        data_admissao=date.fromisoformat(u["data_admissao"]),
        email=u["email"],
        senha=u["senha"],
        tipo=TipoUsuario(u["tipo"]),
    )


def autenticar(email: str, senha: str) -> Usuario | None:
    for u in _carregar_usuarios():
        if u["email"] == email and u["senha"] == senha:
            return _converter_dict_para_usuario(u)
    return None


def cadastrar_usuario(
    nome: str,
    cpf: str,
    email: str,
    senha: str,
    data_admissao: date,
    cargo: str,
    equipe: str,
    tipo: TipoUsuario,
) -> Usuario | str:
    # deve ser usado apenas se o usuario logado for do tipo RH
    if not check_cpf(cpf):
        return "CPF inválido. Deve conter 11 dígitos numéricos."
    if not check_email(email):
        return "E-mail inválido. Verifique o formato (ex: exemplo@dominio.com)."
    if not check_password(senha):
        return "Senha fraca. Deve ter ao menos 8 caracteres, incluindo letra maiúscula, minúscula e número."

    usuarios = _carregar_usuarios()

    if any(u["cpf"] == cpf for u in usuarios):
        return "Erro: CPF já cadastrado."
    if any(u["email"] == email for u in usuarios):
        return "Erro: E-mail já cadastrado."

    novo_usuario = Usuario(
        cpf=cpf,
        nome=nome,
        cargo=cargo,
        equipe=equipe,
        data_admissao=data_admissao,
        email=email,
        senha=senha,
        tipo=tipo,
    )

    usuarios.append(
        {
            "cpf": cpf,
            "nome": nome,
            "cargo": cargo,
            "equipe": equipe,
            "data_admissao": data_admissao.isoformat(),
            "email": email,
            "senha": senha,
            "tipo": tipo.value,
            "solicitacoes_protocolos": []  # Inicializa com lista vazia
        }
    )

    _salvar_usuarios(usuarios)
    return novo_usuario


def cadastrar_rh(
    nome: str,
    cpf: str,
    email: str,
    senha: str,
    data_admissao: date,
    cargo: str = "RH",
    equipe: str = "Recursos Humanos",
) -> Usuario | str:
    return cadastrar_usuario(
        nome=nome,
        cpf=cpf,
        email=email,
        senha=senha,
        data_admissao=data_admissao,
        cargo=cargo,
        equipe=equipe,
        tipo=TipoUsuario.RH,
    )


def cadastrar_gestor(
    nome: str,
    cpf: str,
    email: str,
    senha: str,
    data_admissao: date,
    cargo: str = "Gestor",
    equipe: str = "Gestão",
) -> Usuario | str: 
    return cadastrar_usuario(
    nome=nome,
    cpf=cpf,
    email=email,
    senha=senha,
    data_admissao=data_admissao,
    cargo=cargo,
    equipe=equipe,
    tipo=TipoUsuario.GESTOR,
    )


def buscar_usuario_por_cpf(cpf: str) -> Usuario | None:
    for u in _carregar_usuarios():
        if u["cpf"] == cpf:
            return _converter_dict_para_usuario(u)
    return None

def buscar_rh_por_cpf(cpf: str) -> Usuario | None:
    for u in _carregar_usuarios():
        if u["cpf"] == cpf and u["tipo"] == TipoUsuario.RH.value:
            return _converter_dict_para_usuario(u)
    return None

def buscar_gestor_por_cpf(cpf: str) -> Usuario | None:
    for u in _carregar_usuarios():
        if u["cpf"] == cpf and u["tipo"] == TipoUsuario.Gestor.value:
            return _converter_dict_para_usuario(u)
    return None

def excluir_usuario(cpf: str) -> bool:
    # deve ser usado apenas se o usuario logado for do tipo RH
    usuarios = _carregar_usuarios()
    novos_usuarios = [u for u in usuarios if u["cpf"] != cpf]

    if len(novos_usuarios) == len(usuarios):
        return False  # CPF não encontrado

    _salvar_usuarios(novos_usuarios)
    return True


def atualizar_usuario(
    cpf: str,
    nome: str = None,
    email: str = None,
    senha: str = None,
    cargo: str = None,
    equipe: str = None,
) -> bool:
    # deve ser usado apenas se o usuario logado for do tipo RH
    usuarios = _carregar_usuarios()
    atualizado = False

    for u in usuarios:
        if u["cpf"] == cpf:
            if nome:
                u["nome"] = nome
            if email:
                u["email"] = email
            if senha:
                u["senha"] = senha
            if cargo:
                u["cargo"] = cargo
            if equipe:
                u["equipe"] = equipe
            atualizado = True
            break

    if atualizado:
        _salvar_usuarios(usuarios)
    return atualizado
