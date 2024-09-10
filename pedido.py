
from datetime import date

class Pedido:

    def __init__(self: object, datapedido: date, IDUsuario: int, status: str) -> None:
        self.__id: int = id
        self.__datapedido: date = datapedido
        self.__IDUsuario: int = IDUsuario
        self.__status: str = status
    
    @property
    def id(self):
        return self.__id
    
    @property
    def datapedido(self):
        return self.__datapedido
    
    @property
    def IDUsuario(self):
        return self.__IDUsuario
    
    @property
    def status(self):
        return self.__status
    

