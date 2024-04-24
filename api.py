from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='.')

livros = [
    {'id': 1, 'titulo': 'It:A coisa', 'autor': 'Stephen King', 'sinopse': 'Nesse clássico que inspirou os filmes da Warner, um grupo de amigos conhecido como Clube dos Otários aprende o real sentido da amizade, do amor, da confiança... e do medo. O mais profundo e tenebroso medo. Durante as férias de 1958, em uma pacata cidadezinha chamada Derry, um grupo de sete amigos começa a ver coisas estranhas. Um conta que viu um palhaço, outro que viu uma múmia. Finalmente, acabam descobrindo que estavam todos vendo a mesma coisa: um ser sobrenatural e maligno que pode assumir várias formas. É assim que Bill, Beverly, Eddie, Ben, Richie, Mike e Stan enfrentam a Coisa pela primeira vez. Quase trinta anos depois, o grupo volta a se encontrar. Mike, o único que permaneceu em Derry, dá o sinal ― uma nova onda de terror tomou a pequena cidade. É preciso unir forças novamente. Só eles têm a chave do enigma. Só eles sabem o que se esconde nas entranhas de Derry. Só eles podem vencer a Coisa “Mesmo depois de tantos anos, o público continua obcecado por IT. Ficamos obcecados porque todos temos medos. Todos temos algo que nos assusta, sejam palhaços e aranhas ou coisas que se escondem em um lugar muito mais profundo de nossa mente. Este livro fala com todo mundo. É o romance mais assustador de King, e duvido que isso vá mudar” ― The Guardian'},
    {'id': 2, 'titulo': 'A arte da guerra', 'autor': 'Sun Tzu','sinopse': '"A guerra é um assunto de importância vital para o Estado; o reino da vida ou da morte; o caminho para a sobrevivência ou a ruína. É indispensável estudá-la profundamente." Sun Tzu'},
    {'id': 3, 'titulo': 'boa noite punpun', 'autor': 'Inio Asano','sinopse': 'A trama compreende quatro fases distintas da vida de Punpun: o Ensino Infantil, o Fundamental, o Médio e, por fim, a chegada aos seus 20 anos de idade. Neste mangá do gênero slice of life, os temas abordados mostram o início da vida de um adolescente nos aspectos psicológicos, físicos e sociais.'},
    {'id': 4, 'titulo': 'o menino que descobriu o vento', 'autor': 'William Kamkwamba','sinopse': 'Sempre esforçando-se para adquirir conhecimentos diversificados, um jovem de Malawi se cansa de assistir todos os colegas de seu vilarejo passando por dificuldades e começa a desenvolver uma inovadora turbina de vento.'},
    {'id': 5, 'titulo': 'relatos de um gato viajante', 'autor': 'hiro arikawa','sinopse': 'O ser humano é uma criatura arrogante demais para quem não passa de um macaco gigante que sabe andar ereto. O mais importante na vida é ter amigos com presença de espírito e senso de humor. Neste mundo, as paisagens que um gato jamais verá são muito maiores do que tudo o que ele chega a conhecer.'},
    {'id': 6, 'titulo': 'O alquimista', 'autor': 'Paulo coelho','sinopse': 'Santiago, um jovem pastor da Andaluzia, parte rumo ao Egito em busca de um tesouro escondido entre as Pirâmides. O que ele não sabe é que sua jornada o levará a riquezas muito diferentes  e mais satisfatórias  do que ele estava esperando.'},
    {'id': 7, 'titulo': 'a menina que roubava livros', 'autor': 'Markus Zusak','sinopse': 'Durante a Segunda Guerra Mundial, uma jovem garota chamada Liesel Meminger sobrevive fora de Munique lendo os livros que ela rouba. Ajudada por seu pai adotivo, ela aprende a ler e partilhar livros com seus amigos, incluindo um judeu que vive na clandestinidade em sua casa. Enquanto não está lendo ou estudando, ela faz algumas tarefas para a mãe e brinca com o amigo Rudy.'},
    {'id': 8, 'titulo': 'Blade Runner Origins', 'autor': 'K. Perkins','sinopse': 'Na Los Angeles de 2009, o corpo de uma cientista da TYRELL CORPORATION, que trabalhava num novo modelo de REPLICANTE, é encontrado numa cena de aparente suicídio. O detetive CAL MOREAUX é designado para o caso. Determinado a encontrar a verdade, ele enfrenta uma conspiração gigante e perversa dentro da própria Tyrell.'},
    {'id': 9, 'titulo': 'Venom protetor letal', 'autor': 'James R. Tuck','sinopse': 'Eddie Brock e seu simbionte alienígena partilham um objetivo. Eles querem matar o Homem-Aranha. Após numerosas tentativas de esmagar o Atirador de Teias, no entanto, estabelecem uma trégua complicada com ele e vão para o oeste, a fim de deixar a confusão para trás. Mas a confusão tem outros planos.'}
]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/editarlivro.html', methods=['GET'])
def editar_livro_page():
    return render_template('editarlivro.html')

@app.route('/livros', methods=['GET', 'POST'])
def manipular_livros():
    if request.method == 'GET':
        return render_template("listarlivros.html", livros=livros, livros_json=jsonify(livros).json)
    elif request.method == 'POST':
        novo_livro = request.form.to_dict()
        ultimo_id = max([livro['id'] for livro in livros]) if livros else 0
        novo_livro['id'] = ultimo_id + 1
        livros.append(novo_livro)
        return jsonify(novo_livro)

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
    return jsonify({"message": "Livro não encontrado"}), 404

@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice, livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])

@app.route('/livros/<int:id>/editar', methods=['GET'])
def editar_livro(id):
    for livro in livros:
        if livro.get('id') == id:
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

    for livro in livros:
        if livro['id'] == id:
            livro['titulo'] = novo_titulo
            livro['autor'] = novo_autor
            livro['sinopse'] = nova_sinopse
            return render_template('editar_livro.html', livro=livro)
    
    return jsonify({"message": "Livro não encontrado"}), 404

@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    global livros
    livros = [livro for livro in livros if livro['id'] != id]
    return jsonify({"message": "Livro excluído com sucesso!"}), 200

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
