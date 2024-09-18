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
                SET QuantidadeEmEstoque = %s
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
                SET Nome = %s, Descrição = %s, Preço = %s, Quantidadeemestoque = %s, Categoria_idCategoria = %s
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

    def inserirPagamento(self, pagamento):
        """Insere o pagamento no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql = """
                INSERT INTO pagamento (tipoPagamento, dataPagamento, status, valor, Pedido_idPedido)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (pagamento['tipoPagamento'], pagamento['dataPagamento'], pagamento['status'], pagamento['valor'],
                       pagamento['Pedido_idPedido'])
            cursor.execute(sql, valores)
            self.conexao.commit()
            cursor.close()

    def buscarPagamentoPorPedidoId(self, pedido_id):
        """Busca pagamento por ID do pedido."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            query = "SELECT * FROM pagamento WHERE Pedido_idPedido = %s"
            cursor.execute(query, (pedido_id,))
            result = cursor.fetchone()
            cursor.close()
            return result

    def buscarItensPorPedido(self, pedido_id):
        """Busca itens de um pedido específico."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            query = """
            SELECT p.Nome, ip.Quantidade, ip.Preco_unitario
            FROM produto p
            JOIN item_do_pedido ip ON p.idProduto = ip.idProduto
            WHERE ip.idPedido = %s
            """
            cursor.execute(query, (pedido_id,))
            result = cursor.fetchall()
            cursor.close()
            return result

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
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_update = """
                UPDATE Usuario
                SET Nome = %s, CPF = %s, Email = %s, Senha = %s, Endereco = %s, Telefone = %s, Administrador = %s
                WHERE IDUsuário = %s"""
            cursor.execute(sql_update, (nome, cpf, email, senha, endereco, telefone, administrador, id_usuario))
            self.conexao.commit()

    def validarUsuario(self, email, senha):
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

    def inserirPedido(self, pedido):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """INSERT INTO pedido (Data_pedido, IDUsuário, Status_pedido)VALUES (%s, %s, %s)"""
            valores = (pedido.data_pedido, pedido.id_usuario, pedido.status_pedido)
            cursor.execute(sql_insert, valores)
            self.conexao.commit()
            return cursor.lastrowid

    def listarPedidos(self):
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Pedido")
            pedidos = cursor.fetchall()
            return pedidos
        return []

    def buscarPedidoPorId(self, pedido_id):
        """Busca um pedido pelo ID."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            sql_select = """SELECT * FROM pedido WHERE idPedido = %s"""
            cursor.execute(sql_select, (pedido_id,))
            pedido = cursor.fetchone()
            return pedido
        return None

    def inserirItensPedido(self, pedido_id, itens):
        """Insere itens no pedido na tabela item_do_pedido."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql = """
                   INSERT INTO item_do_pedido (idPedido, idProduto, Quantidade, Preco_unitario)
                   VALUES (%s, %s, %s, %s)
               """
            for item in itens:
                preco_unitario = item.get('Preco_unitario', 0)  # Usar valor padrão se a chave não existir
                cursor.execute(sql, (pedido_id, item['IDProduto'], item['Quantidade'], preco_unitario))
            self.conexao.commit()
            cursor.close()

        # ==========================================
        # FUNÇÕES PARA ENDEREÇOS
        # ==========================================

    def listarEnderecos(self, id_usuario):
        """Lista todos os endereços de um usuário."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            try:
                sql_query = "SELECT * FROM Endereco WHERE IDUsuário = %s"
                cursor.execute(sql_query, (id_usuario,))
                enderecos = cursor.fetchall()
                return enderecos
            except Error as e:
                print("Erro ao listar endereços:", e)
            finally:
                cursor.close()
        return []

    def inserirEndereco(self, rua, numero, cidade, estado, cep, pais, id_usuario):
        """Insere um novo endereço no banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            sql_insert = """
                INSERT INTO endereco (rua, numero, cidade, estado, CEP, pais, Usuário_IDUsuário)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (rua, numero, cidade, estado, cep, pais, id_usuario))
            self.conexao.commit()
            cursor.close()

    def buscarEnderecosPorUsuario(self, id_usuario):
        """Busca endereços de um usuário específico."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor(dictionary=True)
            try:
                sql_query = "SELECT * FROM Endereco WHERE IDUsuário = %s"
                cursor.execute(sql_query, (id_usuario,))
                enderecos = cursor.fetchall()
                print("Endereços encontrados:", endereços)  # Depuração
                return enderecos
            except Error as e:
                print("Erro ao buscar endereços:", e)
            finally:
                cursor.close()
        return []

    def adicionarEndereco(self, id_usuario, endereco):
        """Adiciona um novo endereço ao banco de dados."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            try:
                sql_insert = """
                       INSERT INTO Endereco (IDUsuário, Rua, Número, Bairro, Cidade, Estado, CEP)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """
                cursor.execute(sql_insert, (
                id_usuario, endereco.rua, endereco.numero, endereco.bairro, endereco.cidade, endereco.estado,
                endereco.cep))
                self.conexao.commit()
            except Error as e:
                print("Erro ao adicionar endereço:", e)
                self.conexao.rollback()
            finally:
                cursor.close()

    def atualizarEndereco(self, id_endereco, novo_endereco):
        """Atualiza um endereço existente."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            try:
                sql_update = """
                       UPDATE Endereco
                       SET Rua = %s, Número = %s, Bairro = %s, Cidade = %s, Estado = %s, CEP = %s
                       WHERE idEndereco = %s
                   """
                cursor.execute(sql_update, (
                novo_endereco.rua, novo_endereco.numero, novo_endereco.bairro, novo_endereco.cidade,
                novo_endereco.estado, novo_endereco.cep, id_endereco))
                self.conexao.commit()
            except Error as e:
                print("Erro ao atualizar endereço:", e)
                self.conexao.rollback()
            finally:
                cursor.close()

    def removerEndereco(self, id_endereco):
        """Remove um endereço existente."""
        if self.conexao.is_connected():
            cursor = self.conexao.cursor()
            try:
                sql_delete = "DELETE FROM Endereco WHERE idEndereco = %s"
                cursor.execute(sql_delete, (id_endereco,))
                self.conexao.commit()
            except Error as e:
                print("Erro ao remover endereço:", e)
                self.conexao.rollback()
            finally:
                cursor.close()

    # ==========================================
    # FECHAR CONEXÃO
    # ==========================================

    def fecha(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Conexão com o MySQL fechada")

# Testando a classe Database
if __name__ == "__main__":
    db = Database()
    db.fecha()
