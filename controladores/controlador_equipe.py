from modelos.modelo_equipe import Equipe
from typing import List, Tuple


class ControladorEquipe:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__equipe = Equipe()
        self.__tela_equipe = None

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def equipe(self):
        return self.__equipe

    @property
    def tela_equipe(self):
        return self.__tela_equipe

    def abrir_tela_equipe(self):
        """Abre a tela de equipe"""
        from telas.tela_equipe import TelaEquipe

        self.__tela_equipe = TelaEquipe(self)
        return self.__tela_equipe

    def voltar_tela_funcionario_rh(self):
        """Volta para a tela do funcionário RH"""
        self.__tela_equipe = None
        return self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    # ==================== VALIDAÇÕES ====================

    def validar_nome_equipe(self, nome: str) -> Tuple[bool, str]:
        """Valida nome da equipe"""
        if not nome or not nome.strip():
            return False, "Nome da equipe é obrigatório"

        if len(nome.strip()) < 3:
            return False, "Nome da equipe deve ter pelo menos 3 caracteres"

        return True, ""

    def validar_cpf_gestor(self, cpf: str) -> Tuple[bool, str]:
        """Valida CPF do gestor"""
        if not cpf or not cpf.strip():
            return True, ""  # Gestor é opcional

        # Validar formato
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
            return False, "CPF do gestor deve conter 11 dígitos numéricos"

        # Verificar se gestor existe
        gestor = self.__controlador_sistema.controlador_gestor.buscar_por_cpf(cpf)
        if not gestor:
            return False, "Gestor não encontrado no sistema"

        return True, ""

    def validar_cpf_colaborador(self, cpf: str) -> Tuple[bool, str]:
        """Valida CPF de colaborador"""
        if not cpf or not cpf.strip():
            return False, "CPF do colaborador é obrigatório"

        # Validar formato
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
            return False, "CPF deve conter 11 dígitos numéricos"

        # Verificar se colaborador existe
        colaborador = self.__controlador_sistema.controlador_colaborador.buscar_por_cpf(
            cpf
        )
        if not colaborador:
            return False, "Colaborador não encontrado no sistema"

        return True, ""

    def validar_equipe_unica(
        self, nome: str, equipe_atual: str = None
    ) -> Tuple[bool, str]:
        """Valida se nome da equipe é único"""
        equipes = self.buscar_equipes()

        for equipe in equipes:
            if equipe.get("nome", "").lower() == nome.lower():
                # Se estamos editando, ignora a equipe atual
                if equipe_atual and equipe.get("nome") == equipe_atual:
                    continue
                return False, "Já existe uma equipe com este nome"

        return True, ""

    def validar_dados_equipe(
        self, dados: dict, equipe_atual: str = None
    ) -> Tuple[bool, str]:
        """Valida todos os dados da equipe"""
        nome = dados.get("nome", "").strip()
        cpf_gestor = dados.get("cpf_gestor", "").strip()
        colaboradores_cpf = dados.get("colaboradores_cpf", [])

        # Validar nome
        valido, msg = self.validar_nome_equipe(nome)
        if not valido:
            return False, msg

        # Validar nome único
        valido, msg = self.validar_equipe_unica(nome, equipe_atual)
        if not valido:
            return False, msg

        # Validar gestor (opcional)
        if cpf_gestor:
            valido, msg = self.validar_cpf_gestor(cpf_gestor)
            if not valido:
                return False, msg

        # Validar colaboradores
        cpfs_validados = []
        for cpf in colaboradores_cpf:
            if cpf.strip():  # Ignorar CPFs vazios
                valido, msg = self.validar_cpf_colaborador(cpf.strip())
                if not valido:
                    return False, f"{msg} ({cpf})"

                # Verificar duplicatas
                if cpf.strip() in cpfs_validados:
                    return False, f"CPF duplicado: {cpf}"

                cpfs_validados.append(cpf.strip())

        return True, ""

    # ==================== OPERAÇÕES PRINCIPAIS ====================

    def cadastrar_equipe(self, dados: dict) -> Tuple[bool, str]:
        """Cadastra uma nova equipe"""
        try:
            # Validar dados
            valido, msg = self.validar_dados_equipe(dados)
            if not valido:
                return False, msg

            # Criar nova equipe
            nova_equipe = {
                "nome": dados.get("nome", "").strip(),
                "cpf_gestor": dados.get("cpf_gestor", "").strip(),
                "colaboradores_cpf": [
                    cpf.strip()
                    for cpf in dados.get("colaboradores_cpf", [])
                    if cpf.strip()
                ],
            }

            # Carregar equipes existentes
            equipes = self.__equipe.carregar_equipes()
            equipes.append(nova_equipe)

            # Salvar
            if self.__equipe.salvar_equipes(equipes):
                return True, "Equipe cadastrada com sucesso!"
            else:
                return False, "Erro ao salvar equipe"

        except Exception as e:
            return False, f"Erro interno: {str(e)}"

    def buscar_equipes(self) -> List[dict]:
        """Busca todas as equipes enriquecidas com nomes"""
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
                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_por_cpf(
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
        """Busca equipe por nome"""
        try:
            equipes = self.buscar_equipes()
            for equipe in equipes:
                if equipe.get("nome", "").lower() == nome.lower():
                    return equipe
            return None
        except Exception as e:
            print(f"Erro ao buscar equipe por nome: {e}")
            return None

    def excluir_equipe(self, nome: str) -> Tuple[bool, str]:
        """Exclui uma equipe"""
        try:
            equipes = self.__equipe.carregar_equipes()

            # Encontrar e remover equipe
            equipe_encontrada = False
            for i, equipe in enumerate(equipes):
                if equipe.get("nome", "") == nome:
                    equipes.pop(i)
                    equipe_encontrada = True
                    break

            if not equipe_encontrada:
                return False, "Equipe não encontrada"

            # Salvar
            if self.__equipe.salvar_equipes(equipes):
                return True, "Equipe excluída com sucesso!"
            else:
                return False, "Erro ao salvar exclusão"

        except Exception as e:
            return False, f"Erro ao excluir equipe: {str(e)}"

    def obter_colaboradores_sem_equipe(self) -> List[dict]:
        """Retorna colaboradores que não estão em nenhuma equipe"""
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

    def obter_gestores_sem_equipe(self) -> List[dict]:
        """Retorna gestores que não estão em nenhuma equipe"""
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
