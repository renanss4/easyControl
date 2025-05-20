import json
import os
from datetime import datetime, date
import random
import string
from typing import List, Dict, Tuple
from controllers.colaborador_controller import buscar_colaborador_por_cpf

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
    cpf_colaborador: str, data_inicio: date, data_fim: date, parcelamento: bool = False
) -> Dict:
    # deve ser usado apenas se o usuario logado for do tipo rh
    """Cadastra uma nova solicitação de férias"""

    solicitacao = {
        "protocolo": gerar_protocolo(),
        "cpf_colaborador": cpf_colaborador,
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_fim": data_fim.strftime("%Y-%m-%d"),
        "parcelamento": parcelamento,
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
    """Retorna as solicitações com informações adicionais do colaborador"""
    solicitacoes = _carregar_solicitacoes()
    detalhadas = []

    for sol in solicitacoes:
        colaborador = buscar_colaborador_por_cpf(sol["cpf_colaborador"])

        sol_detalhada = sol.copy()
        sol_detalhada["nome_colaborador"] = (
            colaborador.nome if colaborador else "Colaborador não encontrado"
        )

        # Formatação de datas
        sol_detalhada["data_inicio"] = _formatar_data(sol["data_inicio"])
        sol_detalhada["data_fim"] = _formatar_data(sol["data_fim"])
        sol_detalhada["data_solicitacao"] = _formatar_data(sol["data_solicitacao"])

        detalhadas.append(sol_detalhada)

    return detalhadas


def buscar_solicitacoes_por_cpf(cpf_colaborador: str) -> List[Dict]:
    """Busca e retorna as solicitações de um colaborador específico (por CPF)"""
    solicitacoes = _carregar_solicitacoes()
    filtradas = [s for s in solicitacoes if s["cpf_colaborador"] == cpf_colaborador]

    for s in filtradas:
        s["data_inicio"] = _formatar_data(s["data_inicio"])
        s["data_fim"] = _formatar_data(s["data_fim"])
        s["data_solicitacao"] = _formatar_data(s["data_solicitacao"])

    return filtradas


def cancelar_solicitacao(protocolo: str) -> bool:
    # deve ser usado apenas se o usuario logado for do tipo rh
    """Atualiza o status de uma solicitação para 'cancelada'"""
    solicitacoes = _carregar_solicitacoes()
    for s in solicitacoes:
        if s["protocolo"] == protocolo:
            s["status"] = "cancelada"
            _salvar_solicitacoes(solicitacoes)
            return True
    return False


def aprovar_solicitacao(protocolo: str) -> bool:
    # deve ser usado apenas se o usuario logado for do tipo gestor
    """Atualiza o status de uma solicitação para 'aprovada'"""
    solicitacoes = _carregar_solicitacoes()
    for s in solicitacoes:
        if s["protocolo"] == protocolo:
            s["status"] = "aprovada"
            _salvar_solicitacoes(solicitacoes)
            return True
    return False


def rejeitar_solicitacao(protocolo: str) -> bool:
    # deve ser usado apenas se o usuario logado for do tipo gestor
    """Atualiza o status de uma solicitação para 'rejeitada'"""
    solicitacoes = _carregar_solicitacoes()
    for s in solicitacoes:
        if s["protocolo"] == protocolo:
            s["status"] = "rejeitada"
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

    total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)
    if total_dias > 30:
        return False, "Total de dias não pode exceder 30"

    if len(periodos) > 3:
        return False, "Máximo de 3 períodos permitidos"

    # Validar tamanho de cada período
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


def cadastrar_solicitacao_parcelada(
    cpf_colaborador: str, periodos: List[Tuple[date, date]], parcelamento: bool = True
) -> Dict:
    """
    Cadastra uma solicitação de férias parcelada.
    """
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
