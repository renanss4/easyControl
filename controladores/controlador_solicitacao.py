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
            from telas.tela_solicitacao import TelaCadastrarSolicitacao

            self.__tela_solicitacao = TelaCadastrarSolicitacao(self)
        else:
            from telas.tela_solicitacao import TelaAnalisarSolicitacao

            self.__tela_solicitacao = TelaAnalisarSolicitacao(self)

        return self.__tela_solicitacao

    def voltar_tela_funcionario_rh(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_tela_gestor(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_gestor.abrir_tela_gestor_logado()

    def cadastrar_solicitacao(self, dados: dict) -> tuple[bool, str]:
        # Limpeza e validação básica do CPF
        cpf = dados.get("cpf_colaborador", "").strip().replace(".", "").replace("-", "")
        if not (cpf and len(cpf) == 11 and cpf.isdigit()):
            return False, "CPF inválido."

        # Busca do colaborador em diferentes categorias
        pessoa = (
            self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                cpf
            )
            or self.__controlador_sistema.controlador_funcionario_rh.buscar_funcionario_rh_por_cpf(
                cpf
            )
            or self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(cpf)
        )
        if not pessoa:
            return False, "Colaborador não encontrado."

        # Verificação de tempo de admissão
        if pessoa.data_admissao:
            meses_admissao = (date.today() - pessoa.data_admissao).days / 30.5 + 1
            meses_admissao = int(meses_admissao)  # Convertendo para inteiro
            if meses_admissao < 12:
                return False, "Colaborador deve ter pelo menos 12 meses de admissão."

        # Verificação se há solicitação pendente para o mesmo CPF
        if any(
            sol.get("status") == "PENDENTE"
            for sol in self.buscar_solicitacoes_por_cpf(cpf)
        ):
            return (
                False,
                "Já existe uma solicitação pendente para este colaborador (pelo CPF informado).",
            )

        # Nova validação: verificar se já existe solicitação pendente para a pessoa (mesmo que o CPF mude)
        solicitacoes = self.__solicitacao.carregar_solicitacoes()
        for sol in solicitacoes:
            pessoa_sol = sol.get("pessoa", {})
            if pessoa_sol.get("cpf") == pessoa.cpf and sol.get("status") == "PENDENTE":
                return False, "Esta pessoa já possui uma solicitação pendente."

        # Validação dos períodos
        periodos = dados.get("periodos", [])
        if not periodos or not all(
            isinstance(inicio, date) and isinstance(fim, date)
            for inicio, fim in periodos
        ):
            return False, "Períodos inválidos ou não informados."

        hoje = date.today()

        for inicio, fim in periodos:
            if (inicio - hoje).days < 30:
                return (
                    False,
                    "Os períodos precisam ser solicitados com no mínimo 30 dias de antecedência.",
                )
            if inicio.weekday() in [4, 5, 6]:
                return False, "As férias não podem iniciar em sexta, sábado ou domingo."
            if fim <= inicio:
                return False, "Data final do período deve ser posterior à data inicial."

        # Validação do parcelamento
        parcelamento = dados.get("parcelamento", False)
        total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)
        if parcelamento:
            if (periodos[0][1] - periodos[0][0]).days + 1 != 14:
                return False, "O primeiro período do parcelamento deve conter 14 dias."
            if len(periodos) not in [2, 3] or total_dias != 30:
                return (
                    False,
                    "Parcelamento inválido: deve ter 2 ou 3 períodos totalizando 30 dias.",
                )
        else:
            if len(periodos) != 1 or total_dias != 30:
                return False, "Período único inválido: deve conter 30 dias contínuos."

        # Garantir que os períodos não sejam sobrepostos
        for i in range(len(periodos) - 1):
            if periodos[i][1] >= periodos[i + 1][0]:
                return False, "Os períodos não podem se sobrepor."

        # Geração de protocolo único
        protocolo = f"SOL-{hoje.strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}"

        pessoa_json = {
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "cargo": pessoa.cargo,
            "data_admissao": pessoa.data_admissao.strftime("%Y-%m-%d"),
            "email": pessoa.email,
        }

        nova_solicitacao = {
            "protocolo": protocolo,
            "pessoa": pessoa_json,
            "parcelamento": parcelamento,
            "status": "PENDENTE",
            "data_solicitacao": hoje.strftime("%Y-%m-%d"),
            "periodos": [
                {
                    "DATA_INICIO": inicio.strftime("%Y-%m-%d"),
                    "DATA_FIM": fim.strftime("%Y-%m-%d"),
                }
                for inicio, fim in periodos
            ],
        }

        # Salvar a nova solicitação
        solicitacoes.append(nova_solicitacao)
        self.__solicitacao.adicionar_pessoa(pessoa)
        self.__solicitacao.salvar_solicitacoes(solicitacoes)
        return True, f"Solicitação cadastrada com sucesso. Protocolo: {protocolo}"

    def buscar_solicitacoes(self) -> list:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            # Enriquecer com dados do colaborador
            for sol in solicitacoes:
                cpf = sol.get("pessoa")["cpf"]
                if cpf:
                    colaborador = (
                        self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                            cpf
                        )
                        or self.__controlador_sistema.controlador_funcionario_rh.buscar_funcionario_rh_por_cpf(
                            cpf
                        )
                        or self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(
                            cpf
                        )
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
            return [s for s in todas_solicitacoes if s.get("pessoa")["cpf"] == cpf]
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

    def aprovar_solicitacao(
        self, protocolo: str, cpf_gestor: str = None
    ) -> tuple[bool, str]:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return (
                            False,
                            "Apenas solicitações pendentes podem ser aprovadas",
                        )

                    # VERIFICAR PORCENTAGEM DE FÉRIAS SE GESTOR FORNECIDO
                    if cpf_gestor:
                        # Obter período da solicitação para verificar sobreposição
                        periodos = sol.get("periodos", [])
                        if periodos:
                            # Usar o primeiro período como referência (pode ser expandido para todos)
                            periodo_inicio = periodos[0]["DATA_INICIO"]
                            periodo_fim = periodos[-1]["DATA_FIM"]  # Último período

                            print(f"=== VERIFICANDO APROVAÇÃO ===")
                            print(f"Protocolo: {protocolo}")
                            print(f"Período: {periodo_inicio} a {periodo_fim}")
                            print(f"Gestor: {cpf_gestor}")

                            porcentagem_com_aprovacao, pode_aprovar = (
                                self.calcular_porcentagem_ferias_equipe(
                                    cpf_gestor, periodo_inicio, periodo_fim, protocolo
                                )
                            )

                            print(
                                f"Resultado: {porcentagem_com_aprovacao:.1f}% - Pode aprovar: {pode_aprovar}"
                            )

                            if not pode_aprovar:
                                mensagem_erro = f"Não é possível aprovar esta solicitação. Durante o período de {periodo_inicio} a {periodo_fim}, a equipe teria {porcentagem_com_aprovacao:.1f}% de colaboradores em férias (máximo permitido: 50%)"
                                print(f"BLOQUEANDO APROVAÇÃO: {mensagem_erro}")
                                return False, mensagem_erro

                    sol["status"] = "APROVADA"
                    sucesso = self.__solicitacao.salvar_solicitacoes(solicitacoes)

                    if sucesso:
                        print(f"APROVAÇÃO REALIZADA COM SUCESSO: {protocolo}")
                        return True, "Solicitação aprovada com sucesso!"
                    else:
                        return False, "Erro ao salvar aprovação"

            return False, "Solicitação não encontrada"
        except Exception as e:
            print(f"Erro ao aprovar solicitação: {e}")
            return False, f"Erro interno: {str(e)}"

    def rejeitar_solicitacao(self, protocolo: str) -> tuple[bool, str]:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return (
                            False,
                            "Apenas solicitações pendentes podem ser rejeitadas",
                        )

                    sol["status"] = "REJEITADA"
                    sucesso = self.__solicitacao.salvar_solicitacoes(solicitacoes)

                    if sucesso:
                        return True, "Solicitação rejeitada com sucesso!"
                    else:
                        return False, "Erro ao salvar rejeição"

            return False, "Solicitação não encontrada"
        except Exception as e:
            print(f"Erro ao rejeitar solicitação: {e}")
            return False, f"Erro interno: {str(e)}"

    def cancelar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return False

                    sol["status"] = "CANCELADA"

                    self.__solicitacao.cancelar_solicitacao()
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao cancelar solicitação: {e}")
            return False

    def buscar_solicitacoes_equipe(self, cpf_gestor: str) -> list[dict]:
        """Busca todas as solicitações dos colaboradores da equipe do gestor"""
        try:
            # Buscar a equipe do gestor
            equipes = self.__controlador_sistema.controlador_equipe._ControladorEquipe__equipe.carregar_equipes()
            equipe_do_gestor = None

            for equipe in equipes:
                if (
                    equipe.get("gestor")
                    and isinstance(equipe["gestor"], dict)
                    and equipe["gestor"].get("cpf") == cpf_gestor
                ):
                    equipe_do_gestor = equipe
                    break

            if not equipe_do_gestor:
                print(f"Nenhuma equipe encontrada para o gestor {cpf_gestor}")
                return []

            # Obter CPFs dos colaboradores da equipe
            cpfs_colaboradores = []
            for colaborador in equipe_do_gestor.get("colaboradores", []):
                if isinstance(colaborador, dict) and colaborador.get("cpf"):
                    cpfs_colaboradores.append(colaborador["cpf"])

            if not cpfs_colaboradores:
                print("Nenhum colaborador encontrado na equipe")
                return []

            print(f"Colaboradores da equipe: {cpfs_colaboradores}")

            # Buscar solicitações de todos os colaboradores da equipe
            todas_solicitacoes = self.__solicitacao.carregar_solicitacoes()
            solicitacoes_equipe = []

            for solicitacao in todas_solicitacoes:
                pessoa = solicitacao.get("pessoa", {})
                cpf_colaborador = (
                    pessoa.get("cpf") if isinstance(pessoa, dict) else None
                )

                if cpf_colaborador in cpfs_colaboradores:
                    # Buscar nome do colaborador
                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf_colaborador
                    )
                    nome_colaborador = (
                        colaborador.nome
                        if colaborador
                        else pessoa.get("nome", "Nome não encontrado")
                    )

                    # Adicionar dados necessários à solicitação
                    solicitacao_completa = solicitacao.copy()
                    solicitacao_completa["nome_colaborador"] = nome_colaborador
                    solicitacao_completa["cpf_colaborador"] = cpf_colaborador
                    solicitacoes_equipe.append(solicitacao_completa)

            print(f"Encontradas {len(solicitacoes_equipe)} solicitações para a equipe")
            return solicitacoes_equipe

        except Exception as e:
            print(f"Erro ao buscar solicitações da equipe: {e}")
            return []

    def calcular_porcentagem_ferias_equipe(
        self,
        cpf_gestor: str,
        periodo_inicio: str = None,
        periodo_fim: str = None,
        protocolo_para_aprovar: str = None,
    ) -> tuple[float, bool]:
        """
        Calcula porcentagem de colaboradores em férias em um período específico
        Se periodo_inicio e periodo_fim forem fornecidos, considera sobreposição com esse período
        Se protocolo_para_aprovar for fornecido, simula a aprovação para calcular a nova porcentagem
        Retorna (porcentagem, pode_aprovar)
        """
        try:
            from datetime import date
            import copy

            # Buscar a equipe do gestor
            equipes = self.__controlador_sistema.controlador_equipe._ControladorEquipe__equipe.carregar_equipes()
            equipe_do_gestor = None

            for equipe in equipes:
                if (
                    equipe.get("gestor")
                    and isinstance(equipe["gestor"], dict)
                    and equipe["gestor"].get("cpf") == cpf_gestor
                ):
                    equipe_do_gestor = equipe
                    break

            if not equipe_do_gestor:
                return 0.0, True

            # Obter CPFs dos colaboradores da equipe
            cpfs_colaboradores = []
            for colaborador in equipe_do_gestor.get("colaboradores", []):
                if isinstance(colaborador, dict) and colaborador.get("cpf"):
                    cpfs_colaboradores.append(colaborador["cpf"])

            total_colaboradores = len(cpfs_colaboradores)
            if total_colaboradores == 0:
                return 0.0, True

            # Buscar todas as solicitações
            todas_solicitacoes = self.__solicitacao.carregar_solicitacoes()

            # CORRIGIR: Fazer uma cópia profunda para simular aprovação sem modificar original
            solicitacoes_simulacao = copy.deepcopy(todas_solicitacoes)

            # Se há protocolo para aprovar, simular aprovação na cópia
            if protocolo_para_aprovar:
                for sol in solicitacoes_simulacao:
                    if sol.get("protocolo") == protocolo_para_aprovar:
                        sol["status"] = "APROVADA"
                        print(
                            f"SIMULANDO APROVAÇÃO do protocolo {protocolo_para_aprovar}"
                        )
                        break

            # Contar colaboradores em férias (aprovadas) com sobreposição no período
            colaboradores_em_ferias = set()  # Usar set para evitar duplicatas

            # Se não há período específico, usar data atual
            if not periodo_inicio or not periodo_fim:
                hoje = date.today()
                periodo_inicio_date = hoje
                periodo_fim_date = hoje
            else:
                try:
                    periodo_inicio_date = date.fromisoformat(periodo_inicio)
                    periodo_fim_date = date.fromisoformat(periodo_fim)
                except ValueError:
                    return 0.0, True

            print(f"Analisando período: {periodo_inicio_date} a {periodo_fim_date}")
            print(f"Total de colaboradores na equipe: {total_colaboradores}")

            # USAR A SIMULAÇÃO PARA CALCULAR
            for solicitacao in solicitacoes_simulacao:
                if solicitacao.get("status") != "APROVADA":
                    continue

                pessoa = solicitacao.get("pessoa", {})
                cpf_colaborador = (
                    pessoa.get("cpf") if isinstance(pessoa, dict) else None
                )

                if cpf_colaborador in cpfs_colaboradores:
                    # Verificar se há sobreposição de períodos
                    periodos = solicitacao.get("periodos", [])
                    for periodo in periodos:
                        try:
                            data_inicio = date.fromisoformat(periodo["DATA_INICIO"])
                            data_fim = date.fromisoformat(periodo["DATA_FIM"])

                            # Verificar sobreposição entre os períodos
                            # Há sobreposição se: inicio1 <= fim2 AND inicio2 <= fim1
                            if (
                                data_inicio <= periodo_fim_date
                                and periodo_inicio_date <= data_fim
                            ):
                                colaboradores_em_ferias.add(cpf_colaborador)
                                print(
                                    f"Colaborador {cpf_colaborador} estará em férias no período (protocolo: {solicitacao.get('protocolo')})"
                                )
                                break
                        except (ValueError, KeyError):
                            continue

            # Calcular porcentagem
            num_colaboradores_ferias = len(colaboradores_em_ferias)
            porcentagem = (num_colaboradores_ferias / total_colaboradores) * 100
            pode_aprovar = porcentagem <= 50.0

            print(
                f"Colaboradores em férias: {num_colaboradores_ferias}/{total_colaboradores}"
            )
            print(f"Porcentagem calculada: {porcentagem:.1f}%")
            print(f"Pode aprovar: {pode_aprovar}")

            return porcentagem, pode_aprovar

        except Exception as e:
            print(f"Erro ao calcular porcentagem de férias da equipe: {e}")
            return 0.0, True
