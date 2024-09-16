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
                password='Root#123'
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

    # ==========================================
    # FUNÇÕES PARA CATEGORIAS
    # ==========================================

    def listarCategorias(self):
        """Lista todas as categorias do banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_query = "SELECT * FROM Categoria"
            cursor.execute(sql_query)
            categorias = cursor.fetchall()
            print("Categorias recuperadas:", categorias)  # Depuração
            return categorias
        return []

    def buscarCategoriaPorId(self, id_categoria):
        """Busca uma categoria específica pelo ID."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_query = "SELECT * FROM Categoria WHERE idCategoria = %s"
            cursor.execute(sql_query, (id_categoria,))
            categoria = cursor.fetchone()
            return categoria

    def inserirCategoria(self, nome, descricao):
        """Insere uma nova categoria no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = "INSERT INTO Categoria (Nome, Descricao) VALUES (%s, %s)"
            cursor.execute(sql_insert, (nome, descricao))
            self.conexao.commit()

    # ==========================================
    # FUNÇÕES PARA PRODUTOS
    # ==========================================

    def listarProdutosPorCategoria(self, id_categoria):
        """Lista produtos por categoria específica."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_query = "SELECT * FROM Produto WHERE Categoria_idCategoria = %s"
            cursor.execute(sql_query, (id_categoria,))
            produtos = cursor.fetchall()
            return produtos

    def ListaProdutos(self):
        """Lista todos os produtos disponíveis."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)  # Retorna dicionários ao invés de tuplas
            cursor.execute("SELECT * FROM Produto;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirProdutos(self, produto):
        """Insere um novo produto no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Produto (Nome, Descrição, Preço, Quantidadeemestoque, Categoria_idCategoria)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (produto.nome, produto.descricao, produto.preco, produto.quantidade, produto.categoria_id)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    def buscarProdutoPorId(self, id_produto):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_query = "SELECT * FROM Produto WHERE idProduto = %s"
            cursor.execute(sql_query, (id_produto,))
            produto = cursor.fetchone()
            print(f"Produto encontrado: {produto}")  # Depuração
            return produto
        return None

    def atualizarEstoque(self, id_produto, quantidade):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_update = """
                UPDATE Produto
                SET Quantidadeemestoque = %s
                WHERE idProduto = %s
            """
            cursor.execute(sql_update, (quantidade, id_produto))
            self.conexao.commit()
            print(f"Estoque atualizado para o produto {id_produto}: {quantidade}")  # Depuração

    def removerProduto(self, id_produto):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_delete = "DELETE FROM Produto WHERE idProduto = %s"
            cursor.execute(sql_delete, (id_produto,))
            self.conexao.commit()
            print(f"Produto {id_produto} removido")  # Depuração

    # ==========================================
    # FUNÇÕES PARA CARRINHO DE COMPRAS
    # ==========================================

    def ListaCarrinho(self, id_usuario):
        """Lista os itens no carrinho de um usuário."""
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
        """Limpa o carrinho de compras de um usuário."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_delete = "DELETE FROM Carrinho WHERE IDUsuário = %s"
            cursor.execute(sql_delete, (id_usuario,))
            self.conexao.commit()

    def inserirCarrinho(self, id_produto, quantidade, id_usuario):
        """Adiciona um item ao carrinho de compras."""
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

    # ==========================================
    # FUNÇÕES PARA USUÁRIOS
    # ==========================================

    def ListaUsuario(self):
        """Lista todos os usuários cadastrados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Usuario;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirUsuario(self, usuario):
            """Insere um novo usuário no banco de dados."""
            if self.conexao.is_connected():
                cursor = self.conexao.cursor()
                sql_insert = "INSERT INTO usuario (Nome, CPF, Email, Senha, Endereco, Telefone, Administrador) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                valores = (usuario.nome, usuario.cpf, usuario.email, usuario.senha, usuario.endereco, usuario.telefone, usuario.administrador)
                cursor.execute(sql_insert, valores)
                self.conexao.commit()

    def buscarUsuarioPorId(self, id_usuario):
        """Busca informações de um usuário pelo ID."""
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

    def buscarUsuario(self, email, senha):
        """Busca um usuário pelo email e senha."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            query = "SELECT * FROM Usuario WHERE Email = %s AND Senha = %s"
            cursor.execute(query, (email, senha))
            usuario = cursor.fetchone()
            cursor.close()
            return usuario
        return None

    # ==========================================
    # FUNÇÕES PARA PEDIDOS
    # ==========================================

    def ListaPedido(self):
        """Lista todos os pedidos realizados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Pedido;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirPedido(self, pedido):
        """Insere um novo pedido no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Pedido (DataPedido, IDUsuário, Status)
                VALUES (%s, %s, %s)
            """
            valores = (pedido.data_pedido, pedido.id_usuario, pedido.status)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    # ==========================================
    # FUNÇÕES PARA ENDEREÇOS
    # ==========================================

    def ListaEndereco(self):
        """Lista todos os endereços cadastrados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Endereco;")
            registros = cursor.fetchall()
            return registros
        return []

    def inserirEndereco(self, endereco):
        """Insere um novo endereço no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Endereco (Rua, Numero, Cidade, Estado, CEP, Pais, IDUsuário)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (endereco.rua, endereco.numero, endereco.cidade, endereco.estado, endereco.CEP, endereco.pais, endereco.IDUsuário)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()

    # ==========================================
    # FUNÇÃO PARA FECHAR CONEXÃO
    # ==========================================

    def fecha(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao.is_connected():
            self.conexao.close()
            print("Conexão ao MySQL encerrada")
