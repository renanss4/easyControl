import json
import os
from datetime import datetime
import random
import string
from controllers.colaborador_controller import buscar_colaborador_por_cpf

def gerar_protocolo():
    """Gera um número de protocolo único no formato: SOL-YYYYMMDD-XXXXX"""
    data = datetime.now().strftime("%Y%m%d")
    aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"SOL-{data}-{aleatorio}"

def cadastrar_solicitacao(cpf_colaborador, data_inicio, data_fim, parcelamento=False):
    """
    Cadastra uma nova solicitação de férias.
    
    Args:
        cpf_colaborador (str): CPF do colaborador
        data_inicio (date): Data de início das férias
        data_fim (date): Data de fim das férias
        parcelamento (bool): Indica se as férias serão parceladas
    """
    
    # Criar estrutura da solicitação
    solicitacao = {
        "protocolo": gerar_protocolo(),
        "cpf_colaborador": cpf_colaborador,
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "data_fim": data_fim.strftime("%Y-%m-%d"),
        "parcelamento": parcelamento,
        "status": "pendente",
        "data_solicitacao": datetime.now().date().strftime("%Y-%m-%d")
    }
    
    # Verificar e criar diretório se não existir
    arquivo_solicitacoes = "data/solicitacoes.json"
    os.makedirs(os.path.dirname(arquivo_solicitacoes), exist_ok=True)
    
    # Carregar ou criar lista de solicitações
    try:
        with open(arquivo_solicitacoes, 'r') as f:
            try:
                solicitacoes = json.load(f)
            except json.JSONDecodeError:
                solicitacoes = []
    except FileNotFoundError:
        solicitacoes = []
    
    # Adicionar nova solicitação
    solicitacoes.append(solicitacao)
    
    # Salvar arquivo atualizado
    with open(arquivo_solicitacoes, 'w') as f:
        json.dump(solicitacoes, f, indent=4)
    
    return solicitacao

def obter_solicitacoes():
    """Retorna todas as solicitações cadastradas."""
    try:
        with open("data/solicitacoes.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def formatar_data(data_str):
    """Converte a data do formato ISO para DD/MM/YYYY"""
    try:
        if isinstance(data_str, str):
            data = datetime.strptime(data_str, "%Y-%m-%d")
            return data.strftime("%d/%m/%Y")
        return "N/A"
    except ValueError:
        return "N/A"

def obter_solicitacoes_detalhadas():
    """Retorna todas as solicitações cadastradas com detalhes do colaborador."""
    solicitacoes = obter_solicitacoes()
    solicitacoes_detalhadas = []
    
    for solicitacao in solicitacoes:
        colaborador = buscar_colaborador_por_cpf(solicitacao['cpf_colaborador'])
        solicitacao_detalhada = solicitacao.copy()
        solicitacao_detalhada['nome_colaborador'] = colaborador.nome if colaborador else "Colaborador não encontrado"
        
        # Formatando as datas
        solicitacao_detalhada['data_inicio'] = formatar_data(solicitacao['data_inicio'])
        solicitacao_detalhada['data_fim'] = formatar_data(solicitacao['data_fim'])
        solicitacao_detalhada['data_solicitacao'] = formatar_data(solicitacao['data_solicitacao'])
        
        solicitacoes_detalhadas.append(solicitacao_detalhada)
    
    return solicitacoes_detalhadas

