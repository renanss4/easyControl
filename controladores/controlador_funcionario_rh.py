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

    def cadastrar_funcionario_rh():
        pass

    def atualizar_funcionario_rh():
        pass

    def excluir_funcionario_rh():
        pass

    def buscar_funcionario_rh_por_cpf():
        pass

    def buscar_funcionarios_rh():
        pass
