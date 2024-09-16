from flask import Flask, render_template, request, redirect, url_for, session
from BD import Database
from usuario import Usuario
from pedido import Pedido
from produto import Produto
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

db = Database()

# ==========================================
# ROTAS PARA PRODUTOS E CATEGORIAS
# ==========================================

# Página inicial que lista os produtos
@app.route('/')
def index():
    produtos = db.ListaProdutos()
    return render_template('index.html', produtos=produtos)

# Lista todas as categorias
@app.route('/categorias')
def listar_categorias():
    categorias = db.listarCategorias()
    return render_template('categoria.html', categorias=categorias)

# Cadastro de categorias
@app.route('/cadastro_categoria', methods=['GET', 'POST'])
def cadastrar_categoria():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        if nome and descricao:
            db.inserirCategoria(nome, descricao)
            return redirect(url_for('listar_categorias'))  # Corrigido para o endpoint correto
        else:
            return "Todos os campos são obrigatórios", 400

    return render_template('cadastro_categoria.html')

# Lista produtos por categoria
@app.route('/categoria/<int:id_categoria>')
def produtos_por_categoria(id_categoria):
    produtos = db.listarProdutosPorCategoria(id_categoria)
    categoria = db.buscarCategoriaPorId(id_categoria)
    return render_template('produtos_categoria.html', produtos=produtos, categoria=categoria)

# Lista todos os produtos
@app.route('/produtos')
def produtos():
    produtos = db.ListaProdutos()
    return render_template('produtos.html', produtos=produtos)

# Adiciona um novo produto
@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    categorias = db.listarCategorias()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = request.form['categoria_id']
        produto = Produto(nome, descricao, preco, quantidade, categoria_id)
        db.inserirProdutos(produto)
        return redirect(url_for('index'))
    return render_template('adicionar_produto.html', categorias=categorias)

# ==========================================
# ROTAS PARA CARRINHO DE COMPRAS
# ==========================================

# Adiciona produto ao carrinho
@app.route('/adicionar_carrinho/<int:id_produto>', methods=['POST'])
def adicionar_carrinho(id_produto):
    quantidade = request.form.get('quantidade', type=int)
    id_usuario = session.get('id_usuario')

    if id_usuario:
        if quantidade and quantidade > 0:
            produto = db.buscarProdutoPorId(id_produto)
            if produto:
                estoque = produto.get('Quantidadeemestoque', 0)
                if quantidade <= estoque:
                    db.inserirCarrinho(id_produto, quantidade, id_usuario)

                    novo_estoque = estoque - quantidade
                    db.atualizarEstoque(id_produto, novo_estoque)

                    if novo_estoque == 0:
                        db.removerProduto(id_produto)

                    return redirect(url_for('carrinho'))
                else:
                    return "Quantidade solicitada excede o estoque disponível", 400
            else:
                return "Produto não encontrado", 404
        else:
            return "Quantidade inválida", 400
    else:
        return redirect(url_for('login_usuario'))

# Exibe o carrinho de compras
@app.route('/carrinho')
def carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    id_usuario = session.get('id_usuario')
    carrinho_items = db.ListaCarrinho(id_usuario)
    return render_template('carrinho.html', carrinho_items=carrinho_items)

# Limpa o carrinho de compras
@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    id_usuario = session['id_usuario']
    db.limparCarrinho(id_usuario)
    return redirect(url_for('carrinho'))

# ==========================================
# ROTAS PARA FINALIZAÇÃO DE COMPRA
# ==========================================

# Finaliza a compra
@app.route('/finalizar_compra', methods=['GET', 'POST'])
def finalizar_compra():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    if request.method == 'POST':
        carrinho_items = db.ListaCarrinho(session['id_usuario'])
        if carrinho_items:
            for item in carrinho_items:
                pedido = Pedido(
                    data_pedido=datetime.now(),
                    id_usuario=session['id_usuario'],
                    status='Pendente'
                )
                db.inserirPedido(pedido)

            db.limparCarrinho(session['id_usuario'])
        return redirect(url_for('index'))

    return render_template('finalizar_compra.html')

# ==========================================
# ROTAS PARA GESTÃO DE USUÁRIOS
# ==========================================

# Página do perfil do usuário
@app.route('/usuario')
def usuario():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    usuario = db.buscarUsuarioPorId(session['id_usuario'])
    return render_template('usuario.html', usuario=usuario)

# Login de usuários
@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = db.buscarUsuario(email, senha)

        if usuario:
            session['id_usuario'] = usuario['IDUsuário']
            session['usuario_nome'] = usuario['Nome']
            session['administrador'] = usuario['Administrador']
            return redirect(url_for('index'))
        else:
            return "Email ou senha incorretos", 400

    return render_template('login.html')

# Logout de usuários
@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    session.pop('usuario_nome', None)
    session.pop('administrador', None)
    return redirect(url_for('index'))

# Cadastro de novos usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')  # Corrigido para "cpf"
        email = request.form.get('email')
        senha = request.form.get('senha')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        administrador = request.form.get('administrador') == '1'

        if nome and cpf and email and senha and endereco and telefone:
            usuario = Usuario(
                nome=nome,
                cpf=cpf,
                email=email,
                senha=senha,
                endereco=endereco,
                telefone=telefone,
                administrador=administrador
            )
            db.inserirUsuario(usuario)  # Insere o novo usuário no banco de dados
            return redirect(url_for('login_usuario'))
        else:
            return "Todos os campos são obrigatórios", 400

    return render_template('cadastro.html')

@app.route('/verificar_sessao')
def verificar_sessao():
    administrador = session.get('administrador')
    return f"Administrador: {administrador}"

if __name__ == '__main__':
    app.run(debug=True)
