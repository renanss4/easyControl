from controladores.controlador_colaborador import ControladorColaborador
from controladores.controlador_equipe import ControladorEquipe
from controladores.controlador_funcionario_rh import ControladorFuncionarioRH
from controladores.controlador_gestor import ControladorGestor
from controladores.controlador_solicitacao import ControladorSolicitacao
from telas.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = None
        self.__controlador_colaborador = ControladorColaborador(self)
        self.__controlador_equipe = ControladorEquipe(self)
        self.__controlador_funcionario_rh = ControladorFuncionarioRH(self)
        self.__controlador_gestor = ControladorGestor(self)
        self.__controlador_solicitacao = ControladorSolicitacao(self)
        self.__usuario_logado = None

    @property
    def tela_sistema(self):
        return self.__tela_sistema

    @property
    def controlador_colaborador(self):
        return self.__controlador_colaborador

    @property
    def controlador_equipe(self):
        return self.__controlador_equipe

    @property
    def controlador_funcionario_rh(self):
        return self.__controlador_funcionario_rh

    @property
    def controlador_gestor(self):
        return self.__controlador_gestor

    @property
    def controlador_solicitacao(self):
        return self.__controlador_solicitacao

    @property
    def usuario_logado(self):
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, usuario):
        self.__usuario_logado = usuario

    def abrir_tela_sistema(self):
        self.__tela_sistema = TelaSistema(self)
        self.__tela_sistema.mainloop()

    def autenticar_usuario(self, email: str, senha: str) -> object | bool:
        # Tenta autenticar como RH
        usuario_rh = self.__controlador_funcionario_rh.autenticar(email, senha)
        if usuario_rh:
            self.__usuario_logado = usuario_rh
            return usuario_rh

        # Tenta autenticar como Gestor
        usuario_gestor = self.__controlador_gestor.autenticar(email, senha)
        if usuario_gestor:
            self.__usuario_logado = usuario_gestor
            return usuario_gestor

        return False
