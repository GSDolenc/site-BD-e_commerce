class Categoria:

    def __init__(self: object, nome: str, descricao: str) -> None:
        self.__id: int = id
        self.__nome: str = nome
        self.__descricao: str = descricao

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao



