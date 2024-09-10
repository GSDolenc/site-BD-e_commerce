class Endereco:
    def __init__(self: object, rua: str, numero: int, cidade: str, estado: str, CEP: str, pais: str, IDUsuario: int) -> None:
        self.__id: int = id
        self.__rua: str = rua
        self.__numero: int = numero
        self.__cidade: str = cidade
        self.__estado: str = estado
        self.__CEP: str = CEP
        self.__pais: str = pais
        self.__IDUsuario: int = IDUsuario

    @property
    def id(self):
        return self.__id
    
    @property
    def rua(self):
        return self.__rua
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def cidade(self):
        return self.__cidade
    
    @property
    def estado(self):
        return self.__estado
    
    @property
    def CEP(self):
        return self.__CEP
    
    @property
    def pais(self):
        return self.__pais
    
    @property
    def IDUsuario(self):
        return self.__IDUsuario
