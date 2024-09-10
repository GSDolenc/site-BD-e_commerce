import mysql.connector
from mysql.connector import Error
from categoria import Categoria
from produto import Produtos
from carrinho import Carrinho
from usuario import Usuario
from pedido import Pedido
from endereco import Endereco

class Database:
    conexao = None

    def __init__(self):
        try:
            self.conexao = mysql.connector.connect(
                host='localhost',
                database='mydb',
                user='root',
                password='root'
            )
            if self.conexao.is_connected():
                db_info = self.conexao.get_server_info()
                print("Conectado ao servidor MySQL versão", db_info)
                cursor = self.conexao.cursor()
                cursor.execute("SELECT DATABASE();")
                nome_do_banco = cursor.fetchone()
                print("Conectado ao banco de dados", nome_do_banco[0])
        except Error as e:
            print("Erro ao conectar ao MySQL", e)

    def ListaCategorias(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Categoria;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            for Linha in registros:
                print("Id:", Linha[0], "Nome:", Linha[1], 'Descrição:', Linha[2])
            return registros

    def inserirCategoria(self, categoria):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Categoria (nome, descricao) VALUES (%s, %s)"
            valores = (categoria.nome, categoria.descricao)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()  # Garantir que os dados são salvos
            print("Categoria inserida com sucesso")

    def ListaProdutos(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT Nome, Descrição, Preço, Quantidadeemestoque FROM Produto;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            return registros

    def inserirProdutos(self, produto):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Produto (Nome, Descrição, Preço, Quantidadeemestoque, Categoria_idCategoria)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (produto.nome, produto.descricao, produto.preco, produto.quantidade, produto.categoria_id)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()  # Garantir que os dados são salvos

    def ListaCarrinho(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Carrinho;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            return registros

    def inserirCarrinho(self, id_produto, quantidade, id_usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Carrinho (idproduto, quantidade, IDUsuario) VALUES (%s, %s, %s)"
            valores = (id_produto, quantidade, id_usuario)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()
            print("Produto adicionado ao carrinho com sucesso")

    def ListaUsuario(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Usuario;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            return registros

    def inserirUsuario(self, usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Usuario (Nome, CPF, Email, Senha, Endereço, Telefone, Administrador)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (usuario.nome, usuario.CPF, usuario.email, usuario.senha, usuario.endereco, usuario.telefone, usuario.administrador)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()  # Garantir que os dados são salvos
            print("Usuário inserido com sucesso")

    def ListaPedido(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Pedido;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            return registros

    def inserirPedido(self, pedido):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Pedido (datapedido, IDUsuario, status)
                VALUES (%s, %s, %s)
            """
            valores = (pedido.datapedido, pedido.IDUsuario, pedido.status)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def ListaEndereco(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Endereco;")
            registros = cursor.fetchall()
            print("Total de registros encontrados:", cursor.rowcount)
            return registros

    def inserirEndereco(self, endereco):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Endereco (rua, numero, cidade, estado, CEP, pais, IDUsuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (endereco.rua, endereco.numero, endereco.cidade, endereco.estado, endereco.CEP, endereco.pais, endereco.IDUsuario)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def buscarUsuario(self, email, senha):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_select = """
                SELECT * FROM Usuario 
                WHERE Email = %s AND Senha = %s
            """
            cursor.execute(sql_select, (email, senha))
            usuario = cursor.fetchone()
            return usuario

    def fecha(self):
        if self.conexao.is_connected():
            self.conexao.close()
            print("Conexão ao MySQL encerrada")
