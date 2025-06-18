from modelos.modelo_colaborador import Colaborador
from datetime import date


class ControladorColaborador:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.colaborador = Colaborador()
        self.tela_colaborador = None

    def abrir_tela_colaborador(self):
        if self.tela_colaborador is None:
            from telas.tela_colaborador import TelaColaborador

            self.tela_colaborador = TelaColaborador(self)
        return self.tela_colaborador

    def fechar_tela_colaborador(self):
        if self.tela_colaborador is not None:
            self.tela_colaborador.destroy()
            self.tela_colaborador = None

    def converter_dict_para_colaborador(self, colaborador_dict: dict) -> Colaborador | bool:
        try:
            return Colaborador(
                cpf=colaborador_dict["cpf"],
                nome=colaborador_dict["nome"],
                cargo=colaborador_dict["cargo"],
                data_admissao=date.fromisoformat(colaborador_dict["data_admissao"]),
                email=colaborador_dict["email"],
            )
        except (KeyError, ValueError):
            return False

    def cadastrar_colaborador():
        pass

    def atualizar_colaborador():
        pass

    def excluir_colaborador():
        pass

    def buscar_colaborador_por_cpf():
        pass

    def buscar_colaboradores():
        pass
