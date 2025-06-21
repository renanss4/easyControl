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
    def cadastrar_equipe(self, dados: dict) -> tuple[bool, str]:
        print(f"Dados recebidos para cadastro de equipe: {dados}") 
        try:
            # Validar nome da equipe
            nome = dados.get("nome", "").strip()
            if not nome:
                return False, "Nome da equipe é obrigatório"
            if len(nome) < 3:
                return False, "Nome da equipe deve ter pelo menos 3 caracteres"

            # Validar se equipe já existe
            equipes = self.__equipe.carregar_equipes()
            for equipe in equipes:
                if equipe.get("nome", "").lower() == nome.lower():
                    return False, "Já existe uma equipe com este nome"

            cpf_gestor = dados.get("gestor", "").strip()
            print(f"CPF do gestor: {cpf_gestor}")
            colaboradores_cpf = dados.get("colaboradores", [])
            print(f"CPFs dos colaboradores: {colaboradores_cpf}")
            
            # Validar gestor (se fornecido)
            gestor_json = None
            if cpf_gestor:
                cpf_limpo = cpf_gestor.replace(".", "").replace("-", "")
                if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                    return False, "CPF do gestor inválido"
                print(f"Buscando gestor com CPF: {cpf_gestor}") 
                gestor = self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(
                    cpf_gestor
                )
                print(f"Gestor encontrado: {gestor}")
                if not gestor:
                    return False, "Gestor não encontrado"
                print(gestor.nome)
                
                gestor_json = {
                    "cpf": gestor.cpf,
                    "nome": gestor.nome,
                    "email": gestor.email,
                    "cargo": gestor.cargo,
                }
            
            # Validar colaboradores
            cpfs_validados = []
            for cpf in colaboradores_cpf:
                if cpf.strip():
                    cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
                    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                        return False, f"CPF inválido: {cpf}"

                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf.strip()
                    )
                    if not colaborador:
                        return False, f"Colaborador não encontrado: {cpf}"

                    if cpf.strip() in cpfs_validados:
                        return False, f"CPF duplicado: {cpf}"

                    cpfs_validados.append(cpf.strip())

            colaborador_json = [
                {
                    "cpf": cpf,
                    "nome": self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(cpf).nome,
                    "email": self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(cpf).email,
                    "cargo": self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(cpf).cargo,
                }
                for cpf in cpfs_validados
            ]

            print(f"Gestor JSON: {gestor_json}")
            print(f"Colaboradores JSON: {colaborador_json}")
            
            # Criar nova equipe
            nova_equipe = {
                "nome": nome,
                "gestor": gestor_json,  # Pode ser None se não houver gestor
                "colaboradores": colaborador_json,
            }
            print(nova_equipe)
            equipes.append(nova_equipe)
            sucesso = self.__equipe.salvar_equipes(equipes)
            
            if sucesso:
                return True, "Equipe cadastrada com sucesso!"
            else:
                return False, "Erro ao salvar equipe no banco de dados"

        except Exception as e:
            print(f"Erro ao cadastrar equipe: {e}")
            return False, f"Erro interno: {str(e)}"

    def buscar_equipes(self) -> list[dict]:
        try:
            equipes = self.__equipe.carregar_equipes()

            # Enriquecer com nomes
            for equipe in equipes:
                # Nome do gestor
                if "gestor" in equipe and equipe["gestor"] and isinstance(equipe["gestor"], dict):
                    cpf_gestor = equipe["gestor"].get("cpf")
                    if cpf_gestor:
                        gestor = self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(
                            cpf_gestor
                        )
                        equipe["gestor"] = (
                            gestor.nome if gestor else "Gestor não encontrado"
                        )
                    else:
                        equipe["gestor"] = "Sem gestor"
                else:
                    equipe["gestor"] = "Sem gestor"

                # Nomes dos colaboradores
                colaboradores_nomes = []
                for colaborador in equipe.get("colaboradores", []):
                    cpf = colaborador.get("cpf")
                    if cpf:
                        colaborador_obj = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                            cpf
                        )
                        if colaborador_obj:
                            colaboradores_nomes.append(colaborador_obj.nome)
                        else:
                            colaboradores_nomes.append(f"CPF {cpf} não encontrado")

                equipe["colaboradores_nomes"] = colaboradores_nomes
                equipe["total_colaboradores"] = len(equipe.get("colaboradores", []))

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

    def atualizar_equipe(self, nome_atual: str, dados: dict) -> tuple[bool, str]:
        """Atualiza uma equipe existente, permitindo adicionar/remover colaboradores e gestor"""
        try:
            # Validar nome da equipe
            nome = dados.get("nome", "").strip()
            if not nome:
                return False, "Nome da equipe é obrigatório"
            if len(nome) < 3:
                return False, "Nome da equipe deve ter pelo menos 3 caracteres"

            # Carregar equipes
            equipes = self.__equipe.carregar_equipes()
            
            # Validar se novo nome já existe (exceto para a equipe atual)
            for equipe in equipes:
                if (
                    equipe.get("nome", "").lower() == nome.lower()
                    and equipe.get("nome") != nome_atual
                ):
                    return False, "Já existe uma equipe com este nome"

            cpf_gestor = dados.get("gestor", "").strip()
            colaboradores_cpf = dados.get("colaboradores", [])

            # Validar gestor (se fornecido)
            gestor_json = None
            if cpf_gestor:
                cpf_limpo = cpf_gestor.replace(".", "").replace("-", "")
                if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                    return False, "CPF do gestor inválido"

                gestor = self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(
                    cpf_gestor
                )
                if not gestor:
                    return False, "Gestor não encontrado"

                gestor_json = {
                    "cpf": gestor.cpf,
                    "nome": gestor.nome,
                    "email": gestor.email,
                    "cargo": gestor.cargo,
                }

            # Validar colaboradores
            cpfs_validados = []
            for cpf in colaboradores_cpf:
                if cpf.strip():
                    cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
                    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                        return False, f"CPF inválido: {cpf}"

                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                        cpf.strip()
                    )
                    if not colaborador:
                        return False, f"Colaborador não encontrado: {cpf}"

                    if cpf.strip() in cpfs_validados:
                        return False, f"CPF duplicado: {cpf}"

                    cpfs_validados.append(cpf.strip())

            # Criar lista de colaboradores JSON
            colaborador_json = []
            for cpf in cpfs_validados:
                colaborador = self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(cpf)
                colaborador_json.append({
                    "cpf": colaborador.cpf,
                    "nome": colaborador.nome,
                    "email": colaborador.email,
                    "cargo": colaborador.cargo,
                })

            # Atualizar equipe
            for i, equipe in enumerate(equipes):
                if equipe.get("nome") == nome_atual:
                    equipes[i] = {
                        "nome": nome,
                        "gestor": gestor_json,  # Pode ser None se não houver gestor
                        "colaboradores": colaborador_json,
                    }
                    sucesso = self.__equipe.salvar_equipes(equipes)
                    
                    if sucesso:
                        return True, "Equipe atualizada com sucesso!"
                    else:
                        return False, "Erro ao salvar equipe no banco de dados"

            return False, "Equipe não encontrada"

        except Exception as e:
            print(f"Erro ao atualizar equipe: {e}")
            return False, f"Erro interno: {str(e)}"

    def excluir_equipe(self, nome: str) -> tuple[bool, str]:
        try:
            equipes = self.__equipe.carregar_equipes()
            equipes_filtradas = [
                equipe for equipe in equipes if equipe.get("nome") != nome
            ]

            if len(equipes) == len(equipes_filtradas):
                return False, "Equipe não encontrada"

            sucesso = self.__equipe.salvar_equipes(equipes_filtradas)
            
            if sucesso:
                return True, "Equipe excluída com sucesso!"
            else:
                return False, "Erro ao excluir equipe do banco de dados"

        except Exception as e:
            print(f"Erro ao excluir equipe: {e}")
            return False, f"Erro interno: {str(e)}"

    # Métodos adicionais
    def obter_colaboradores_sem_equipe(self) -> list[dict]:
        try:
            # Buscar todos os colaboradores
            todos_colaboradores = self.__controlador_sistema.controlador_colaborador.buscar_colaboradores()

            # Buscar CPFs já em equipes
            equipes = self.__equipe.carregar_equipes()
            colaboradores_em_equipes = set()

            for equipe in equipes:
                for colaborador in equipe.get("colaboradores", []):
                    colaboradores_em_equipes.add(colaborador["cpf"])

            # Filtrar colaboradores sem equipe
            colaboradores_sem_equipe = []
            for colaborador in todos_colaboradores:
                if (
                    hasattr(colaborador, "cpf")
                    and colaborador.cpf not in colaboradores_em_equipes
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
                # Verificar se a equipe tem gestor e se o gestor tem CPF
                if "gestor" in equipe and equipe["gestor"] and isinstance(equipe["gestor"], dict):
                    cpf_gestor = equipe["gestor"].get("cpf")
                    if cpf_gestor:
                        print(f"Adicionando CPF do gestor {cpf_gestor} à lista de gestores em equipes")
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

    def obter_colaboradores_disponiveis_para_equipe(self, nome_equipe: str) -> list[dict]:
        """Retorna colaboradores que podem ser adicionados à equipe (sem equipe + já na equipe)"""
        try:
            # Usar o método existente para buscar colaboradores sem equipe
            colaboradores_sem_equipe = self.obter_colaboradores_sem_equipe()
            
            # Buscar colaboradores já na equipe atual
            equipes = self.__equipe.carregar_equipes()
            colaboradores_da_equipe = []
            
            for equipe in equipes:
                if equipe.get("nome") == nome_equipe:
                    for colab in equipe.get("colaboradores", []):
                        colaboradores_da_equipe.append({
                            "cpf": colab.get("cpf"),
                            "nome": colab.get("nome")
                        })
                    break
            
            # Combinar listas (sem duplicatas)
            todos_disponiveis = colaboradores_sem_equipe + colaboradores_da_equipe
            return todos_disponiveis

        except Exception as e:
            print(f"Erro ao obter colaboradores disponíveis para equipe: {e}")
            return []

    def obter_gestores_disponiveis_para_equipe(self, nome_equipe: str) -> list[dict]:
        """Retorna gestores que podem ser adicionados à equipe (sem equipe + gestor atual)"""
        try:
            # Usar o método existente para buscar gestores sem equipe
            gestores_sem_equipe = self.obter_gestores_sem_equipe()
            
            # Buscar gestor atual da equipe
            equipes = self.__equipe.carregar_equipes()
            gestor_atual = []
            
            for equipe in equipes:
                if equipe.get("nome") == nome_equipe:
                    if equipe.get("gestor") and isinstance(equipe["gestor"], dict):
                        gestor_atual.append({
                            "cpf": equipe["gestor"].get("cpf"),
                            "nome": equipe["gestor"].get("nome")
                        })
                    break
            
            # Combinar listas (sem duplicatas)
            todos_disponiveis = gestores_sem_equipe + gestor_atual
            return todos_disponiveis

        except Exception as e:
            print(f"Erro ao obter gestores disponíveis para equipe: {e}")
            return []
