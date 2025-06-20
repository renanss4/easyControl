from modelos.modelo_colaborador import Colaborador
from datetime import date


class ControladorColaborador:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__colaborador = Colaborador()
        self.__tela_colaborador = None

    @staticmethod
    def converter_dict_para_colaborador(colaborador_dict: dict) -> Colaborador | bool:
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

    # Navegação entre telas
    def abrir_tela_colaborador(self):
        from telas.tela_colaborador import TelaColaborador

        self.__tela_colaborador = TelaColaborador(self)
        return self.__tela_colaborador

    def voltar_tela_funcionario_rh(self):
        self.__tela_colaborador = None
        self.__controlador_sistema.controlador_funcionario_rh.abrir_tela_funcionario_rh()

    # CRUD de Colaborador
    def cadastrar_colaborador(self, cpf, nome, cargo, email) -> bool:
        try:
            dados = {
                "cpf": cpf.strip(),
                "nome": nome.strip(),
                "cargo": cargo.strip(),
                "email": email.strip(),
            }

            campos_obrigatorios = ["cpf", "nome", "cargo", "email"]

            # Verificar se todos os campos obrigatórios estão presentes
            for campo in campos_obrigatorios:
                if campo not in dados or not dados[campo]:
                    return False

            # Validar formato do CPF (11 dígitos)
            cpf = dados["cpf"].replace(".", "").replace("-", "")
            if len(cpf) != 11 or not cpf.isdigit():
                return False

            # Validar email básico
            email = dados["email"]
            if "@" not in email or "." not in email:
                return False

            # Carregar colaboradores existentes
            colaboradores = self.__colaborador.carregar_colaboradores()

            # Verificar se CPF já existe
            for col in colaboradores:
                if col.get("cpf") == dados["cpf"]:
                    return False  # CPF já existe

            # Criar novo colaborador
            novo_colaborador = {
                "cpf": dados["cpf"],
                "nome": dados["nome"],
                "cargo": dados["cargo"],
                "data_admissao": dados.get("data_admissao", date.today().isoformat()),
                "email": dados["email"],
            }

            colaboradores.append(novo_colaborador)
            return self.__colaborador.salvar_colaboradores(colaboradores)

        except Exception as e:
            print(f"Erro ao cadastrar colaborador: {e}")
            return False

    def buscar_colaboradores(self) -> list[Colaborador]:
        try:
            colaboradores = self.__colaborador.carregar_colaboradores()
            return [self.converter_dict_para_colaborador(col) for col in colaboradores]
        except Exception as e:
            print(f"Erro ao buscar colaboradores: {e}")
            return []

    def buscar_colaborador_por_cpf(self, cpf: str) -> Colaborador | None:
        try:
            colaboradores = self.__colaborador.carregar_colaboradores()
            for col_dict in colaboradores:
                if col_dict.get("cpf") == cpf:
                    return self.converter_dict_para_colaborador(col_dict)
            return None
        except Exception as e:
            print(f"Erro ao buscar colaborador: {e}")
            return None

    def atualizar_colaborador(
        self, cpf: str, nome: str, cargo: str, email: str
    ) -> bool:
        try:
            # Verificar se todos os campos obrigatórios estão presentes
            if not all([cpf, nome, cargo, email]):
                return False

            # Validar formato do CPF (11 dígitos)
            cpf = cpf.replace(".", "").replace("-", "")
            if len(cpf) != 11 or not cpf.isdigit():
                return False

            # Validar email básico
            if "@" not in email or "." not in email:
                return False

            colaboradores = self.__colaborador.carregar_colaboradores()

            for i, col in enumerate(colaboradores):
                if col.get("cpf") == cpf:
                    colaboradores[i]["nome"] = nome
                    colaboradores[i]["cargo"] = cargo
                    colaboradores[i]["email"] = email
                    return self.__colaborador.salvar_colaboradores(colaboradores)

            return False  # CPF não encontrado

        except Exception as e:
            print(f"Erro ao atualizar colaborador: {e}")
            return False

    def excluir_colaborador(self, cpf: str) -> bool:
        try:
            colaboradores = self.__colaborador.carregar_colaboradores()
            colaboradores_filtrados = [
                col for col in colaboradores if col.get("cpf") != cpf
            ]

            if len(colaboradores) == len(colaboradores_filtrados):
                return False  # CPF não encontrado

            return self.__colaborador.salvar_colaboradores(colaboradores_filtrados)

        except Exception as e:
            print(f"Erro ao excluir colaborador: {e}")
            return False
