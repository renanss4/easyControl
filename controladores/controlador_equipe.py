from modelos.modelo_equipe import Equipe


class ControladorEquipe:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__equipe = Equipe()
        self.__tela_equipe = None

    # Navegação entre telas
    def abrir_tela_equipe(self):
        from telas.tela_equipe import TelaEquipe

        self.__tela_equipe = TelaEquipe(self)
        return self.__tela_equipe

    def voltar_tela_funcionario_rh(self):
        self.__tela_equipe = None
        self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    # CRUD de Equipe
    def cadastrar_equipe(self, dados: dict) -> bool:
        try:
            # Validar nome da equipe
            nome = dados.get("nome", "").strip()
            if not nome:
                return False
            if len(nome) < 3:
                return False

            # Validar se equipe já existe
            equipes = self.__equipe.carregar_equipes()
            for equipe in equipes:
                if equipe.get("nome", "").lower() == nome.lower():
                    return False

            cpf_gestor = dados.get("cpf_gestor", "").strip()
            colaboradores_cpf = dados.get("colaboradores_cpf", [])

            # Validar gestor (se fornecido)
            if cpf_gestor:
                cpf_limpo = cpf_gestor.replace(".", "").replace("-", "")
                if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                    return False

                gestor = self.__controlador_sistema.controlador_gestor.buscar_por_cpf(
                    cpf_gestor
                )
                if not gestor:
                    return False

            # Validar colaboradores
            cpfs_validados = []
            for cpf in colaboradores_cpf:
                if cpf.strip():
                    cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
                    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                        return False

                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf.strip()
                    )
                    if not colaborador:
                        return False

                    if cpf.strip() in cpfs_validados:
                        return False

                    cpfs_validados.append(cpf.strip())

            # Criar nova equipe
            nova_equipe = {
                "nome": nome,
                "cpf_gestor": cpf_gestor,
                "colaboradores_cpf": cpfs_validados,
            }

            equipes.append(nova_equipe)
            return self.__equipe.salvar_equipes(equipes)

        except Exception as e:
            print(f"Erro ao cadastrar equipe: {e}")
            return False

    def buscar_equipes(self) -> list[dict]:
        try:
            equipes = self.__equipe.carregar_equipes()

            # Enriquecer com nomes
            for equipe in equipes:
                # Nome do gestor
                cpf_gestor = equipe.get("cpf_gestor", "")
                if cpf_gestor:
                    gestor = (
                        self.__controlador_sistema.controlador_gestor.buscar_por_cpf(
                            cpf_gestor
                        )
                    )
                    equipe["nome_gestor"] = (
                        gestor.nome if gestor else "Gestor não encontrado"
                    )
                else:
                    equipe["nome_gestor"] = "Sem gestor"

                # Nomes dos colaboradores
                colaboradores_nomes = []
                for cpf in equipe.get("colaboradores_cpf", []):
                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf
                    )
                    if colaborador:
                        colaboradores_nomes.append(colaborador.nome)
                    else:
                        colaboradores_nomes.append(f"CPF {cpf} não encontrado")

                equipe["colaboradores_nomes"] = colaboradores_nomes
                equipe["total_colaboradores"] = len(equipe.get("colaboradores_cpf", []))

            return equipes

        except Exception as e:
            print(f"Erro ao buscar equipes: {e}")
            return []

    def buscar_equipe_por_nome(self, nome: str) -> dict:
        try:
            equipes = self.buscar_equipes()
            for equipe in equipes:
                if equipe.get("nome", "").lower() == nome.lower():
                    return equipe
            return None
        except Exception as e:
            print(f"Erro ao buscar equipe por nome: {e}")
            return None

    def atualizar_equipe(self, nome_atual: str, dados: dict) -> bool:
        # aqui é onde pode adicionar colaboradores e gestores e remover também
        try:
            # Validar nome da equipe
            nome = dados.get("nome", "").strip()
            if not nome:
                return False
            if len(nome) < 3:
                return False

            # Validar se novo nome já existe (exceto para a equipe atual)
            equipes = self.__equipe.carregar_equipes()
            for equipe in equipes:
                if (
                    equipe.get("nome", "").lower() == nome.lower()
                    and equipe.get("nome") != nome_atual
                ):
                    return False

            cpf_gestor = dados.get("cpf_gestor", "").strip()
            colaboradores_cpf = dados.get("colaboradores_cpf", [])

            # Validar gestor (se fornecido)
            if cpf_gestor:
                cpf_limpo = cpf_gestor.replace(".", "").replace("-", "")
                if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                    return False

                gestor = self.__controlador_sistema.controlador_gestor.buscar_por_cpf(
                    cpf_gestor
                )
                if not gestor:
                    return False

            # Validar colaboradores
            cpfs_validados = []
            for cpf in colaboradores_cpf:
                if cpf.strip():
                    cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
                    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                        return False

                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf.strip()
                    )
                    if not colaborador:
                        return False

                    if cpf.strip() in cpfs_validados:
                        return False

                    cpfs_validados.append(cpf.strip())

            # Atualizar equipe
            for i, equipe in enumerate(equipes):
                if equipe.get("nome") == nome_atual:
                    equipes[i] = {
                        "nome": nome,
                        "cpf_gestor": cpf_gestor,
                        "colaboradores_cpf": cpfs_validados,
                    }
                    return self.__equipe.salvar_equipes(equipes)

            return False  # Equipe não encontrada

        except Exception as e:
            print(f"Erro ao atualizar equipe: {e}")
            return False

    def excluir_equipe(self, nome: str) -> bool:
        try:
            equipes = self.__equipe.carregar_equipes()
            equipes_filtradas = [
                equipe for equipe in equipes if equipe.get("nome") != nome
            ]

            if len(equipes) == len(equipes_filtradas):
                return False  # Equipe não encontrada

            return self.__equipe.salvar_equipes(equipes_filtradas)

        except Exception as e:
            print(f"Erro ao excluir equipe: {e}")
            return False

    # Métodos adicionais
    def obter_colaboradores_sem_equipe(self) -> list[dict]:
        try:
            # Buscar todos os colaboradores
            todos_colaboradores = self.__controlador_sistema.controlador_colaborador.buscar_colaboradores()

            # Buscar CPFs já em equipes
            equipes = self.__equipe.carregar_equipes()
            cpfs_em_equipes = set()

            for equipe in equipes:
                cpfs_em_equipes.update(equipe.get("colaboradores_cpf", []))

            # Filtrar colaboradores sem equipe
            colaboradores_sem_equipe = []
            for colaborador in todos_colaboradores:
                if (
                    hasattr(colaborador, "cpf")
                    and colaborador.cpf not in cpfs_em_equipes
                ):
                    colaboradores_sem_equipe.append(
                        {"cpf": colaborador.cpf, "nome": colaborador.nome}
                    )

            return colaboradores_sem_equipe

        except Exception as e:
            print(f"Erro ao obter colaboradores sem equipe: {e}")
            return []

    def obter_gestores_sem_equipe(self) -> list[dict]:
        try:
            # Buscar todos os gestores
            todos_gestores = (
                self.__controlador_sistema.controlador_gestor.buscar_gestores()
            )

            # Buscar CPFs de gestores já em equipes
            equipes = self.__equipe.carregar_equipes()
            cpfs_gestores_em_equipes = set()

            for equipe in equipes:
                cpf_gestor = equipe.get("cpf_gestor", "")
                if cpf_gestor:
                    cpfs_gestores_em_equipes.add(cpf_gestor)

            # Filtrar gestores sem equipe
            gestores_sem_equipe = []
            for gestor in todos_gestores:
                if (
                    hasattr(gestor, "cpf")
                    and gestor.cpf not in cpfs_gestores_em_equipes
                ):
                    gestores_sem_equipe.append({"cpf": gestor.cpf, "nome": gestor.nome})

            return gestores_sem_equipe

        except Exception as e:
            print(f"Erro ao obter gestores sem equipe: {e}")
            return []

    def calcular_porcentagem_colaboradores_ferias(self, codigo_equipe: str) -> float:
        try:
            from datetime import date

            # Buscar equipe
            equipe = self.buscar_por_codigo(codigo_equipe)
            if not equipe:
                return 0.0

            # Buscar colaboradores da equipe
            colaboradores_equipe = equipe.get("colaboradores", [])
            total_colaboradores = len(colaboradores_equipe)

            if total_colaboradores == 0:
                return 0.0

            # Contar colaboradores em férias
            colaboradores_em_ferias = 0
            hoje = date.today()

            # Buscar todas as solicitações aprovadas
            solicitacoes = (
                self.__controlador_sistema.controlador_solicitacao.buscar_solicitacoes()
            )
            solicitacoes_aprovadas = [
                s for s in solicitacoes if s.get("status") == "aprovado"
            ]

            for cpf_colaborador in colaboradores_equipe:
                # Verificar se o colaborador tem solicitação aprovada em período atual
                for solicitacao in solicitacoes_aprovadas:
                    if solicitacao.get("cpf_colaborador") == cpf_colaborador:
                        # Verificar se está dentro do período de férias
                        periodos = solicitacao.get("periodos", [])
                        for periodo in periodos:
                            data_inicio = date.fromisoformat(periodo["data_inicio"])
                            data_fim = date.fromisoformat(periodo["data_fim"])

                            if data_inicio <= hoje <= data_fim:
                                colaboradores_em_ferias += 1
                                break  # Já contou este colaborador, sair do loop
                        break  # Já verificou a solicitação deste colaborador

            # Calcular porcentagem
            # retornar o número inteiro de quem já está de férias
            # retornar o número total
            porcentagem = (colaboradores_em_ferias / total_colaboradores) * 100
            return porcentagem  # colaboradores_em_ferias, total_colaboradores

        except Exception as e:
            print(f"Erro ao calcular porcentagem de colaboradores em férias: {e}")
            return 0.0
