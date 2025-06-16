from ..modelos.modelo_colaborador import Colaborador
from ..modelos.modelo_solicitacao import Solicitacao
from datetime import date


class ControladorColaborador:
    @staticmethod  # esse método deve ficar no controller
    def converter_dict_para_colaborador(colaborador_dict: dict) -> Colaborador | bool:
        try:
            return Colaborador(
                cpf=colaborador_dict["cpf"],
                nome=colaborador_dict["nome"],
                cargo=colaborador_dict["cargo"],
                data_admissao=date.fromisoformat(colaborador_dict["data_admissao"]),
                email=colaborador_dict["email"],
                solicitacoes=[
                    Solicitacao(**sol)
                    for sol in colaborador_dict.get("solicitacoes", [])
                ],
            )
        except (KeyError, ValueError):
            return False

    def __init__(self, modelo_colaborador):
        self.modelo_colaborador = modelo_colaborador
