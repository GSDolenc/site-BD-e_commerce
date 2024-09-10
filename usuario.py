class Usuario:
    def __init__(self, nome, cpf, email, senha, endereco, telefone, administrador=False):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.endereco = endereco
        self.telefone = telefone
        self.administrador = administrador


    # Adicione um método para validar a senha
    def validar_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest() == self.senha
