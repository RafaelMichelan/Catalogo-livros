from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, template_folder='.')

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/editarlivro.html', methods=['GET'])
def editar_livro_page():
    return render_template('editarlivro.html')

@app.route('/livros', methods=['GET', 'POST'])
def manipular_livros():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM livros')
        livros = cursor.fetchall()
        return render_template("listarlivros.html", livros=livros)
    elif request.method == 'POST':
        novo_livro = request.form.to_dict()
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO livros (titulo, autor, sinopse) VALUES (%s, %s, %s)',
            (novo_livro['titulo'], novo_livro['autor'], novo_livro['sinopse'])
        )
        mysql.connection.commit()
        return redirect(url_for('manipular_livros'))

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM livros WHERE id = %s', (id,))
    livro = cursor.fetchone()
    if livro:
        return jsonify(livro)
    return jsonify({"message": "Livro não encontrado"}), 404

@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE livros SET titulo = %s, autor = %s, sinopse = %s WHERE id = %s',
        (livro_alterado['titulo'], livro_alterado['autor'], livro_alterado['sinopse'], id)
    )
    mysql.connection.commit()
    return jsonify(livro_alterado)

@app.route('/livros/<int:id>/editar', methods=['GET'])
def editar_livro(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM livros WHERE id = %s', (id,))
    livro = cursor.fetchone()
    if livro:
        return render_template('editar_livro.html', livro=livro)
    return jsonify({"message": "Livro não encontrado"}), 404

@app.route('/livros/novo', methods=['POST'])
def novo_livro():
    return render_template('incluirlivro.html')

@app.route('/livros/<int:id>/editar', methods=['POST'])
def salvar_edicao_livro(id):
    novo_titulo = request.form['titulo']
    novo_autor = request.form['autor']
    nova_sinopse = request.form['sinopse']

    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE livros SET titulo = %s, autor = %s, sinopse = %s WHERE id = %s',
        (novo_titulo, novo_autor, nova_sinopse, id)
    )
    mysql.connection.commit()

    cursor.execute('SELECT * FROM livros WHERE id = %s', (id,))
    livro = cursor.fetchone()
    return render_template('editar_livro.html', livro=livro)

@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM livros WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({"message": "Livro excluído com sucesso!"}), 200

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)