from modelos.modelo_solicitacao import Solicitacao
from datetime import date


class ControladorSolicitacao:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__solicitacao = Solicitacao()
        self.__tela_solicitacao = None

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema

    @property
    def solicitacao(self):
        return self.__solicitacao

    @property
    def tela_solicitacao(self):
        return self.__tela_solicitacao

    def abrir_tela_solicitacao(self):
        from telas.tela_solicitacao import TelaSolicitacao

        self.__tela_solicitacao = TelaSolicitacao(self)
        return self.__tela_solicitacao

    def voltar_tela_funcionario_rh(self):
        """Volta para a tela do funcionário RH"""
        self.__tela_solicitacao = None
        return self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_tela_gestor(self):
        """Volta para a tela do gestor"""
        self.__tela_solicitacao = None
        return self.__controlador_sistema.controlador_gestor.abrir_tela_gestor()

    def converter_dict_para_solicitacao(
        self, solicitacao_dict: dict
    ) -> Solicitacao | bool:
        try:
            # Primeiro, determina e converte a pessoa (pode ser Colaborador, FuncionarioRH ou Gestor)
            pessoa_obj = None
            if "pessoa" in solicitacao_dict:
                pessoa_data = solicitacao_dict["pessoa"]

                # Tenta converter usando os diferentes controladores
                # Primeiro tenta colaborador
                pessoa_obj = self.__controlador_sistema.controlador_colaborador.converter_dict_para_colaborador(
                    pessoa_data
                )

                # Se não conseguiu, tenta funcionário RH
                if not pessoa_obj and hasattr(
                    self.__controlador_sistema, "controlador_funcionario_rh"
                ):
                    pessoa_obj = self.__controlador_sistema.controlador_funcionario_rh.converter_dict_para_funcionario_rh(
                        pessoa_data
                    )

                # Se não conseguiu, tenta gestor
                if not pessoa_obj and hasattr(
                    self.__controlador_sistema, "controlador_gestor"
                ):
                    pessoa_obj = self.__controlador_sistema.controlador_gestor.converter_dict_para_gestor(
                        pessoa_data
                    )

            # Se ainda não encontrou a pessoa, retorna False
            if not pessoa_obj:
                return False

            # Converte os períodos se existirem
            periodos = []
            if "periodos" in solicitacao_dict:
                from modelos.tipos_enum import PeriodoFerias

                for periodo_dict in solicitacao_dict["periodos"]:
                    periodo = PeriodoFerias(
                        data_inicio=date.fromisoformat(periodo_dict["data_inicio"]),
                        data_fim=date.fromisoformat(periodo_dict["data_fim"]),
                    )
                    periodos.append(periodo)

            # Converte o status se existir
            if "status" in solicitacao_dict:
                from modelos.tipos_enum import StatusSolicitacao

                status = StatusSolicitacao(solicitacao_dict["status"])

            return Solicitacao(
                protocolo=solicitacao_dict["protocolo"],
                pessoa=pessoa_obj,
                data_solicitacao=date.fromisoformat(
                    solicitacao_dict["data_solicitacao"]
                ),
                periodos=periodos,
                parcelamento=solicitacao_dict.get("parcelamento", False),
                status=status,
            )
        except (KeyError, ValueError, TypeError):
            return False

    def aprovar_solicitacao(self):
        pass

    def rejeitar_solicitacao(self):
        pass

    def cancelar_solicitacao(self):
        pass

    def cadastrar_solicitacao(self):
        pass

    def cadastrar_solicitacao_parcelada(self):
        pass

    def buscar_pessoa(self):
        pass

    def buscar_solicitacao_por_protocolo(self):
        pass

    def buscar_solicitacoes(self):
        pass
