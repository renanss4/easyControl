from modelos.modelo_funcionario_rh import FuncionarioRH
from datetime import date


class ControladorFuncionarioRH:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__funcionario_rh = FuncionarioRH()
        self.__tela_funcionario_rh = None

    def abrir_tela_funcionario_rh(self):
        from telas.tela_funcionario_rh import TelaRH

        self.__tela_funcionario_rh = TelaRH(self)
        return self.__tela_funcionario_rh

    def voltar_para_tela_sistema(self):
        """Retorna para a tela principal do sistema"""
        self.__tela_funcionario_rh = None
        self.__controlador_sistema.abrir_tela_sistema()

    def converter_dict_para_funcionario_rh(
        self, funcionario_rh_dict: dict
    ) -> FuncionarioRH | bool:
        try:
            return FuncionarioRH(
                cpf=funcionario_rh_dict["cpf"],
                nome=funcionario_rh_dict["nome"],
                cargo=funcionario_rh_dict["cargo"],
                data_admissao=date.fromisoformat(funcionario_rh_dict["data_admissao"]),
                email=funcionario_rh_dict["email"],
                senha=funcionario_rh_dict["senha"],
            )
        except (KeyError, ValueError):
            return False

    def autenticar(self, email: str, senha: str) -> FuncionarioRH | None:
        for funcionario_rh_dict in self.__funcionario_rh.carregar_funcionarios_rh():
            if (
                funcionario_rh_dict["email"] == email
                and funcionario_rh_dict["senha"] == senha
            ):
                return self.converter_dict_para_funcionario_rh(funcionario_rh_dict)
        return None

    def abrir_tela_colaborador(self):
        """Abre a tela de cadastro de colaborador através do sistema"""
        return (
            self.__controlador_sistema.controlador_colaborador.abrir_tela_colaborador()
        )

    def abrir_tela_gestor(self):
        """Abre a tela de cadastro de gestor através do sistema"""
        return self.__controlador_sistema.controlador_gestor.abrir_tela_gestor()

    def abrir_tela_solicitacao(self):
        """Abre a tela de solicitação através do sistema"""
        return (
            self.__controlador_sistema.controlador_solicitacao.abrir_tela_solicitacao()
        )

    def abrir_tela_equipe(self):
        """Abre a tela de equipe através do sistema"""
        return self.__controlador_sistema.controlador_equipe.abrir_tela_equipe()

    def cadastrar_funcionario_rh(
        self, nome: str, cpf: str, email: str, senha: str, cargo: str
    ) -> bool:
        """Cadastra um novo funcionário RH"""
        try:
            # Validar dados
            if not all([nome, cpf, email, senha, cargo]):
                return False

            # Validar formato do CPF (11 dígitos)
            cpf_limpo = cpf.replace(".", "").replace("-", "")
            if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
                return False

            # Validar email básico
            if "@" not in email or "." not in email:
                return False

            # Validar senha
            if len(senha) < 6:
                return False

            # Carregar funcionários existentes
            funcionarios = self.__funcionario_rh.carregar_funcionarios_rh()

            # Verificar se CPF já existe
            for func in funcionarios:
                if func.get("cpf") == cpf:
                    return False  # CPF já existe

            # Criar novo funcionário
            novo_funcionario = {
                "cpf": cpf,
                "nome": nome,
                "cargo": cargo,
                "data_admissao": date.today().isoformat(),
                "email": email,
                "senha": senha,
            }

            funcionarios.append(novo_funcionario)
            return self.__funcionario_rh.salvar_funcionarios_rh(funcionarios)

        except Exception as e:
            print(f"Erro ao cadastrar funcionário RH: {e}")
            return False

    def buscar_funcionario_rh_por_cpf(self, cpf: str) -> FuncionarioRH | None:
        """Busca funcionário RH por CPF"""
        try:
            funcionarios = self.__funcionario_rh.carregar_funcionarios_rh()
            for func_dict in funcionarios:
                if func_dict.get("cpf") == cpf:
                    return self.converter_dict_para_funcionario_rh(func_dict)
            return None
        except Exception as e:
            print(f"Erro ao buscar funcionário RH: {e}")
            return None

    def atualizar_funcionario_rh(self, cpf: str, dados: dict) -> bool:
        """Atualiza dados de um funcionário RH"""
        try:
            # Validar dados obrigatórios
            if (
                not dados.get("nome")
                or not dados.get("email")
                or not dados.get("cargo")
            ):
                return False

            # Validar email básico
            email = dados["email"]
            if "@" not in email or "." not in email:
                return False

            # Validar senha se foi fornecida
            if dados.get("senha") and len(dados["senha"]) < 6:
                return False

            funcionarios = self.__funcionario_rh.carregar_funcionarios_rh()

            for i, func in enumerate(funcionarios):
                if func.get("cpf") == cpf:
                    # Atualizar apenas os campos fornecidos
                    funcionarios[i]["nome"] = dados["nome"]
                    funcionarios[i]["email"] = dados["email"]
                    funcionarios[i]["cargo"] = dados["cargo"]

                    # Só atualizar senha se foi fornecida
                    if dados.get("senha"):
                        funcionarios[i]["senha"] = dados["senha"]

                    return self.__funcionario_rh.salvar_funcionarios_rh(funcionarios)

            return False  # CPF não encontrado

        except Exception as e:
            print(f"Erro ao atualizar funcionário RH: {e}")
            return False

    def excluir_funcionario_rh(self, cpf: str) -> bool:
        """Exclui um funcionário RH"""
        try:
            funcionarios = self.__funcionario_rh.carregar_funcionarios_rh()
            funcionarios_filtrados = [
                func for func in funcionarios if func.get("cpf") != cpf
            ]

            if len(funcionarios) == len(funcionarios_filtrados):
                return False  # CPF não encontrado

            return self.__funcionario_rh.salvar_funcionarios_rh(funcionarios_filtrados)

        except Exception as e:
            print(f"Erro ao excluir funcionário RH: {e}")
            return False
