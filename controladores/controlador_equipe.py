from modelos.modelo_equipe import Equipe


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
        if self.__tela_equipe is None:
            from telas.tela_equipe import TelaEquipe

            self.__tela_equipe = TelaEquipe(self)
        return self.__tela_equipe

    def converter_dict_para_equipe(self, equipe_dict: dict) -> Equipe | bool:
        try:
            return Equipe(
                nome=equipe_dict["nome"],
                gestor=self.__controlador_sistema.controlador_gestor.converter_dict_para_gestor(
                    equipe_dict["gestor"]
                ),
                colaboradores=[
                    self.__controlador_sistema.controlador_colaborador.converter_dict_para_colaborador(
                        col
                    )
                    for col in equipe_dict.get("colaboradores", [])
                ],
            )
        except (KeyError, ValueError):
            return False

    def cadastrar_equipe(self):
        pass

    def atualizar_equipe(self):
        pass

    def excluir_equipe(self):
        pass

    def buscar_equipe_por_nome(self):
        pass

    def buscar_equipes(self):
        pass

    def adicionar_colaborador(self):
        pass

    def remover_colaborador(self):
        pass

    def adicionar_gestor(self):
        pass

    def remover_gestor(self):
        pass

    def listar_colaboradores_equipe(self):
        pass
