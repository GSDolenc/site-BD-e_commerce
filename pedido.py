from datetime import datetime


class Pedido:

    def __init__(self, data_pedido: datetime, id_usuario: int, status_pedido: str) -> None:
        self.__id: int = None  # Inicialize como None; será atribuído pelo banco de dados
        self.__data_pedido: datetime = data_pedido
        self.__id_usuario: int = id_usuario
        self.__status_pedido: str = status_pedido

    @property
    def id(self):
        return self.__id

    @property
    def data_pedido(self):
        return self.__data_pedido

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def status_pedido(self):
        return self.__status_pedido
