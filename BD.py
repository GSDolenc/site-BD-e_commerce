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

    def removerCategoria(self, id_categoria):
        """Remove uma categoria pelo ID."""
        try:
            if self.conexao.is_connected():
                cursor = self.conexao.cursor()
                sql_delete = "DELETE FROM Categoria WHERE idCategoria = %s"
                cursor.execute(sql_delete, (id_categoria,))
                self.conexao.commit()
                print(f"Categoria {id_categoria} removida")  # Depuração
        except mysql.connector.Error as err:
            print(f"Erro ao remover categoria: {err}")

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

    def atualizarEstoque(self, id_produto, novo_estoque):
        """Atualiza a quantidade em estoque de um produto."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_update = """
                UPDATE Produto
                SET Quantidadeemestoque = %s
                WHERE idProduto = %s
            """
            cursor.execute(sql_update, (novo_estoque, id_produto))
            self.conexao.commit()
            cursor.close()

    def removerProduto(self, id_produto):
        """Remove um produto do banco de dados e atualiza o estoque se necessário."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            try:
                # Remover o produto do carrinho antes de removê-lo da tabela de produtos
                sql_remove_carrinho = "DELETE FROM Carrinho WHERE IDProduto = %s"
                cursor.execute(sql_remove_carrinho, (id_produto,))

                # Agora remover o produto da tabela de produtos
                sql_delete = "DELETE FROM Produto WHERE idProduto = %s"
                cursor.execute(sql_delete, (id_produto,))

                self.conexao.commit()
            except Exception as e:
                self.conexao.rollback()
                raise e
            finally:
                cursor.close()

    def atualizarProduto(self, id_produto, nome, descricao, preco, quantidade, categoria_id):
        try:
            with self.conexao.cursor() as cursor:
                sql = """
                UPDATE Produto
                SET Nome = %s, Descricao = %s, Preço = %s, Quantidadeemestoque = %s, Categoria_idCategoria = %s
                WHERE idProduto = %s
                """
                cursor.execute(sql, (nome, descricao, preco, quantidade, categoria_id, id_produto))
                self.conexao.commit()
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            self.conexao.rollback()

    # ==========================================
    # FUNÇÕES PARA CARRINHO DE COMPRAS
    # ==========================================

    def ListaCarrinho(self, id_usuario):
        """Lista os itens no carrinho de um usuário."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)  # Retorna dicionários ao invés de tuplas
            sql_query = """
                SELECT p.idProduto AS IDProduto, p.Nome, c.Quantidade, p.Preço
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

    def inserirUsuario(self, nome, cpf, email, senha, endereco, telefone, administrador):
        """Insere um novo usuário no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO Usuario (Nome, CPF, Email, Senha, Endereco, Telefone, Administrador)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (nome, cpf, email, senha, endereco, telefone, administrador)
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

    def atualizarUsuario(self, id_usuario, nome, cpf, email, senha, endereco, telefone, administrador):
        """Atualiza as informações de um usuário existente."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_update = """
                UPDATE Usuario
                SET Nome = %s, CPF = %s, Email = %s, Senha = %s, Endereco = %s, Telefone = %s, Administrador = %s
                WHERE IDUsuário = %s
            """
            cursor.execute(sql_update, (nome, cpf, email, senha, endereco, telefone, administrador, id_usuario))
            self.conexao.commit()

    def validarUsuario(self, email, senha):
        """Valida as credenciais do usuário para login."""
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

    # ==========================================
    # FUNÇÕES PARA PEDIDOS
    # ==========================================

    def inserirPedido(self, id_usuario, data_pedido, status_pedido):
        """Insere um novo pedido no banco de dados."""
        try:
            if self.conexao.is_connected():
                cursor = self.conexao.cursor()
                sql_insert = """
                    INSERT INTO Pedido (IDUsuário, Data_pedido, Status_pedido)
                    VALUES (%s, %s, %s)
                """
                valores = (id_usuario, data_pedido, status_pedido)
                cursor.execute(sql_insert, valores)
                self.conexao.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir pedido: {e}")
            self.conexao.rollback()
            raise e

    def listarPedidos(self):
        """Lista todos os pedidos do banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Pedido")
            pedidos = cursor.fetchall()
            return pedidos
        return []

    def buscarPedidoPorId(self, id_pedido):
        """Busca um pedido específico pelo ID."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_query = "SELECT * FROM Pedido WHERE idPedido = %s"
            cursor.execute(sql_query, (id_pedido,))
            pedido = cursor.fetchone()
            return pedido
        return None

    # ==========================================
    # FECHAR CONEXÃO
    # ==========================================

    def fecha(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Conexão com o MySQL fechada")

# Testando a classe Database
if __name__ == "__main__":
    db = Database()
    db.fecha()
