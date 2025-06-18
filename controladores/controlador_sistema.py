from controladores.controlador_colaborador import ControladorColaborador
from controladores.controlador_equipe import ControladorEquipe
from controladores.controlador_funcionario_rh import ControladorFuncionarioRH
from controladores.controlador_gestor import ControladorGestor
from controladores.controlador_solicitacao import ControladorSolicitacao
from telas.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema(self)
        self.controlador_colaborador = ControladorColaborador(self)
        self.controlador_equipe = ControladorEquipe(self)
        self.controlador_funcionario_rh = ControladorFuncionarioRH(self)
        self.controlador_gestor = ControladorGestor(self)
        self.controlador_solicitacao = ControladorSolicitacao(self)

    def abre_tela_sistema(self):
        self.tela_sistema.mainloop()

    def fecha_tela_sistema(self):
        if self.tela_sistema is not None:
            self.tela_sistema.destroy()
            self.tela_sistema = None

    def autenticar_usuario(self, email: str, senha: str) -> object | bool:
        """
        Autentica um usuário (RH ou Gestor) através dos controladores específicos
        """
        # Tenta autenticar como RH
        usuario_rh = self.controlador_funcionario_rh.autenticar(email, senha)
        if usuario_rh:
            self.usuario_logado = usuario_rh
            return usuario_rh

        # Tenta autenticar como Gestor
        usuario_gestor = self.controlador_gestor.autenticar(email, senha)
        if usuario_gestor:
            self.usuario_logado = usuario_gestor
            return usuario_gestor

        return False
