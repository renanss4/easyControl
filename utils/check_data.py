# check cpf
def check_cpf(cpf):
    """
    Verifica se o CPF é válido.
    """
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    return True

# check email
def check_email(email):
    """
    Verifica se o e-mail é válido.
    """
    if "@" not in email or "." not in email:
        return False
    return True