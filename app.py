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
            return redirect(url_for('listar_categorias'))
        else:
            return "Todos os campos são obrigatórios", 400

    return render_template('cadastro_categoria.html')

@app.route('/excluir_categoria/<int:id_categoria>', methods=['POST'])
def excluir_categoria(id_categoria):
    if not session.get('administrador'):
        return "Acesso negado", 403

    db.removerCategoria(id_categoria)
    return redirect(url_for('listar_categorias'))

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
    if not session.get('administrador'):
        return "Acesso negado", 403

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


@app.route('/editar_produto/<int:id_produto>', methods=['GET', 'POST'])
def editar_produto(id_produto):
    if not session.get('administrador'):
        return "Acesso negado", 403

    produto = db.buscarProdutoPorId(id_produto)

    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        categoria_id = request.form.get('categoria_id')

        if not categoria_id:
            return "Categoria não selecionada", 400

        db.atualizarProduto(id_produto, nome, descricao, preco, quantidade, categoria_id)
        return redirect(url_for('produtos'))

    categorias = db.listarCategorias()
    return render_template('editar_produto.html', produto=produto, categorias=categorias)


@app.route('/excluir_produto/<int:id_produto>', methods=['POST'])
def excluir_produto(id_produto):
    if not session.get('administrador'):
        return "Acesso negado", 403

    db.removerProduto(id_produto)
    return redirect(url_for('produtos'))



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
                estoque = produto.get('QuantidadeEmEstoque', 0)
                if quantidade <= estoque:
                    db.inserirCarrinho(id_produto, quantidade, id_usuario)
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
@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    carrinho_items = db.ListaCarrinho(session['id_usuario'])
    if carrinho_items:
        # Criar o pedido com os nomes corretos dos parâmetros
        pedido = Pedido(
            data_pedido=datetime.now(),
            id_usuario=session['id_usuario'],
            status_pedido='Pendente'
        )

        # Inserir o pedido e obter o ID
        pedido_id = db.inserirPedido(pedido)

        for item in carrinho_items:
            id_produto = item['IDProduto']
            quantidade = item['Quantidade']

            produto = db.buscarProdutoPorId(id_produto)
            estoque_atual = produto.get('Quantidadeemestoque', 0)

            novo_estoque = estoque_atual - quantidade
            if novo_estoque < 0:
                novo_estoque = 0

            db.atualizarEstoque(id_produto, novo_estoque)

        db.limparCarrinho(session['id_usuario'])

        return redirect(url_for('pagina_pagamento', pedido_id=pedido_id))

    return redirect(url_for('index'))


@app.route('/pagina_pagamento/<int:pedido_id>')
def pagina_pagamento(pedido_id):
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    # Buscar o pedido
    pedido = db.buscarPedidoPorId(pedido_id)

    if pedido:
        return render_template('pagina_pagamento.html', pedido=pedido)

    return "Pedido não encontrado", 404


@app.route('/processar_pagamento', methods=['POST'])
def processar_pagamento():
    pedido_id = request.form.get('pedido_id')
    tipo_pagamento = request.form.get('tipoPagamento')
    valor = calcular_valor_pedido(pedido_id)  # Função para calcular o valor total do pedido

    if tipo_pagamento == 'Cartão de Crédito':
        numero_cartao = request.form.get('numeroCartao')
        nome_cartao = request.form.get('nomeCartao')
        data_expiracao = request.form.get('dataExpiracao')

    # Inserir o pagamento na base de dados
    db.inserirPagamento(
        tipo_pagamento=tipo_pagamento,
        valor=valor,
        pedido_id=pedido_id
    )

    return redirect(url_for('index'))


# ==========================================
# ROTAS PARA GESTÃO DE USUÁRIOS
# ==========================================

# Página do perfil do usuário
@app.route('/usuario')
def usuario():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('login_usuario'))

    usuario = db.buscarUsuarioPorId(id_usuario)
    enderecos = db.buscarEnderecosPorUsuario(session['id_usuario'])

    return render_template('usuario.html', usuario=usuario, enderecos=enderecos)

# Login de usuários
@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = db.validarUsuario(email, senha)

        if usuario:
            session['id_usuario'] = usuario['IDUsuário']
            session['usuario_nome'] = usuario['Nome']
            session['administrador'] = usuario['Administrador']
            return redirect(url_for('index'))

        return "Email ou senha inválidos", 401

    return render_template('login.html')

# Cadastro de usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha = request.form.get('senha')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        administrador = request.form.get('administrador') == 'on'

        # Verifique se todos os campos obrigatórios estão preenchidos
        if not nome or not cpf or not email or not senha or not endereco or not telefone:
            return "Preencha todos os campos obrigatórios", 400

        db.inserirUsuario(nome, cpf, email, senha, endereco, telefone, administrador)
        return redirect(url_for('login_usuario'))

    return render_template('cadastro.html')


@app.route('/adicionar_endereco', methods=['POST'])
def adicionar_endereco():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    rua = request.form.get('rua')
    numero = request.form.get('numero')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    cep = request.form.get('cep')
    pais = request.form.get('pais')

    if rua and numero and cidade and estado and cep and pais:
        db.inserirEndereco(rua, numero, cidade, estado, cep, pais, session['id_usuario'])

    return redirect(url_for('usuario'))

# Logout
@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    session.pop('usuario_nome', None)
    session.pop('administrador', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
