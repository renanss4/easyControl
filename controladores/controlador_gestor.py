from modelos.modelo_gestor import Gestor
from datetime import date


class ControladorGestor:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__gestor = Gestor()
        self.__tela_gestor = None

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def gestor(self):
        return self.__gestor

    @property
    def tela_gestor(self):
        return self.__tela_gestor

    def abrir_tela_gestor(self):
        from telas.tela_gestor import TelaGestor

        self.__tela_gestor = TelaGestor(self)
        return self.__tela_gestor

    def abrir_tela_gestor_logado(self):
        """Abre a tela do gestor logado (para gestores que fizeram login)"""
        from telas.tela_gestor import TelaGestorLogado

        self.__tela_gestor = TelaGestorLogado(self)
        return self.__tela_gestor

    def voltar_tela_funcionario_rh(self):
        """Volta para a tela do funcionário RH"""
        self.__tela_gestor = None
        return self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_para_tela_sistema(self):
        """Retorna para a tela principal do sistema"""
        self.__tela_gestor = None
        self.__controlador_sistema.abrir_tela_sistema()

    def converter_dict_para_gestor(self, gestor_dict: dict) -> Gestor | bool:
        try:
            return Gestor(
                cpf=gestor_dict["cpf"],
                nome=gestor_dict["nome"],
                cargo=gestor_dict["cargo"],
                data_admissao=date.fromisoformat(gestor_dict["data_admissao"]),
                email=gestor_dict["email"],
                senha=gestor_dict["senha"],
            )
        except (KeyError, ValueError):
            return False

    def autenticar(self, email: str, senha: str) -> Gestor | None:
        for gestor_dict in self.__gestor.carregar_gestores():
            if gestor_dict["email"] == email and gestor_dict["senha"] == senha:
                return self.converter_dict_para_gestor(gestor_dict)
        return None

    def cadastrar_gestor(self, dados: dict) -> bool:
        """
        Cadastra um novo gestor
        """
        try:
            campos_obrigatorios = ["cpf", "nome", "cargo", "email", "senha"]

            # Verificar se todos os campos obrigatórios estão presentes
            for campo in campos_obrigatorios:
                if campo not in dados or not dados[campo]:
                    return False

            # Validar formato do CPF (11 dígitos)
            cpf = dados["cpf"].replace(".", "").replace("-", "")
            if len(cpf) != 11 or not cpf.isdigit():
                return False

            # Validar email básico
            email = dados["email"]
            if "@" not in email or "." not in email:
                return False

            # Carregar gestores existentes
            gestores = self.__gestor.carregar_gestores()

            # Verificar se CPF já existe
            for gest in gestores:
                if gest.get("cpf") == dados["cpf"]:
                    return False  # CPF já existe

            novo_gestor = {
                "cpf": dados["cpf"],
                "nome": dados["nome"],
                "cargo": dados["cargo"],
                "data_admissao": date.today().isoformat(),
                "email": dados["email"],
                "senha": dados["senha"],
            }

            gestores.append(novo_gestor)
            return self.__gestor.salvar_gestores(gestores)

        except Exception as e:
            print(f"Erro ao cadastrar gestor: {e}")
            return False

    def buscar_por_cpf(self, cpf: str) -> Gestor | None:
        """Busca gestor por CPF"""
        try:
            gestores = self.__gestor.carregar_gestores()
            for gest_dict in gestores:
                if gest_dict.get("cpf") == cpf:
                    return self.converter_dict_para_gestor(gest_dict)
            return None
        except Exception as e:
            print(f"Erro ao buscar gestor: {e}")
            return None

    def atualizar_gestor(self, cpf: str, dados: dict) -> bool:
        """Atualiza dados de um gestor"""
        try:
            campos_obrigatorios = ["cpf", "nome", "cargo", "email"]

            # Verificar se todos os campos obrigatórios estão presentes
            for campo in campos_obrigatorios:
                if campo not in dados or not dados[campo]:
                    return False

            # Validar email básico
            email = dados["email"]
            if "@" not in email or "." not in email:
                return False

            gestores = self.__gestor.carregar_gestores()

            for i, gest in enumerate(gestores):
                if gest.get("cpf") == cpf:
                    gestores[i].update(dados)
                    return self.__gestor.salvar_gestores(gestores)

            return False  # CPF não encontrado

        except Exception as e:
            print(f"Erro ao atualizar gestor: {e}")
            return False

    def excluir_gestor(self, cpf: str) -> bool:
        """Exclui um gestor"""
        try:
            gestores = self.__gestor.carregar_gestores()
            gestores_filtrados = [gest for gest in gestores if gest.get("cpf") != cpf]

            if len(gestores) == len(gestores_filtrados):
                return False  # CPF não encontrado

            return self.__gestor.salvar_gestores(gestores_filtrados)

        except Exception as e:
            print(f"Erro ao excluir gestor: {e}")
            return False

    def buscar_gestores(self):
        pass

    def abrir_tela_solicitacao(self):
        """Abre a tela de solicitação através do sistema"""
        return (
            self.__controlador_sistema.controlador_solicitacao.abrir_tela_solicitacao()
        )

    def abrir_tela_equipe(self):
        """Abre a tela de equipe através do sistema"""
        return self.__controlador_sistema.controlador_equipe.abrir_tela_equipe()
