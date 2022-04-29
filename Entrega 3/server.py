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
@app.route('/utilizadores/<int:numero>', methods=["GET"])
def utilizadores(numero = None):
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
    elif request.method == "GET":
        db = get_db_connection()
        row = db.execute('SELECT * FROM utilizadores WHERE id = ?', (numero,)).fetchone()
        db.close()

        if not row:
            return {}, 404
        else:
            print(dict(row))
            return {'data': dict(row)}, 200


@app.route('/artistas', methods=["POST"])
@app.route('/artistas/<id_artista>', methods=["GET"])
def artistas(id_artista = None):
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
    elif request.method == "GET":
        db = get_db_connection()
        row = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_artista,)).fetchone()
        db.close()

        if not row:
            return {}, 404
        else:
            print(dict(row))
            return {'data': dict(row)}, 200
        

@app.route('/musicas', methods=["POST"])
@app.route('/musicas/<id_musica>', methods=["GET"])

def musicas(id_musica = None):
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

    elif request.method == "GET":
        db = get_db_connection()
        row = db.execute('SELECT * FROM musicas WHERE id_spotify = ?', (id_musica,)).fetchone()
        db.close()

        if not row:
            return {}, 404
        else:
            print(dict(row))
            return {'data': dict(row)}, 200

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

@app.route('/', methods=["GET"])

def index():
    if request.method == "GET":
        
        body = request.get_json()
        tipo = body["tipo"].lower()
        db = get_db_connection()
        row = list(db.execute('SELECT * FROM '+tipo+'').fetchall())
        db.close()


        if not row:
            return {}, 404
        else:
            final = {}
            for x in row:
                final[row.index(x)] = dict(x)
            return final, 200






if __name__ == '__main__':
    app.run(debug=True)
