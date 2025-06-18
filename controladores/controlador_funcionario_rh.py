from modelos.modelo_funcionario_rh import FuncionarioRH
from datetime import date


class ControladorFuncionarioRH:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.funcionario_rh = FuncionarioRH()
        self.tela_funcionario_rh = None

    def abrir_tela_funcionario_rh(self):
        if self.tela_funcionario_rh is None:
            from telas.tela_funcionario_rh import TelaRH

            self.tela_funcionario_rh = TelaRH(self)
        return self.tela_funcionario_rh

    def fechar_tela_funcionario_rh(self):
        if self.tela_funcionario_rh is not None:
            self.tela_funcionario_rh.destroy()
            self.tela_funcionario_rh = None

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
        for funcionario_rh_dict in self.funcionario_rh.carregar_funcionarios_rh():
            if (
                funcionario_rh_dict["email"] == email
                and funcionario_rh_dict["senha"] == senha
            ):
                return self.converter_dict_para_funcionario_rh(funcionario_rh_dict)
        return None

    # Métodos para abrir telas através do controlador do sistema
    def abrir_tela_cadastro_colaborador(self):
        """Abre a tela de cadastro de colaborador através do sistema"""
        return self.controlador_sistema.controlador_colaborador.abrir_tela_colaborador()

    def abrir_tela_cadastro_gestor(self):
        """Abre a tela de cadastro de gestor através do sistema"""
        return self.controlador_sistema.controlador_gestor.abrir_tela_gestor()

    def abrir_tela_cadastro_funcionario_rh(self):
        """Abre a tela de cadastro de funcionário RH através do sistema"""
        # Aqui pode ser uma tela específica ou reutilizar a mesma lógica
        return self.controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def abrir_tela_solicitacao(self):
        """Abre a tela de solicitação através do sistema"""
        return self.controlador_sistema.controlador_solicitacao.abrir_tela_solicitacao()

    def abrir_tela_equipe(self):
        """Abre a tela de equipe através do sistema"""
        return self.controlador_sistema.controlador_equipe.abrir_tela_equipe()

    def consultar_lista_colaboradores(self):
        """Abre tela de colaborador em modo consulta"""
        return self.controlador_sistema.controlador_colaborador.abrir_tela_colaborador()

    def gerar_relatorio_ferias(self):
        """Gera relatório de férias - implementar lógica específica"""
        # TODO: Implementar lógica de relatório
        pass
