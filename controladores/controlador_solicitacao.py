from modelos.modelo_solicitacao import Solicitacao
from datetime import date
import random
import string


class ControladorSolicitacao:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__solicitacao = Solicitacao()
        self.__tela_solicitacao = None

    def abrir_tela_solicitacao(self):
        usuario_logado = self.__controlador_sistema.usuario_logado

        if hasattr(usuario_logado, "__class__") and "FuncionarioRH" in str(
            usuario_logado.__class__
        ):
            from telas.tela_solicitacao import TelaCadastrarSolicitacao

            self.__tela_solicitacao = TelaCadastrarSolicitacao(self)
        else:
            from telas.tela_solicitacao import TelaAnalisarSolicitacao

            self.__tela_solicitacao = TelaAnalisarSolicitacao(self)

        return self.__tela_solicitacao

    def voltar_tela_funcionario_rh(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_tela_gestor(self):
        self.__tela_solicitacao = None
        self.__controlador_sistema.controlador_gestor.abrir_tela_gestor_logado()

    def cadastrar_solicitacao(self, dados: dict) -> tuple[bool, str]:
        # Limpeza e validação básica do CPF
        cpf = dados.get("cpf_colaborador", "").strip().replace(".", "").replace("-", "")
        if not (cpf and len(cpf) == 11 and cpf.isdigit()):
            return False, "CPF inválido."

        # Busca do colaborador em diferentes categorias
        pessoa = (
            self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                cpf
            )
            or self.__controlador_sistema.controlador_funcionario_rh.buscar_funcionario_rh_por_cpf(
                cpf
            )
            or self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(cpf)
        )
        if not pessoa:
            return False, "Colaborador não encontrado."

        # Verificação de tempo de admissão
        if pessoa.data_admissao:
            meses_admissao = (date.today() - pessoa.data_admissao).days / 30.44
            if meses_admissao < 12:
                return False, "Colaborador deve ter pelo menos 12 meses de admissão."

        # Verificação se há solicitação pendente para o mesmo CPF
        if any(
            sol.get("status") == "PENDENTE"
            for sol in self.buscar_solicitacoes_por_cpf(cpf)
        ):
            return (
                False,
                "Já existe uma solicitação pendente para este colaborador (pelo CPF informado).",
            )

        # Nova validação: verificar se já existe solicitação pendente para a pessoa (mesmo que o CPF mude)
        solicitacoes = self.__solicitacao.carregar_solicitacoes()
        for sol in solicitacoes:
            pessoa_sol = sol.get("pessoa", {})
            if pessoa_sol.get("cpf") == pessoa.cpf and sol.get("status") == "PENDENTE":
                return False, "Esta pessoa já possui uma solicitação pendente."

        # Validação dos períodos
        periodos = dados.get("periodos", [])
        if not periodos or not all(
            isinstance(inicio, date) and isinstance(fim, date)
            for inicio, fim in periodos
        ):
            return False, "Períodos inválidos ou não informados."

        hoje = date.today()

        for inicio, fim in periodos:
            if (inicio - hoje).days < 30:
                return (
                    False,
                    "Os períodos precisam ser solicitados com no mínimo 30 dias de antecedência.",
                )
            if inicio.weekday() in [4, 5, 6]:
                return False, "As férias não podem iniciar em sexta, sábado ou domingo."
            if fim <= inicio:
                return False, "Data final do período deve ser posterior à data inicial."

        # Validação do parcelamento
        parcelamento = dados.get("parcelamento", False)
        total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)
        if parcelamento:
            if (periodos[0][1] - periodos[0][0]).days + 1 != 14:
                return False, "O primeiro período do parcelamento deve conter 14 dias."
            if len(periodos) not in [2, 3] or total_dias != 30:
                return (
                    False,
                    "Parcelamento inválido: deve ter 2 ou 3 períodos totalizando 30 dias.",
                )
        else:
            if len(periodos) != 1 or total_dias != 30:
                return False, "Período único inválido: deve conter 30 dias contínuos."

        # Garantir que os períodos não sejam sobrepostos
        for i in range(len(periodos) - 1):
            if periodos[i][1] >= periodos[i + 1][0]:
                return False, "Os períodos não podem se sobrepor."

        # Geração de protocolo único
        protocolo = f"SOL-{hoje.strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}"

        pessoa_json = {
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "cargo": pessoa.cargo,
            "data_admissao": pessoa.data_admissao.strftime("%Y-%m-%d"),
            "email": pessoa.email,
        }

        nova_solicitacao = {
            "protocolo": protocolo,
            "pessoa": pessoa_json,
            "parcelamento": parcelamento,
            "status": "PENDENTE",
            "data_solicitacao": hoje.strftime("%Y-%m-%d"),
            "periodos": [
                {
                    "DATA_INICIO": inicio.strftime("%Y-%m-%d"),
                    "DATA_FIM": fim.strftime("%Y-%m-%d"),
                }
                for inicio, fim in periodos
            ],
        }

        # Salvar a nova solicitação
        solicitacoes.append(nova_solicitacao)
        self.__solicitacao.adicionar_pessoa(pessoa)
        self.__solicitacao.salvar_solicitacoes(solicitacoes)
        return True, f"Solicitação cadastrada com sucesso. Protocolo: {protocolo}"

    def buscar_solicitacoes(self) -> list:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            # Enriquecer com dados do colaborador
            for sol in solicitacoes:
                cpf = sol.get("pessoa")["cpf"]
                if cpf:
                    colaborador = (
                        self.__controlador_sistema.controlador_colaborador.buscar_colaborador_por_cpf(
                            cpf
                        )
                        or self.__controlador_sistema.controlador_funcionario_rh.buscar_funcionario_rh_por_cpf(
                            cpf
                        )
                        or self.__controlador_sistema.controlador_gestor.buscar_gestor_por_cpf(
                            cpf
                        )
                    )
                    if colaborador:
                        sol["nome_colaborador"] = colaborador.nome
                    else:
                        sol["nome_colaborador"] = "Nome não encontrado"
                else:
                    sol["nome_colaborador"] = "CPF não informado"

            return solicitacoes
        except Exception as e:
            print(f"Erro ao buscar solicitações: {e}")
            return []

    def buscar_solicitacoes_por_cpf(self, cpf: str) -> list:
        try:
            todas_solicitacoes = self.buscar_solicitacoes()
            return [s for s in todas_solicitacoes if s.get("pessoa")["cpf"] == cpf]
        except Exception as e:
            print(f"Erro ao buscar solicitações por CPF: {e}")
            return []

    def buscar_solicitacao_por_protocolo(self, protocolo: str) -> dict | None:
        try:
            solicitacoes = self.buscar_solicitacoes()
            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    return sol
            return None
        except Exception as e:
            print(f"Erro ao buscar solicitação: {e}")
            return None

    def aprovar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return False

                    sol["status"] = "APROVADA"
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao aprovar solicitação: {e}")
            return False

    def rejeitar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return False

                    sol["status"] = "REJEITADA"
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao rejeitar solicitação: {e}")
            return False

    def cancelar_solicitacao(self, protocolo: str) -> bool:
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()

            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    if sol.get("status") != "PENDENTE":
                        return False

                    sol["status"] = "CANCELADA"

                    self.__solicitacao.cancelar_solicitacao()
                    return self.__solicitacao.salvar_solicitacoes(solicitacoes)

            return False
        except Exception as e:
            print(f"Erro ao cancelar solicitação: {e}")
            return False
