import json
import os
from models.equipe import Equipe
from typing import List, Dict, Optional

CAMINHO_ARQUIVO = "data/equipes.json"

def _carregar_equipes() -> List[Dict]:
    """Carrega todas as equipes do arquivo JSON"""
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    try:
        with open(CAMINHO_ARQUIVO, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _salvar_equipes(equipes: List[Dict]) -> None:
    """Salva a lista de equipes no arquivo JSON"""
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(equipes, f, indent=4)

def _converter_dict_para_equipe(e: Dict) -> Equipe:
    """Converte um dicionário para objeto Equipe"""
    return Equipe(
        nome=e["nome"],
        gestor_cpf=e.get("gestor_cpf", ""),  # pode ser vazio inicialmente
        colaboradores_cpf=e.get("colaboradores_cpf", [])  # pode ser lista vazia
    )

def criar_equipe(nome: str, gestor_cpf: Optional[str] = None) -> Equipe | str:
    """
    Cria uma nova equipe.
    :param nome: Nome da equipe
    :param gestor_cpf: CPF do gestor (opcional)
    :return: Objeto Equipe ou mensagem de erro
    """
    if not nome:
        return "Nome da equipe é obrigatório."

    equipes = _carregar_equipes()
    
    # Verificar se já existe equipe com mesmo nome
    if any(e["nome"] == nome for e in equipes):
        return "Erro: Já existe uma equipe com este nome."

    nova_equipe = Equipe(
        nome=nome,
        gestor_cpf=gestor_cpf if gestor_cpf else ""
    )

    equipe_dict = {
        "nome": nova_equipe.nome,
        "gestor_cpf": nova_equipe.gestor_cpf,
        "colaboradores_cpf": []
    }

    equipes.append(equipe_dict)
    _salvar_equipes(equipes)

    return nova_equipe

def listar_equipes() -> List[Equipe]:
    """Retorna lista de todas as equipes"""
    return [_converter_dict_para_equipe(e) for e in _carregar_equipes()]

def buscar_equipe_por_nome(nome: str) -> Optional[Equipe]:
    """Busca uma equipe pelo nome"""
    equipes = _carregar_equipes()
    for equipe in equipes:
        if equipe["nome"] == nome:
            return _converter_dict_para_equipe(equipe)
    return None

def atualizar_equipe(
    nome: str,
    novo_nome: Optional[str] = None,
    novo_gestor_cpf: Optional[str] = None
) -> Equipe | str:
    """
    Atualiza os dados de uma equipe existente.
    :param nome: Nome atual da equipe
    :param novo_nome: Novo nome (opcional)
    :param novo_gestor_cpf: Novo CPF do gestor (opcional)
    :return: Equipe atualizada ou mensagem de erro
    """
    equipes = _carregar_equipes()
    
    # Procurar a equipe pelo nome atual
    for i, equipe in enumerate(equipes):
        if equipe["nome"] == nome:
            if novo_nome:
                # Verificar se o novo nome já existe em outra equipe
                if any(e["nome"] == novo_nome and e != equipe for e in equipes):
                    return "Erro: Já existe uma equipe com este nome."
                equipes[i]["nome"] = novo_nome
            
            if novo_gestor_cpf is not None:  # permite remover gestor com string vazia
                equipes[i]["gestor_cpf"] = novo_gestor_cpf
            
            _salvar_equipes(equipes)
            return _converter_dict_para_equipe(equipes[i])
            
    return "Equipe não encontrada."

def excluir_equipe(nome: str) -> bool:
    """
    Remove uma equipe pelo nome.
    Retorna True se a equipe foi removida, False caso contrário.
    """
    equipes = _carregar_equipes()
    equipes_atualizadas = [e for e in equipes if e["nome"] != nome]
    
    if len(equipes) == len(equipes_atualizadas):
        return False
        
    _salvar_equipes(equipes_atualizadas)
    return True

def adicionar_colaborador(nome_equipe: str, cpf_colaborador: str) -> bool:
    """
    Adiciona um colaborador à equipe.
    :param nome_equipe: Nome da equipe
    :param cpf_colaborador: CPF do colaborador
    :return: True se adicionado com sucesso, False caso contrário
    """
    equipes = _carregar_equipes()
    
    for equipe in equipes:
        if equipe["nome"] == nome_equipe:
            if cpf_colaborador not in equipe["colaboradores_cpf"]:
                equipe["colaboradores_cpf"].append(cpf_colaborador)
                _salvar_equipes(equipes)
                return True
    return False

def remover_colaborador(nome_equipe: str, cpf_colaborador: str) -> bool:
    """
    Remove um colaborador da equipe.
    :param nome_equipe: Nome da equipe
    :param cpf_colaborador: CPF do colaborador
    :return: True se removido com sucesso, False caso contrário
    """
    equipes = _carregar_equipes()
    
    for equipe in equipes:
        if equipe["nome"] == nome_equipe:
            if cpf_colaborador in equipe["colaboradores_cpf"]:
                equipe["colaboradores_cpf"].remove(cpf_colaborador)
                _salvar_equipes(equipes)
                return True
    return False

def listar_colaboradores_equipe(nome_equipe: str) -> List[str]:
    """
    Retorna a lista de CPFs dos colaboradores de uma equipe.
    :param nome_equipe: Nome da equipe
    :return: Lista de CPFs dos colaboradores
    """
    equipe = buscar_equipe_por_nome(nome_equipe)
    if equipe:
        return equipe.colaboradores_cpf
    return []