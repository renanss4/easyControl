class Usuario:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    # é usado quando você só digita o nome da variável no terminal, por exemplo → saída mais técnica/debug
    def __repr__(self):
        return f"<Usuario email={self.email}>"

    # é usado quando você chama str(objeto) ou print(objeto) → saída mais legível para humanos
    def __str__(self):
        return f"Usuário: {self.email}"
