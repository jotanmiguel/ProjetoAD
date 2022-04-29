from flask import Flask, request, make_response, abort
import sqlite3

import requests
import json
import os

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('BD.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/utilizadores', methods=["POST"])
#@app.route('/alunos/<int:numero>', methods=["GET"])
def utilizadores():
    if request.method == "POST":
        body = request.get_json()

        nome = body['nome']
        senha = body['senha']
        db = get_db_connection()
        
        ids = db.execute("SELECT * FROM utilizadores ORDER BY id DESC LIMIT 1").fetchone()

        if ids is None:
            id = 1
        else:
            id = list(db.execute("SELECT * FROM utilizadores ORDER BY id DESC LIMIT 1").fetchone())[0]+1

        row = db.execute("INSERT INTO utilizadores (id, nome, senha) VALUES (?, ?, ?)", (id, nome, senha))
        db.commit()
        db.close()

        if not row:
             return "Fail"
        else:
             return "Success"

@app.route('/artistas', methods=["POST"])
def artistas():
    if request.method == "POST":
        body = request.get_json()

        id_spotify = body['id_spotify']
        nome = body['nome']
        db = get_db_connection()

        todos = list(db.execute("SELECT * FROM artistas").fetchall())
        art = []
        for x in todos:
            art.append(x[1])
        if str(body["id_spotify"]) in art:
            print("Artist already is in DataBase")
            return "Fail"
        else:
            ids = db.execute("SELECT * FROM artistas ORDER BY id DESC LIMIT 1").fetchone()

            if ids is None:
                id = 1
            else:
                id = list(db.execute("SELECT * FROM artistas ORDER BY id DESC LIMIT 1").fetchone())[0]+1
                
            row = db.execute("INSERT INTO artistas (id, id_spotify, nome) VALUES (?, ?, ?)", (id, id_spotify, nome))
            db.commit()
            db.close()

            if not row:
                return "Fail"
            else:
                return "Success"

@app.route('/musicas', methods=["POST"])

def musicas():
    if request.method == "POST":
        body = request.get_json()
        id_spotify = body['id_spotify']
        nome = body['nome']
        id_artista = body['id_artista']
        token = body['token']
        # Ler dados do aluno com id na base de dados
        db = get_db_connection()

        todos = list(db.execute("SELECT * FROM musicas").fetchall())
        art = []
        for x in todos:
            art.append(x[1])
        if str(body["id_spotify"]) in art:
            print("Song already is in DataBase")
            return "Fail"

        else:
            ids = db.execute("SELECT * FROM musicas ORDER BY id DESC LIMIT 1").fetchone()

            if ids is None:
                id = 1
            else:
                id = list(db.execute("SELECT * FROM musicas ORDER BY id DESC LIMIT 1").fetchone())[0]+1
                
            row = db.execute("INSERT INTO musicas (id, id_spotify, nome, id_artista) VALUES (?, ?, ?, ?)", (id, id_spotify, nome, id_artista))
            db.commit()
            db.close()

            artistName =str("https://api.spotify.com/v1/artists/"+id_artista+"")
            spotify = os.popen('curl -X "GET" '+artistName+' -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')
            spot = json.loads(spotify.read())
            dados = {"id_spotify":str(id_artista),"nome":spot["name"]} 
            r = requests.post('http://localhost:5000/artistas', json = dados)

            if not row:
                return "Fail"
            else:
                return "Success"

@app.route('/playlist', methods=["POST"])

def playlist():
    if request.method == "POST":
        body = request.get_json()

        user = body['user']
        musica = body['musica']
        avaliacao = body['avaliacao']

        try:
            db = get_db_connection()

            row = db.execute("INSERT INTO playlists (id_user, id_musica, id_avaliacao) VALUES (?, ?, ?)", (user, musica, avaliacao))
            db.commit()
            db.close()

        except sqlite3.IntegrityError:
            print("Song already is in this users Playlist")
            return "Fail"

        if not row:
            return "Fail"
        else:
            return "Success"


#     elif request.method == "PUT":
#         body = request.get_json()
#         if 'numero' not in body:
#             return {'message': 'numero is required'}, 400
#         elif not isinstance(body['numero'], int):
#             return {'message': 'numero is not an int'}, 400
#         elif 'nome' not in body:
#             return {'message': 'nome is required'}, 400

#         numero = body['numero']
#         nome = body['nome']

#         try:
#             db = get_db_connection()
#             db.execute("INSERT INTO aluno (numero, nome) VALUES (?, ?)", (numero, nome))
#             db.commit()
#             db.close()

#             r = make_response()
#             r.headers['location'] = f'/alunos/{body["numero"]}'
#             return r
#         except sqlite3.IntegrityError:
#             return {'message': 'Erro de integridade'}, 400


# @app.route('/notas', methods=["POST", "GET"])
# def notas():
#     if request.method == "POST":
#         body = request.get_json()

#         if 'numero_aluno' not in body:
#             return {'message': 'numero_aluno is required'}, 400
#         elif not isinstance(body['numero_aluno'], int):
#             return {'message': 'numero_aluno is not an int'}, 400
#         elif 'ano' not in body:
#             return {'message': 'ano is required'}, 400
#         elif 'cadeira' not in body:
#             return {'message': 'cadeira is required'}, 400
#         elif 'nota' not in body:
#             return {'message': 'nota is required'}, 400
#         elif not isinstance(body['nota'], int):
#             return {'message': 'nota is not an int'}, 400

#         numero_aluno = body['numero_aluno']
#         ano = body['ano']
#         cadeira = body['cadeira']
#         nota = body['nota']

#         try:
#             db = get_db_connection()
#             db.execute("INSERT INTO notas (numero_aluno, ano, cadeira, nota) VALUES (?, ?, ?, ?)", (numero_aluno, ano, cadeira, nota))
#             db.commit()
#             db.close()

#             return 201
#         except sqlite3.IntegrityError:
#             return {'message': 'Erro de integridade'}, 400

#     if request.method == "GET":
#         # ler campos no pedido e fazer query de acordo
#         r = make_response(request.data)  # Devolve os dados no pedido
#         return r


if __name__ == '__main__':
    app.run(debug=True)
