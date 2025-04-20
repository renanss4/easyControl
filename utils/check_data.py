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
    email = email.strip()
    email = email.lower()
    if "@" not in email or "." not in email:
        return False
    return True

# check password
# senha deve ter pelo menos 8 caracteres
# e pelo menos uma letra maiúscula, uma letra minúscula e um número
def check_password(password):
    """
    Verifica se a senha é válida.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True