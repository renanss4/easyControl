import json
import os
from datetime import datetime, date
import random
import string
from typing import List, Dict, Tuple
from controllers.colaborador_controller import buscar_colaborador_por_cpf
from controllers.usuario_controller import buscar_usuario_por_cpf

ARQUIVO_SOLICITACOES = "data/solicitacoes.json"


def _carregar_solicitacoes() -> List[Dict]:
    if not os.path.exists(ARQUIVO_SOLICITACOES):
        return []
    try:
        with open(ARQUIVO_SOLICITACOES, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _salvar_solicitacoes(solicitacoes: List[Dict]) -> None:
    os.makedirs(os.path.dirname(ARQUIVO_SOLICITACOES), exist_ok=True)
    with open(ARQUIVO_SOLICITACOES, "w") as f:
        json.dump(solicitacoes, f, indent=4)


def _formatar_data(data_str: str) -> str:
    """Converte data ISO (YYYY-MM-DD) para DD/MM/YYYY"""
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return "N/A"


def gerar_protocolo() -> str:
    """Gera um número de protocolo único no formato: SOL-YYYYMMDD-XXXXX"""
    data = datetime.now().strftime("%Y%m%d")
    aleatorio = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"SOL-{data}-{aleatorio}"


def cadastrar_solicitacao(
    cpf_colaborador: str, data_inicio: date, data_fim: date
) -> Dict:
    # deve ser usado apenas se o usuario logado for do tipo rh
    """Cadastra uma nova solicitação de férias"""

    solicitacao = {
        "protocolo": gerar_protocolo(),
        "cpf_colaborador": cpf_colaborador,
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_fim": data_fim.strftime("%Y-%m-%d"),
        "parcelamento": False,
        "status": "pendente",
        "data_solicitacao": datetime.now().strftime("%Y-%m-%d"),
    }

    solicitacoes = _carregar_solicitacoes()
    solicitacoes.append(solicitacao)
    _salvar_solicitacoes(solicitacoes)

    return solicitacao


def obter_solicitacoes() -> List[Dict]:
    """Retorna todas as solicitações cadastradas"""
    return _carregar_solicitacoes()


def obter_solicitacoes_detalhadas() -> List[Dict]:
    """Retorna as solicitações com informações adicionais do colaborador/usuário"""
    solicitacoes = _carregar_solicitacoes()
    detalhadas = []

    for sol in solicitacoes:
        # Buscar tanto usuário quanto colaborador
        usuario = buscar_usuario_por_cpf(sol["cpf_colaborador"])
        colaborador = buscar_colaborador_por_cpf(sol["cpf_colaborador"])

        # Se não encontrar nem usuário nem colaborador, pula
        if not colaborador and not usuario:
            continue

        sol_detalhada = sol.copy()

        # Determinar o nome a ser exibido (prioriza colaborador)
        if colaborador:
            sol_detalhada["nome_colaborador"] = colaborador.nome
        elif usuario:
            sol_detalhada["nome_colaborador"] = usuario.nome
        else:
            sol_detalhada["nome_colaborador"] = "Nome não encontrado"

        # Formatação de datas
        sol_detalhada["data_solicitacao"] = _formatar_data(sol["data_solicitacao"])

        # Lidar com diferentes formatos de período
        if "periodos" in sol:
            # Formato novo (parcelado)
            periodos_formatados = []
            for periodo in sol["periodos"]:
                inicio = _formatar_data(periodo["data_inicio"])
                fim = _formatar_data(periodo["data_fim"])
                periodos_formatados.append({"data_inicio": inicio, "data_fim": fim})
            sol_detalhada["periodos"] = periodos_formatados
        else:
            # Formato antigo (período único)
            sol_detalhada["periodos"] = [
                {
                    "data_inicio": _formatar_data(sol["data_inicio"]),
                    "data_fim": _formatar_data(sol["data_fim"]),
                }
            ]

        detalhadas.append(sol_detalhada)

    return detalhadas


def buscar_solicitacoes_por_cpf(cpf_colaborador: str) -> List[Dict]:
    """Busca e retorna as solicitações de um colaborador/usuário específico (por CPF)"""
    solicitacoes = _carregar_solicitacoes()
    filtradas = [s for s in solicitacoes if s["cpf_colaborador"] == cpf_colaborador]

    # Buscar informações do colaborador/usuário
    usuario = buscar_usuario_por_cpf(cpf_colaborador)
    colaborador = buscar_colaborador_por_cpf(cpf_colaborador)

    nome_exibicao = None
    if colaborador:
        nome_exibicao = colaborador.nome
    if usuario:
        nome_exibicao = usuario.nome if not nome_exibicao else nome_exibicao
    if not nome_exibicao:
        nome_exibicao = "Nome não encontrado"

    for s in filtradas:
        s["nome_colaborador"] = nome_exibicao

        if "periodos" in s:
            # Para solicitações com múltiplos períodos
            periodos_formatados = []
            for p in s["periodos"]:
                inicio = _formatar_data(p["data_inicio"])
                fim = _formatar_data(p["data_fim"])
                periodos_formatados.append(f"{inicio} a {fim}")
            s["periodos_formatados"] = " | ".join(periodos_formatados)
        else:
            # Para solicitações antigas com período único
            s["periodos_formatados"] = (
                f"{_formatar_data(s.get('data_inicio', 'N/A'))} a {_formatar_data(s.get('data_fim', 'N/A'))}"
            )

        s["data_solicitacao"] = _formatar_data(s["data_solicitacao"])

    return filtradas


def cancelar_solicitacao(protocolo: str) -> bool:
    """Atualiza o status de uma solicitação para 'cancelada'"""
    solicitacoes = _carregar_solicitacoes()
    for s in solicitacoes:
        if s["protocolo"] == protocolo and s["status"] == "pendente":
            s["status"] = "cancelada"
            _salvar_solicitacoes(solicitacoes)
            return True
    return False


def aprovar_solicitacao(protocolo: str) -> bool:
    """
    Aprova uma solicitação de férias.

    Args:
        protocolo: Protocolo da solicitação a ser aprovada

    Returns:
        bool: True se aprovada com sucesso, False caso contrário
    """
    solicitacoes = _carregar_solicitacoes()

    for sol in solicitacoes:
        if sol.get("protocolo") == protocolo:
            sol["status"] = "aprovado"
            _salvar_solicitacoes(solicitacoes)
            return True

    return False


def rejeitar_solicitacao(protocolo: str) -> bool:
    """
    Rejeita uma solicitação de férias.

    Args:
        protocolo: Protocolo da solicitação a ser rejeitada

    Returns:
        bool: True se rejeitada com sucesso, False caso contrário
    """
    solicitacoes = _carregar_solicitacoes()

    for sol in solicitacoes:
        if sol.get("protocolo") == protocolo:
            sol["status"] = "rejeitado"
            _salvar_solicitacoes(solicitacoes)
            return True

    return False


def calcular_dias_ferias(data_inicio: date, data_fim: date) -> int:
    """os dias no total não pode ultrapassar 30"""
    delta = (data_fim - data_inicio).days
    if delta < 0:
        raise ValueError("A data de fim deve ser maior que a data de início.")
    return min(delta, 30)


def validar_periodo_ferias(data_inicio: date, data_fim: date) -> Tuple[bool, str]:
    """
    Valida se um período de férias é válido.
    Retorna uma tupla (válido, mensagem).
    """
    if data_inicio > data_fim:
        return False, "Data de início deve ser anterior à data de fim"

    dias = (data_fim - data_inicio).days + 1

    if dias < 5:  # Mínimo de 5 dias por período
        return False, "Período mínimo de férias deve ser 5 dias"

    return True, ""


def validar_parcelamento_ferias(periodos: List[Tuple[date, date]]) -> Tuple[bool, str]:
    """
    Valida se o parcelamento de férias está correto.
    Retorna uma tupla (válido, mensagem).
    """
    if not periodos:
        return False, "Nenhum período informado"

    # Validar antecedência de 30 dias para todos os períodos
    for inicio, _ in periodos:
        valido, msg = validar_antecedencia_minima(inicio)
        if not valido:
            return False, msg

    # Validar dia da semana para início das férias
    for inicio, _ in periodos:
        valido, msg = validar_dia_semana_inicio(inicio)
        if not valido:
            return False, msg

    # Se for parcelado, validar primeiro período de 14 dias
    if len(periodos) > 1:
        valido, msg = validar_primeiro_periodo_parcelado(periodos[0][0], periodos[0][1])
        if not valido:
            return False, msg

    total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)
    if total_dias > 30:
        return False, "Total de dias não pode exceder 30"

    if len(periodos) > 3:
        return False, "Máximo de 3 períodos permitidos"

    # Validar tamanho mínimo de cada período
    for inicio, fim in periodos:
        dias = (fim - inicio).days + 1
        if dias < 5:
            return False, "Cada período deve ter no mínimo 5 dias"

    return True, ""


