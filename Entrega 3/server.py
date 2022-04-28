from flask import Flask, request, make_response, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('BD.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=["GET"])
def root():
    db = get_db_connection()

    query = 'SELECT * FROM utilizadores;'
    query1 = 'SELECT * FROM disciplina;'
    query2 = 'SELECT * FROM turma;'
    query3 = 'SELECT * FROM inscricoes;'
    
    row = db.execute(query)

    return request.method

@app.route('/alunos', methods=["PUT"])
@app.route('/alunos/<int:numero>', methods=["GET"])
def aluno(numero=None):
    if request.method == "GET":
        # Ler dados do aluno com id na base de dados
        db = get_db_connection()
        row = db.execute('SELECT * FROM aluno WHERE numero = ?', (numero,)).fetchone()
        db.close()

        if not row:
            return {}, 404
        else:
            return {'data': dict(row)}, 200

    elif request.method == "PUT":
        body = request.get_json()
        if 'numero' not in body:
            return {'message': 'numero is required'}, 400
        elif not isinstance(body['numero'], int):
            return {'message': 'numero is not an int'}, 400
        elif 'nome' not in body:
            return {'message': 'nome is required'}, 400

        numero = body['numero']
        nome = body['nome']

        try:
            db = get_db_connection()
            db.execute("INSERT INTO aluno (numero, nome) VALUES (?, ?)", (numero, nome))
            db.commit()
            db.close()

            r = make_response()
            r.headers['location'] = f'/alunos/{body["numero"]}'
            return r
        except sqlite3.IntegrityError:
            return {'message': 'Erro de integridade'}, 400


@app.route('/notas', methods=["POST", "GET"])
def notas():
    if request.method == "POST":
        body = request.get_json()

        if 'numero_aluno' not in body:
            return {'message': 'numero_aluno is required'}, 400
        elif not isinstance(body['numero_aluno'], int):
            return {'message': 'numero_aluno is not an int'}, 400
        elif 'ano' not in body:
            return {'message': 'ano is required'}, 400
        elif 'cadeira' not in body:
            return {'message': 'cadeira is required'}, 400
        elif 'nota' not in body:
            return {'message': 'nota is required'}, 400
        elif not isinstance(body['nota'], int):
            return {'message': 'nota is not an int'}, 400

        numero_aluno = body['numero_aluno']
        ano = body['ano']
        cadeira = body['cadeira']
        nota = body['nota']

        try:
            db = get_db_connection()
            db.execute("INSERT INTO notas (numero_aluno, ano, cadeira, nota) VALUES (?, ?, ?, ?)", (numero_aluno, ano, cadeira, nota))
            db.commit()
            db.close()

            return 201
        except sqlite3.IntegrityError:
            return {'message': 'Erro de integridade'}, 400

    if request.method == "GET":
        # ler campos no pedido e fazer query de acordo
        r = make_response(request.data)  # Devolve os dados no pedido
        return r


if __name__ == '__main__':
    app.run(debug=True)
