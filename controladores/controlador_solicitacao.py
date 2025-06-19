from modelos.modelo_solicitacao import Solicitacao
from datetime import date, datetime
import random
import string


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
        """Abre a tela de solicitação - direciona baseado no tipo de usuário"""
        usuario_logado = self.__controlador_sistema.usuario_logado
        
        if hasattr(usuario_logado, "__class__") and "FuncionarioRH" in str(usuario_logado.__class__):
            # Para RH: vai direto para cadastro de solicitação
            from telas.tela_solicitacao import CadastraSolicitacao
            self.__tela_solicitacao = CadastraSolicitacao(self)
        else:
            # Para Gestor: vai direto para análise de solicitações
            from telas.tela_solicitacao import AnalisarSolicitacao
            self.__tela_solicitacao = AnalisarSolicitacao(self)
        
        return self.__tela_solicitacao

    def voltar_tela_funcionario_rh(self):
        """Volta para a tela do funcionário RH"""
        self.__tela_solicitacao = None
        return self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    def voltar_tela_gestor(self):
        """Volta para a tela do gestor logado"""
        self.__tela_solicitacao = None
        return self.__controlador_sistema.controlador_gestor.abrir_tela_gestor_logado()

    def gerar_protocolo(self) -> str:
        """Gera um número de protocolo único no formato: SOL-YYYYMMDD-XXXXX"""
        data = datetime.now().strftime("%Y%m%d")
        aleatorio = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"SOL-{data}-{aleatorio}"

    # ==================== VALIDAÇÕES ====================

    def validar_cpf(self, cpf: str) -> tuple[bool, str]:
        """Valida o formato do CPF"""
        if not cpf or not cpf.strip():
            return False, "Por favor, preencha o CPF."
        
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        if len(cpf_limpo) != 11 or not cpf_limpo.isdigit():
            return False, "CPF deve conter 11 dígitos numéricos!"
        
        # Verificar se colaborador existe
        colaborador = self.__controlador_sistema.controlador_colaborador.buscar_por_cpf(cpf)
        if not colaborador:
            return False, "Colaborador não encontrado no sistema!"
        
        return True, ""

    def validar_solicitacao_pendente(self, cpf: str) -> tuple[bool, str]:
        """Valida se não há solicitação pendente para o colaborador"""
        solicitacoes_existentes = self.buscar_solicitacoes_por_cpf(cpf)
        if any(sol.get("status") == "pendente" for sol in solicitacoes_existentes):
            return False, "Este colaborador já possui uma solicitação pendente"
        return True, ""

    def validar_periodo_ferias(self, inicio: date, fim: date) -> tuple[bool, str]:
        """Valida um período de férias"""
        # Validar antecedência mínima
        if (inicio - date.today()).days < 30:
            return False, "A solicitação deve ser feita com no mínimo 30 dias de antecedência"
            
        # Validar dia útil no início da semana
        dia_semana = inicio.weekday()
        if dia_semana in [4, 5, 6]:  # 4=sexta, 5=sábado, 6=domingo
            if dia_semana == 4:
                return False, "As férias não podem iniciar em uma sexta-feira"
            else:
                return False, "As férias devem iniciar em um dia útil"
        
        # Validar se fim é após início
        if fim <= inicio:
            return False, "A data fim deve ser posterior à data início"
            
        return True, ""

    def validar_datas_formato(self, data_str: str) -> tuple[bool, str, date]:
        """Valida e converte string de data para objeto date"""
        try:
            data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
            return True, "", data_obj
        except ValueError:
            return False, "Formato de data inválido", None

    def validar_periodo_nao_parcelado(self, inicio: date, fim: date) -> tuple[bool, str]:
        """Valida se o período único tem exatamente 30 dias e atende às regras"""
        dias = (fim - inicio).days + 1
        
        # Validar quantidade de dias
        if dias != 30:
            return False, "Para férias não parceladas, o período deve ser de exatamente 30 dias"
        
        # Validar regras básicas do período
        valido, msg = self.validar_periodo_ferias(inicio, fim)
        if not valido:
            return False, msg
            
        return True, ""

    def validar_parcelamento_ferias(self, periodos: list[tuple[date, date]]) -> tuple[bool, str]:
        """Valida as regras de parcelamento de férias"""
        if len(periodos) < 2 or len(periodos) > 3:
            return False, "Parcelamento deve ter 2 ou 3 períodos"
            
        total_dias = sum((fim - inicio).days + 1 for inicio, fim in periodos)
        if total_dias != 30:
            return False, "O total de dias deve ser exatamente 30"
        
        # Validar primeiro período de 14 dias
        primeiro_periodo = periodos[0]
        dias_primeiro = (primeiro_periodo[1] - primeiro_periodo[0]).days + 1
        if dias_primeiro != 14:
            return False, "O primeiro período do parcelamento deve ter exatamente 14 dias"
            
        return True, ""

    def validar_periodos_sequenciais(self, periodos: list[tuple[date, date]]) -> tuple[bool, str]:
        """Valida se os períodos estão em ordem cronológica e atendem às regras"""
        for i, (inicio, fim) in enumerate(periodos):
            # Validar cada período individualmente
            valido, msg = self.validar_periodo_ferias(inicio, fim)
            if not valido:
                return False, f"Período {i+1}: {msg}"
                
            # Validar sequência (não pode haver sobreposição)
            if i < len(periodos) - 1:
                proximo_inicio = periodos[i + 1][0]
                if fim >= proximo_inicio:
                    return False, "Os períodos devem ser sequenciais e não podem se sobrepor"
                
        return True, ""

    def validar_solicitacao_completa(self, dados: dict) -> tuple[bool, str]:
        """Valida todos os dados da solicitação"""
        cpf = dados.get("cpf_colaborador", "").strip()
        periodos_data = dados.get("periodos", [])
        parcelamento = dados.get("parcelamento", False)
        
        # Validar CPF
        valido, msg = self.validar_cpf(cpf)
        if not valido:
            return False, msg
        
        # Validar se não há solicitação pendente
        valido, msg = self.validar_solicitacao_pendente(cpf)
        if not valido:
            return False, msg
        
        # Validar se há períodos
        if not periodos_data:
            return False, "É necessário informar pelo menos um período"
        
        # Converter e validar períodos
        periodos = []
        for i, (inicio, fim) in enumerate(periodos_data):
            if not isinstance(inicio, date):
                return False, f"Data de início do período {i+1} inválida"
            if not isinstance(fim, date):
                return False, f"Data de fim do período {i+1} inválida"
            periodos.append((inicio, fim))
        
        # Validar períodos sequenciais
        valido, msg = self.validar_periodos_sequenciais(periodos)
        if not valido:
            return False, msg
        
        # Validar regras específicas baseado no parcelamento
        if not parcelamento:
            if len(periodos) > 1:
                return False, "Sem parcelamento, deve haver apenas um período"
            valido, msg = self.validar_periodo_nao_parcelado(periodos[0][0], periodos[0][1])
            if not valido:
                return False, msg
        else:
            valido, msg = self.validar_parcelamento_ferias(periodos)
            if not valido:
                return False, msg
        
        return True, ""

    # ==================== OPERAÇÕES PRINCIPAIS ====================

    def cadastrar_solicitacao(self, dados: dict) -> tuple[bool, str]:
        """Cadastra uma nova solicitação com validação completa"""
        try:
            # Validar todos os dados
            valido, msg = self.validar_solicitacao_completa(dados)
            if not valido:
                return False, msg

            # Criar nova solicitação
            nova_solicitacao = {
                "protocolo": self.gerar_protocolo(),
                "cpf_colaborador": dados.get("cpf_colaborador"),
                "parcelamento": dados.get("parcelamento", False),
                "status": "pendente",
                "data_solicitacao": datetime.now().strftime("%Y-%m-%d"),
                "periodos": [
                    {
                        "data_inicio": inicio.strftime("%Y-%m-%d"),
                        "data_fim": fim.strftime("%Y-%m-%d"),
                    }
                    for inicio, fim in dados.get("periodos", [])
                ],
            }

            # Carregar solicitações existentes
            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            solicitacoes.append(nova_solicitacao)
            
            # Salvar
            if self.__solicitacao.salvar_solicitacoes(solicitacoes):
                return True, "Solicitação cadastrada com sucesso!"
            else:
                return False, "Erro ao salvar solicitação"

        except Exception as e:
            return False, f"Erro interno: {str(e)}"

    def buscar_solicitacoes(self) -> list:
        """Busca todas as solicitações"""
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            
            # Enriquecer com dados do colaborador
            for sol in solicitacoes:
                cpf = sol.get("cpf_colaborador")
                if cpf:
                    colaborador = self.__controlador_sistema.controlador_colaborador.buscar_por_cpf(cpf)
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
        """Busca solicitações por CPF do colaborador"""
        try:
            todas_solicitacoes = self.buscar_solicitacoes()
            return [s for s in todas_solicitacoes if s.get("cpf_colaborador") == cpf]
        except Exception as e:
            print(f"Erro ao buscar solicitações por CPF: {e}")
            return []

    def buscar_solicitacoes_equipe(self, cpf_gestor: str) -> list:
        """Busca solicitações da equipe do gestor"""
        try:
            # Por enquanto, retorna todas as solicitações enriquecidas
            return self.buscar_solicitacoes()
        except Exception as e:
            print(f"Erro ao buscar solicitações da equipe: {e}")
            return []

    def validar_operacao_solicitacao(self, protocolo: str, operacao: str) -> tuple[bool, str]:
        """Valida se uma operação pode ser realizada na solicitação"""
        try:
            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            solicitacao = next((s for s in solicitacoes if s.get("protocolo") == protocolo), None)
            
            if not solicitacao:
                return False, "Solicitação não encontrada"
            
            status_atual = solicitacao.get("status", "")
            
            if operacao in ["aprovar", "rejeitar", "cancelar"] and status_atual != "pendente":
                return False, f"Apenas solicitações pendentes podem ser {operacao}das"
            
            return True, ""
        except Exception as e:
            return False, f"Erro ao validar operação: {str(e)}"

    def aprovar_solicitacao(self, protocolo: str) -> tuple[bool, str]:
        """Aprova uma solicitação"""
        try:
            # Validar operação
            valido, msg = self.validar_operacao_solicitacao(protocolo, "aprovar")
            if not valido:
                return False, msg

            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    sol["status"] = "aprovado"
                    if self.__solicitacao.salvar_solicitacoes(solicitacoes):
                        return True, "Solicitação aprovada com sucesso!"
                    else:
                        return False, "Erro ao salvar aprovação"
            
            return False, "Solicitação não encontrada"
        except Exception as e:
            return False, f"Erro ao aprovar: {str(e)}"

    def rejeitar_solicitacao(self, protocolo: str) -> tuple[bool, str]:
        """Rejeita uma solicitação"""
        try:
            # Validar operação
            valido, msg = self.validar_operacao_solicitacao(protocolo, "rejeitar")
            if not valido:
                return False, msg

            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    sol["status"] = "rejeitado"
                    if self.__solicitacao.salvar_solicitacoes(solicitacoes):
                        return True, "Solicitação rejeitada com sucesso!"
                    else:
                        return False, "Erro ao salvar rejeição"
            
            return False, "Solicitação não encontrada"
        except Exception as e:
            return False, f"Erro ao rejeitar: {str(e)}"

    def cancelar_solicitacao(self, protocolo: str) -> tuple[bool, str]:
        """Cancela uma solicitação"""
        try:
            # Validar operação
            valido, msg = self.validar_operacao_solicitacao(protocolo, "cancelar")
            if not valido:
                return False, msg

            solicitacoes = self.__solicitacao.carregar_solicitacoes()
            for sol in solicitacoes:
                if sol.get("protocolo") == protocolo:
                    sol["status"] = "cancelada"
                    if self.__solicitacao.salvar_solicitacoes(solicitacoes):
                        return True, "Solicitação cancelada com sucesso!"
                    else:
                        return False, "Erro ao salvar cancelamento"
            
            return False, "Solicitação não encontrada"
        except Exception as e:
            return False, f"Erro ao cancelar: {str(e)}"

    def converter_dict_para_solicitacao(self, solicitacao_dict: dict) -> Solicitacao | bool:
        try:
            return True
        except Exception as e:
            print(f"Erro ao converter solicitação: {e}")
            return False