def calcular_parcelamento(dias_totais: int) -> List[int]:
    """
    Calcula as opções possíveis de parcelamento baseado no total de dias.
    Retorna uma lista com as possibilidades de parcelamento.
    """
    opcoes = []

    # Período único
    if 5 <= dias_totais <= 30:
        opcoes.append([dias_totais])

    # Dois períodos
    if dias_totais >= 10:  # Mínimo 5 dias cada período
        for p1 in range(5, min(dias_totais - 4, 20)):  # deixa pelo menos 5 dias para p2
            p2 = dias_totais - p1
            if p2 >= 5:
                opcoes.append([p1, p2])

    # Três períodos
    if dias_totais >= 15:  # Mínimo 5 dias cada período
        for p1 in range(5, min(dias_totais - 9, 20)):
            for p2 in range(5, min(dias_totais - p1 - 4, 15)):
                p3 = dias_totais - p1 - p2
                if p3 >= 5:
                    opcoes.append([p1, p2, p3])

    return opcoes


def validar_cpf_cadastrado(cpf: str) -> Tuple[bool, str]:
    """Verifica se o CPF está cadastrado como usuário ou colaborador"""
    from controllers.colaborador_controller import buscar_colaborador_por_cpf
    from controllers.usuario_controller import buscar_usuario_por_cpf

    colaborador = buscar_colaborador_por_cpf(cpf)
    usuario = buscar_usuario_por_cpf(cpf)

    if not colaborador and not usuario:
        return False, "CPF não encontrado no sistema"

    return True, ""


