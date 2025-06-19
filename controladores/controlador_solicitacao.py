from modelos.modelo_solicitacao import Solicitacao
from datetime import date
import random
import string


class ControladorSolicitacao:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__solicitacao = Solicitacao()
        self.__tela_solicitacao = None

    def abrir_tela_solicitacao(self):
        usuario_logado = self.__controlador_sistema.usuario_logado

        if hasattr(usuario_logado, "__class__") and "FuncionarioRH" in str(
            usuario_logado.__class__
        ):
            from telas.tela_solicitacao import CadastraSolicitacao

            self.__tela_solicitacao = CadastraSolicitacao(self)
        else:
            from telas.tela_solicitacao import AnalisarSolicitacao

            self.__tela_solicitacao = AnalisarSolicitacao(self)

        return self.__tela_solicitacao

    def voltar_tela_funcionario_rh(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_tela_gestor(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_gestor.abrir_tela_gestor_logado()

    def cadastrar_solicitacao(self, dados: dict) -> bool:
        try:
            # Validar CPF
            cpf = dados.get("cpf_colaborador", "").strip()
            if not cpf:
                return False

            cpf_limpo = cpf.replace(".", "").replace("-", "")
            if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                return False

            # Verificar se colaborador existe
            colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                cpf
            )
            if not colaborador:
                return False

            # Verificar se colaborador tem pelo menos 12 meses de admissão
            if hasattr(colaborador, "data_admissao"):
                meses_admissao = (date.today() - colaborador.data_admissao).days / 30.44
                if meses_admissao < 12:
                    return False

            # Verificar se não há solicitação pendente
            solicitacoes_existentes = self.buscar_solicitacoes_por_cpf(cpf)
            if any(sol.get("status") == "pendente" for sol in solicitacoes_existentes):
                return False

            # Verificar se a equipe já tem 50% ou mais em férias
            equipes = self.__controlador_sistema.controlador_equipe.buscar_equipes()
            for equipe in equipes:
                colaboradores_cpf = equipe.get("colaboradores_cpf", [])
                if cpf in colaboradores_cpf:
                    nome_equipe = equipe.get("nome")
                    if nome_equipe:
                        porcentagem_ferias = self.__controlador_sistema.controlador_equipe.calcular_porcentagem_colaboradores_ferias(
                            nome_equipe
                        )
                        if porcentagem_ferias >= 50.0:
                            return False
                    break

            # Validar períodos
            periodos = dados.get("periodos", [])
            if not periodos:
                return False

            # Validar cada período
            for inicio, fim in periodos:
                if not isinstance(inicio, date) or not isinstance(fim, date):
                    return False

                # Antecedência mínima de 30 dias
                if (inicio - date.today()).days < 30:
                    return False

                # Não pode iniciar sexta/sábado/domingo
                if inicio.weekday() in [4, 5, 6]:
                    return False

                # Fim deve ser após início
                if fim <= inicio:
                    return False

            # Validar parcelamento
            parcelamento = dados.get("parcelamento", False)
            total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)

            if not parcelamento:
                if len(periodos) > 1 or total_dias != 30:
                    return False
            else:
                if len(periodos) < 2 or len(periodos) > 3 or total_dias != 30:
                    return False

                # Primeiro período deve ter 14 dias
                primeiro_periodo = periodos[0]
                if (primeiro_periodo[1] - primeiro_periodo[0]).days + 1 != 14:
                    return False

            # Validar períodos sequenciais (não podem se sobrepor)
            for i in range(len(periodos) - 1):
                if periodos[i][1] >= periodos[i + 1][0]:
                    return False

            data = date.today().strftime("%Y%m%d")
            aleatorio = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=5)
            )
            protocolo = f"SOL-{data}-{aleatorio}"

            # Criar nova solicitação
            nova_solicitacao = {
                "protocolo": protocolo,
                "cpf_colaborador": cpf,
                "parcelamento": parcelamento,
                "status": "pendente",
                "data_solicitacao": date.today().strftime("%Y-%m-%d"),
                "periodos": [
                    {
                        "data_inicio": inicio.strftime("%Y-%m-%d"),
                        "data_fim": fim.strftime("%Y-%m-%d"),
                    }
                    for inicio, fim in periodos
                ],
            }

            # Salvar
            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            solicitacoes.append(nova_solicitacao)
            return self.__solicitacao.salvar_solicitacoes(solicitacoes)

        except Exception as e:
            print(f"Erro ao cadastrar solicitação: {e}")
            return False

    def buscar_solicitacoes(self) -> list:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            # Enriquecer com dados do colaborador
            for sol in solicitacoes:
                cpf = sol.get("cpf_colaborador")
                if cpf:
                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf
                    )
                    if colaborador:
                        sol["nome_colaborador"] = colaborador.nome
                    else:
                        sol["nome_colaborador"] = "Nome não encontrado"
                else:
                    sol["nome_colaborador"] = "CPF não informado"

            return solicitacoes
        except Exception as e:
            print(f"Erro ao buscar solicitações: {e}")
            return []

    def buscar_solicitacoes_por_cpf(self, cpf: str) -> list:
        try:
            todas_solicitacoes = self.buscar_solicitacoes()
            return [s for s in todas_solicitacoes if s.get("cpf_colaborador") == cpf]
        except Exception as e:
            print(f"Erro ao buscar solicitações por CPF: {e}")
            return []

    def buscar_solicitacao_por_protocolo(self, protocolo: str) -> dict | None:
        try:
            solicitacoes = self.buscar_solicitacoes()
            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    return sol
            return None
        except Exception as e:
            print(f"Erro ao buscar solicitação: {e}")
            return None

    def aprovar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "pendente":
                        return False

                    sol["status"] = "aprovado"
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao aprovar solicitação: {e}")
            return False

    def rejeitar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "pendente":
                        return False

                    sol["status"] = "rejeitado"
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao rejeitar solicitação: {e}")
            return False

    def cancelar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "pendente":
                        return False

                    sol["status"] = "cancelado"
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao cancelar solicitação: {e}")
            return False
