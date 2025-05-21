import re
from datetime import datetime


def check_cpf(cpf: str) -> bool:
    """Verifica se o CPF é válido."""
    if not cpf or not isinstance(cpf, str):
        return False
    cpf = re.sub(r"[^0-9]", "", cpf)
    return len(cpf) == 11 and cpf.isdigit()


def check_email(email: str) -> bool:
    """Verifica se o email é válido."""
    if not email or not isinstance(email, str):
        return False
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email))


def check_password(password: str) -> bool:
    """Verifica se a senha atende aos requisitos mínimos."""
    if not password or not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True


def check_nome(nome: str) -> bool:
    """Verifica se o nome é válido."""
    if not nome or not isinstance(nome, str):
        return False
    nome = nome.strip()
    if len(nome) < 3:
        return False
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{3,}$", nome))


def check_data(data: str) -> bool:
    """Verifica se a data é válida e está no formato correto."""
    if not data or not isinstance(data, str):
        return False
    try:
        datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def check_cargo(cargo: str) -> bool:
    """Verifica se o cargo é válido."""
    if not cargo or not isinstance(cargo, str):
        return False
    cargo = cargo.strip()
    return len(cargo) >= 2 and bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", cargo))


def check_equipe(equipe: str) -> bool:
    """Verifica se a equipe é válida."""
    if not equipe or not isinstance(equipe, str):
        return False
    equipe = equipe.strip()
    return len(equipe) >= 2


def check_protocolo(protocolo: str) -> bool:
    """Verifica se o protocolo está no formato correto."""
    if not protocolo or not isinstance(protocolo, str):
        return False
    padrao = r"^SOL-\d{8}-[A-Z0-9]{5}$"
    return bool(re.match(padrao, protocolo))


def check_status(status: str) -> bool:
    """Verifica se o status é válido."""
    if not status or not isinstance(status, str):
        return False
    status_validos = ["pendente", "aprovado", "reprovado"]
    return status.lower() in status_validos


def check_tipo_usuario(tipo: str) -> bool:
    """Verifica se o tipo de usuário é válido."""
    if not tipo or not isinstance(tipo, str):
        return False
    tipos_validos = ["gestor", "rh", "colaborador"]
    return tipo.lower() in tipos_validos


def check_parcelamento(parcelamento: bool) -> bool:
    """Verifica se o parcelamento é um booleano."""
    return isinstance(parcelamento, bool)


def check_periodos(periodos: list) -> bool:
    """Verifica se os períodos são válidos."""
    if not isinstance(periodos, list) or not periodos:
        return False

    for periodo in periodos:
        if not isinstance(periodo, dict):
            return False
        if "data_inicio" not in periodo or "data_fim" not in periodo:
            return False
        if not check_data(periodo["data_inicio"]) or not check_data(
            periodo["data_fim"]
        ):
            return False
        # Verifica se data_fim é posterior a data_inicio
        inicio = datetime.strptime(periodo["data_inicio"], "%Y-%m-%d")
        fim = datetime.strptime(periodo["data_fim"], "%Y-%m-%d")
        if fim <= inicio:
            return False

    return True


def valida_todos_dados(**kwargs) -> tuple[bool, str]:
    """
    Valida todos os campos fornecidos.
    Retorna uma tupla (sucesso, mensagem).

    Exemplo de uso:
    sucesso, mensagem = valida_todos_dados(
        cpf="12345678901",
        email="teste@email.com",
        senha="Senha123",
        nome="João Silva",
        data_admissao="2025-05-21",
        cargo="Desenvolvedor",
        equipe="TI"
    )
    """
    validacoes = {
        "cpf": check_cpf,
        "email": check_email,
        "senha": check_password,
        "nome": check_nome,
        "data_admissao": check_data,
        "cargo": check_cargo,
        "equipe": check_equipe,
        "protocolo": check_protocolo,
        "status": check_status,
        "tipo": check_tipo_usuario,
        "parcelamento": check_parcelamento,
        "periodos": check_periodos,
        "data_solicitacao": check_data,
        "data_inicio": check_data,
        "data_fim": check_data,
        "data_aprovacao": check_data,
    }

    mensagens_erro = {
        "cpf": "CPF inválido. Deve conter 11 dígitos numéricos.",
        "email": "E-mail inválido. Formato esperado: exemplo@dominio.com",
        "senha": "Senha deve ter no mínimo 8 caracteres, incluindo maiúscula, minúscula e número.",
        "nome": "Nome inválido. Deve conter apenas letras e espaços, mínimo 3 caracteres.",
        "data_admissao": "Data inválida. Formato esperado: AAAA-MM-DD",
        "cargo": "Cargo inválido. Deve conter apenas letras e espaços, mínimo 2 caracteres.",
        "equipe": "Equipe inválida. Mínimo 2 caracteres.",
        "protocolo": "Protocolo inválido. Formato esperado: SOL-AAAAMMDD-XXXXX",
        "status": "Status inválido. Deve ser: pendente, aprovado ou reprovado",
        "tipo": "Tipo de usuário inválido. Deve ser: gestor, rh ou colaborador",
        "parcelamento": "Parcelamento deve ser um valor booleano",
        "periodos": "Períodos inválidos. Deve ser uma lista de períodos com datas válidas",
        "data_solicitacao": "Data de solicitação inválida. Formato esperado: AAAA-MM-DD",
        "data_inicio": "Data de início inválida. Formato esperado: AAAA-MM-DD",
        "data_fim": "Data de fim inválida. Formato esperado: AAAA-MM-DD",
        "data_aprovacao": "Data de aprovação inválida. Formato esperado: AAAA-MM-DD",
    }

    for campo, valor in kwargs.items():
        if campo in validacoes:
            if not validacoes[campo](valor):
                return False, mensagens_erro[campo]

    return True, "Todos os dados são válidos."
