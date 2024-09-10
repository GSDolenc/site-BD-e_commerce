import mysql.connector
from mysql.connector import Error
from categoria import Categoria
from produto import Produto
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

    def listarCategorias(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_query = "SELECT * FROM Categoria"
            cursor.execute(sql_query)
            categorias = cursor.fetchall()
            return categorias

    def listarProdutosPorCategoria(self, id_categoria):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_query = "SELECT * FROM Produto WHERE Categoria_idCategoria = %s"
            cursor.execute(sql_query, (id_categoria,))
            produtos = cursor.fetchall()
            return produtos

    def buscarCategoriaPorId(self, id_categoria):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_query = "SELECT * FROM Categoria WHERE idCategoria = %s"
            cursor.execute(sql_query, (id_categoria,))
            categoria = cursor.fetchone()
            return categoria

    def inserirCategoria(self, nome, descricao):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Categoria (Nome, Descricao) VALUES (%s, %s)"
            cursor.execute(sql_insert, (nome, descricao))
            self.conexao.commit()

    def ListaProdutos(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)  # Retorna dicionários ao invés de tuplas
            cursor.execute("SELECT * FROM Produto;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirProdutos(self, produto):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Produto (Nome, Descrição, Preço, Quantidadeemestoque, Categoria_idCategoria)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (produto.nome, produto.descricao, produto.preco, produto.quantidade, produto.categoria_id)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def ListaCarrinho(self, id_usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)  # Retorna dicionários ao invés de tuplas
            sql_query = """
                SELECT p.Nome, c.Quantidade, p.Preço
                FROM Carrinho c
                JOIN Produto p ON c.IDProduto = p.idProduto
                WHERE c.IDUsuário = %s
            """
            cursor.execute(sql_query, (id_usuario,))
            registros = cursor.fetchall()
            return registros

    def limparCarrinho(self, id_usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_delete = "DELETE FROM Carrinho WHERE IDUsuário = %s"
            cursor.execute(sql_delete, (id_usuario,))
            self.conexao.commit()

    def inserirCarrinho(self, id_produto, quantidade, id_usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Carrinho (IDProduto, Quantidade, IDUsuário)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE Quantidade = Quantidade + VALUES(Quantidade)
            """
            valores = (id_produto, quantidade, id_usuario)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def ListaUsuario(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Usuario;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirUsuario(self, usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Usuario (Nome, CPF, Email, Senha, Endereço, Telefone, Administrador)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (usuario.nome, usuario.CPF, usuario.email, usuario.senha, usuario.endereco, usuario.telefone,
                       usuario.administrador)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def buscarUsuarioPorId(self, id_usuario):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_select = """
                SELECT * FROM Usuario
                WHERE IDUsuário = %s
            """
            cursor.execute(sql_select, (id_usuario,))
            usuario = cursor.fetchone()
            return usuario
        return None

    def ListaPedido(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Pedido;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirPedido(self, pedido):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Pedido (DataPedido, IDUsuário, Status)
                VALUES (%s, %s, %s)
            """
            valores = (pedido.data_pedido, pedido.id_usuario, pedido.status)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def ListaEndereco(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Endereco;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirEndereco(self, endereco):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Endereco (Rua, Numero, Cidade, Estado, CEP, Pais, IDUsuário)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (endereco.rua, endereco.numero, endereco.cidade, endereco.estado, endereco.CEP, endereco.pais, endereco.IDUsuário)
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
        return None

    def fecha(self):
        if self.conexao.is_connected():
            self.conexao.close()
            print("Conexão ao MySQL encerrada")
