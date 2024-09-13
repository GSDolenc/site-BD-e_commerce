class Categoria:
    def __init__(self, nome: str, descricao: str, id: int = None) -> None:
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

class Produto:
    def __init__(self, nome, descricao, preco, quantidade, categoria_id):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade
        self.categoria_id = categoria_id
