# check cpf
def check_cpf(cpf):
    """
    Verifica se o CPF é válido.
    """
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    return True