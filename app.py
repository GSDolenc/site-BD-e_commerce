from flask import Flask, render_template, request, redirect, url_for, session, flash
from BD import Database
from usuario import Usuario
from produto import Produtos
from categoria import Categoria

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessões

# Instancia o banco de dados
db = Database()

# Página inicial com produtos
@app.route('/')
def index():
    produtos = db.ListaProdutos()
    return render_template('index.html', produtos=produtos)

# Página de detalhes do usuário
@app.route('/usuario')
def usuario():
    if 'usuario_id' in session:
        return f"Bem-vindo, {session['usuario_nome']}!"
    else:
        return redirect(url_for('login'))

# Página de login
@app.route('/usuario/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se o usuário existe no banco de dados
        usuario = db.buscarUsuario(email, senha)
        if usuario:
            session['usuario_id'] = usuario['IDUsuário']
            session['usuario_nome'] = usuario['Nome']
            session['usuario_administrador'] = usuario['Administrador']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha inválidos.', 'danger')

    return render_template('login.html')

# Página de cadastro de novo usuário
@app.route('/usuario/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['CPF']
        email = request.form['email']
        senha = request.form['senha']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        administrador = 'administrador' in request.form  # Verifica se o checkbox 'administrador' foi marcado

        # Cria um objeto Usuario
        usuario = Usuario(nome, cpf, email, senha, endereco, telefone, administrador)

        # Insere o usuário no banco de dados
        db.inserirUsuario(usuario)

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Logout do usuário
@app.route('/usuario/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    session.pop('usuario_administrador', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# Página de carrinho de compras
@app.route('/carrinho')
def carrinho():
    carrinho = db.ListaCarrinho()
    return render_template('carrinho.html', carrinho=carrinho)


@app.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    id_produto = request.form.get('id_produto')
    quantidade = request.form.get('quantidade')

    if id_produto and quantidade:
        db = Database()
        # Verificar se o usuário está logado e tem um ID de usuário
        id_usuario = session.get('user_id')  # Você pode ajustar isso conforme a lógica de autenticação

        if id_usuario:
            db.inserirCarrinho(id_produto, quantidade, id_usuario)
            db.fecha()
            return redirect(url_for('index'))
        else:
            return "Usuário não autenticado", 403
    return "Dados inválidos", 400

# Página de cadastro de produto
@app.route('/produto/cadastro', methods=['GET', 'POST'])
def cadastro_produto():
    if 'usuario_id' not in session or not session.get('usuario_administrador'):
        flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = request.form['categoria_id']  # Correto: obtendo o ID da categoria

        produto = Produtos(nome, descricao, preco, quantidade, categoria_id)
        db.inserirProdutos(produto)

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))

    categorias = db.ListaCategorias()  # Obtendo categorias para exibir no formulário
    return render_template('cadastro_produto.html', categorias=categorias)

# Página de categorias
@app.route('/categoria')
def categoria():
    categorias = db.ListaCategorias()
    return render_template('categoria.html', categorias=categorias)

# Página de cadastro de categorias
@app.route('/cadastro_categoria', methods=['GET', 'POST'])
def cadastro_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        cat = Categoria(nome, descricao)
        db.inserirCategoria(cat)
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('categoria'))
    return render_template('cadastro_categoria.html')

# Página de endereços
@app.route('/endereco')
def endereco():
    enderecos = db.ListaEndereco()
    return render_template('endereco.html', enderecos=enderecos)

# Página de pedidos
@app.route('/pedido')
def pedido():
    pedidos = db.ListaPedido()
    return render_template('pedido.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)
