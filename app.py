from flask import Flask, render_template, request, redirect, url_for, session
from BD import Database
from usuario import Usuario
from pedido import Pedido

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

db = Database()

@app.route('/')
def index():
    produtos = db.ListaProdutos()
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar_carrinho/<int:id_produto>', methods=['POST'])
def adicionar_carrinho(id_produto):
    quantidade = request.form.get('quantidade')
    id_usuario = session.get('id_usuario')

    if id_usuario:
        db.inserirCarrinho(id_produto, quantidade, id_usuario)
        return redirect(url_for('carrinho'))
    else:
        return redirect(url_for('login_usuario'))

@app.route('/carrinho')
def carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))
    id_usuario = session.get('id_usuario')
    carrinho_items = db.ListaCarrinho(id_usuario)
    return render_template('carrinho.html', carrinho_items=carrinho_items)


@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    id_usuario = session['id_usuario']
    db.limparCarrinho(id_usuario)

    return redirect(url_for('carrinho'))


@app.route('/finalizar_compra', methods=['GET', 'POST'])
def finalizar_compra():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    if request.method == 'POST':
        carrinho_items = db.ListaCarrinho(session['id_usuario'])
        if carrinho_items:
            for item in carrinho_items:
                pedido = Pedido(
                    data_pedido=datetime.now(),  # Adicionando data do pedido
                    id_usuario=session['id_usuario'],
                    status='Pendente'  # Definindo um status padrão
                )
                db.inserirPedido(pedido)

            db.limparCarrinho(session['id_usuario'])
        return redirect(url_for('index'))

    return render_template('finalizar_compra.html')

@app.route('/usuario')
def usuario():
    if 'id_usuario' not in session:
        return redirect(url_for('login_usuario'))

    usuario = db.buscarUsuarioPorId(session['id_usuario'])
    return render_template('usuario.html', usuario=usuario)

@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = db.buscarUsuario(email, senha)

        if usuario:
            session['id_usuario'] = usuario['IDUsuário']
            session['usuario_nome'] = usuario['Nome']
            session['usuario_administrador'] = usuario.get('Administrador', False)
            return redirect(url_for('index'))
        else:
            return "Email ou senha incorretos", 400

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    session.pop('usuario_nome', None)
    session.pop('usuario_administrador', None)
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
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
            db.inserirUsuario(usuario)
            return redirect(url_for('login_usuario'))
        else:
            return "Todos os campos são obrigatórios", 400

    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
