from modelos.modelo_equipe import Equipe


class ControladorEquipe:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.equipe = Equipe()
        self.tela_equipe = None

    def abrir_tela_equipe(self):
        if self.tela_equipe is None:
            from telas.tela_equipe import TelaEquipe

            self.tela_equipe = TelaEquipe(self)
        return self.tela_equipe

    def fechar_tela_equipe(self):
        if self.tela_equipe is not None:
            self.tela_equipe.destroy()
            self.tela_equipe = None

    def converter_dict_para_equipe(self, equipe_dict: dict) -> Equipe | bool:
        try:
            return Equipe(
                nome=equipe_dict["nome"],
                gestor=self.controlador_sistema.controlador_gestor.converter_dict_para_gestor(
                    equipe_dict["gestor"]
                ),
                colaboradores=[
                    self.controlador_sistema.controlador_colaborador.converter_dict_para_colaborador(
                        col
                    )
                    for col in equipe_dict.get("colaboradores", [])
                ],
            )
        except (KeyError, ValueError):
            return False

    def cadastrar_equipe():
        pass

    def atualizar_equipe():
        pass

    def excluir_equipe():
        pass

    def buscar_equipe_por_nome():
        pass

    def buscar_equipes():
        pass

    def adicionar_colaborador():
        pass

    def remover_colaborador():
        pass

    def adicionar_gestor():
        pass

    def remover_gestor():
        pass

    def listar_colaboradores_equipe():
        pass
