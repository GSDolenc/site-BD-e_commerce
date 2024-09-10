class Carrinho:

    def __init__(self: object, quantidade: int, idproduto: int) -> None:
        self.__id: int = id
        self.__quantidade: int = quantidade
        self.idproduto: int = idproduto
    
    @property
    def id(self):
        return self.__id
    
    @property
    def quantidade(self):
        return self.__quantidade
    
    @property
    def idproduto(self):
        return self.__idproduto