def cadastrar_solicitacao_parcelada(
    cpf_colaborador: str, periodos: list[tuple[date, date]], parcelamento: bool = True
) -> list[dict] | bool:
    """
    Cadastra uma solicitação de férias parcelada.
    """
    # Validar CPF
    valido, mensagem = validar_cpf_cadastrado(cpf_colaborador)
    if not valido:
        raise ValueError(mensagem)

    # Validar períodos
    valido, mensagem = validar_parcelamento_ferias(periodos)
    if not valido:
        raise ValueError(mensagem)

    solicitacao = {
        "protocolo": gerar_protocolo(),
        "cpf_colaborador": cpf_colaborador,
        "parcelamento": parcelamento,
        "status": "pendente",
        "data_solicitacao": datetime.now().strftime("%Y-%m-%d"),
        "periodos": [
            {
                "data_inicio": inicio.strftime("%Y-%m-%d"),
                "data_fim": fim.strftime("%Y-%m-%d"),
            }
            for inicio, fim in periodos
        ],
    }

    solicitacoes = _carregar_solicitacoes()
    solicitacoes.append(solicitacao)
    _salvar_solicitacoes(solicitacoes)

    return solicitacao


def validar_antecedencia_minima(data_inicio: date) -> Tuple[bool, str]:
    """Valida se a data de início tem antecedência mínima de 30 dias."""
    hoje = date.today()
    dias_antecedencia = (data_inicio - hoje).days

    if dias_antecedencia < 30:
        return (
            False,
            "A solicitação deve ser feita com no mínimo 30 dias de antecedência",
        )

    return True, ""


def validar_dia_semana_inicio(data_inicio: date) -> Tuple[bool, str]:
    """Valida se a data de início é em um dia útil no início da semana (exceto sexta)."""
    dia_semana = data_inicio.weekday()

    # Verifica se é fim de semana (5=sábado, 6=domingo)
    if dia_semana in [5, 6]:
        return False, "As férias devem iniciar em um dia útil"

    # Verifica se é sexta-feira (4)
    if dia_semana == 4:
        return False, "As férias não podem iniciar em uma sexta-feira"

    return True, ""


def validar_primeiro_periodo_parcelado(
    data_inicio: date, data_fim: date
) -> Tuple[bool, str]:
    """Valida se o primeiro período do parcelamento tem 14 dias."""
    dias = (data_fim - data_inicio).days + 1

    if dias != 14:
        return False, "O primeiro período do parcelamento deve ter exatamente 14 dias"

    return True, ""
