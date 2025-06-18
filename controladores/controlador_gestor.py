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
        if self.__tela_gestor is None:
            from telas.tela_gestor import TelaGestor

            self.__tela_gestor = TelaGestor(self)
        return self.__tela_gestor

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

    def cadastrar_gestor(self):
        pass

    def atualizar_gestor(self):
        pass

    def excluir_gestor(self):
        pass

    def buscar_gestor_por_cpf(self):
        pass

    def buscar_gestores(self):
        pass

    def abrir_tela_solicitacao(self):
        # TODO: Implementar lógica para abrir a tela de solicitação
        pass

    def abrir_tela_equipe(self):
        # TODO: Implementar lógica para abrir a tela de equipe
        pass
