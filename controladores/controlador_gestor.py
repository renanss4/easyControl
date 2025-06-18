from modelos.modelo_gestor import Gestor
from datetime import date


class ControladorGestor:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.gestor = Gestor()
        self.tela_gestor = None

    def abrir_tela_gestor(self):
        if self.tela_gestor is None:
            from telas.tela_gestor import TelaGestor

            self.tela_gestor = TelaGestor(self)
        return self.tela_gestor

    def fechar_tela_gestor(self):
        if self.tela_gestor is not None:
            self.tela_gestor.destroy()
            self.tela_gestor = None

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
        for gestor_dict in self.gestor.carregar_gestores():
            if gestor_dict["email"] == email and gestor_dict["senha"] == senha:
                return self.converter_dict_para_gestor(gestor_dict)
        return None

    def cadastrar_gestor():
        pass

    def atualizar_gestor():
        pass

    def excluir_gestor():
        pass

    def buscar_gestor_por_cpf():
        pass

    def buscar_gestores():
        pass

    def aprovar_solicitacao():
        pass

    def rejeitar_solicitacao():
        pass

    def consultar_colaboradores_equipe():
        pass
