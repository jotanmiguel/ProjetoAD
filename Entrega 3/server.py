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
@app.route('/utilizadores/<int:numero>', methods=["GET","DELETE","PUT"])
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

        if not row:
             return {}, 404
        else:
            db.close()
            return "Success", 200

    elif request.method == "GET":
        db = get_db_connection()
        try:
            row = list(db.execute('SELECT * FROM utilizadores WHERE id = ?', (numero,)).fetchone())
            db.close()
            print(row)
        except TypeError:
            return "There is no such user", 404

        if not row:
            return {}, 404
        else:
            
            return {'data': row}, 200

    elif request.method == "DELETE":
        db = get_db_connection()

        try:
            l = list(db.execute('SELECT * FROM utilizadores WHERE id = ?', (numero,)).fetchone())            
            row = db.execute('DELETE FROM utilizadores WHERE id = ?', (numero,))
            db.commit()
            db.close()
        except TypeError:
            return "There is no such user", 404

        if not row:
            return {}, 404
        else:
            
            return "Success", 200

    elif request.method == "PUT":
        body = request.get_json()

        id_user = body['id_user']
        password = body['password']
        db = get_db_connection()

        try:
            l = list(db.execute('SELECT * FROM utilizadores WHERE id = ?', (numero,)).fetchone()) 
            row = db.execute("UPDATE utilizadores SET senha=? WHERE id = ? ", (password,id_user))
            db.commit()
            db.close()
        except TypeError:
            return "There is no such user", 404

        if not row:
            return {}, 404
        else:
            
            return "Success", 200



@app.route('/artistas', methods=["POST"])
@app.route('/artistas/<id_artista>', methods=["GET","DELETE"])
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
            return {}, 404
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
                return {}, 404
            else:
                
                return "Success", 200

    elif request.method == "GET":
        db = get_db_connection()

        try:
            l = list(db.execute('SELECT * FROM artistas WHERE id = ?', (id_artista,)).fetchone())
            row = db.execute('SELECT * FROM artistas WHERE id = ?', (id_artista,)).fetchone()            
            db.close()
            print(row)
        except TypeError:
            return "There is no such artist", 404

        if not row:
            return {}, 404
        else:
            
            return {'data': dict(row)}, 200

    elif request.method == "DELETE":
        db = get_db_connection()

        try:
            l = list(db.execute('SELECT * FROM artistas WHERE id = ?', (id_artista,)).fetchone())
            row = db.execute('DELETE FROM artistas WHERE id = ?', (id_artista,))
            db.commit()
            db.close()
        except TypeError:
            return "There is no such artist", 404       


        if not row:
            return {}, 404
        else:
            
            return "Success", 200

        

@app.route('/musicas', methods=["POST"])
@app.route('/musicas/<id_musica>', methods=["GET","DELETE"])

def musicas(id_musica = None):
    if request.method == "POST":
        body = request.get_json()
        id_spotify = body['id_spotify']
        nome = body['nome']
        id_artista = body['id_artista']
        token = body['token']
        db = get_db_connection()

        todos = list(db.execute("SELECT * FROM musicas").fetchall())
        art = []
        for x in todos:
            art.append(x[1])
        if str(body["id_spotify"]) in art:
            print("Song already is in DataBase")
            return {}, 404

        else:
            ids = db.execute("SELECT * FROM musicas ORDER BY id DESC LIMIT 1").fetchone()

            if ids is None:
                id = 1
            else:
                id = list(db.execute("SELECT * FROM musicas ORDER BY id DESC LIMIT 1").fetchone())[0]+1
                
            row = db.execute("INSERT INTO musicas (id, id_spotify, nome, id_artista) VALUES (?, ?, ?, ?)", (id, id_spotify, nome, id_artista))
            db.commit()

            todos = list(db.execute("SELECT * FROM artistas").fetchall())
            db.close()

            art = []
            for x in todos:
                art.append(x[1])
            if str(body["id_artista"]) in art:
                print("Artist already is in DataBase")
            else:
                artistName =str("https://api.spotify.com/v1/artists/"+id_artista+"")
                spotify = os.popen('curl -X "GET" '+artistName+' -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')
                spot = json.loads(spotify.read())
                dados = {"id_spotify":str(id_artista),"nome":spot["name"]} 
                r = requests.post('http://localhost:5000/artistas', json = dados)

            if not row:
                return {}, 404
            else:
                
                return "Success", 200

    elif request.method == "GET":
        db = get_db_connection()
        try:
            l = list(db.execute('SELECT * FROM musicas WHERE id = ?', (id_musica,)).fetchone())
            row = db.execute('SELECT * FROM musicas WHERE id = ?', (id_musica,)).fetchone()            
            db.close()
        except TypeError:
            return "There is no such song", 404

        if not row:
            return {}, 404
        else:
            
            return {'data': dict(row)}, 200

    elif request.method == "DELETE":
        db = get_db_connection()
        try:
            l = list(db.execute('SELECT * FROM musicas WHERE id = ?', (id_musica,)).fetchone())
            row = db.execute('DELETE FROM musicas WHERE id = ?', (id_musica,))
            db.commit()
            db.close()

        except TypeError:
            return "There is no such artist", 404   

        if not row:
            return {}, 404
        else:
            
            return "Success", 200

@app.route('/playlist', methods=["POST","PUT"])

def playlist():
    if request.method == "POST":
        body = request.get_json()

        user = body['user']
        musica = body['musica']
        avaliacao = body['avaliacao']

        db = get_db_connection()
        todos = list(db.execute("SELECT * FROM musicas").fetchall())
        art = []

        for x in todos:
            art.append(x[0])
        if int(musica) not in art:
            print(art)
            print("Song is not in DataBase")
            return "Song is not in DataBase", 404

        try:

            row = db.execute("INSERT INTO playlists (id_user, id_musica, id_avaliacao) VALUES (?, ?, ?)", (user, musica, avaliacao))
            db.commit()
            db.close()

        except sqlite3.IntegrityError:
            print("Song already is in this users Playlist")
            return {}, 404

        if not row:
            return {}, 404
        else:
            
            return "Success", 200

    elif request.method == "PUT":

        body = request.get_json()

        id_user = body['id_user']
        id_musica = body['id_musica']
        avaliacao = body['avaliacao']

        db = get_db_connection()
        todos = list(db.execute("SELECT * FROM musicas").fetchall())
        art = []

        for x in todos:
            art.append(x[0])
        if int(id_musica) not in art:
            print(art)
            print(id_musica)
            print("Song is not in DataBase")
            return "Song is not in DataBase", 404
        
        row = db.execute("UPDATE playlists SET id_avaliacao = "+avaliacao+" WHERE id_user = "+id_user+" AND id_musica = "+id_musica+"")
        db.commit()
        db.close()

        if not row:
            return {}, 404
        else:
            
            return "Success", 200
        
        



@app.route('/', methods=["GET","DELETE"])

def index():
    if request.method == "GET":

        
        body = request.get_json()
        if len(body) < 2:
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
        elif body["tipo"].upper() == "MUSICAS_A":
            artista = body["extra"]
            db = get_db_connection()
            try:
                id_spot = db.execute('SELECT * FROM artistas WHERE id = ?', (artista,)).fetchone()[1]

            except TypeError:
                return "There is no such artist", 404 

            row = list(db.execute('SELECT * FROM musicas WHERE id_artista = ?', (id_spot,)).fetchall())
            final = []
            songs = []
            for x in row:
                final.append(dict(x)["id"])
                songs.append(dict(x))

            aval = list(db.execute('SELECT * FROM playlists').fetchall())

            dictAval = {}
            count = 0
            for x in aval:
                if dict(x)["id_musica"] in final:
                    dictAval[aval.index(x)] = songs[final.index(dict(x)["id_musica"])]
            db.close()
            if not row:
                return {}, 404
            else:

                return dictAval, 200

        elif body["tipo"].upper() == "MUSICAS_U":

            user = body["extra"]
            db = get_db_connection()
            row = list(db.execute('SELECT * FROM playlists WHERE id_user = ?', (user,)).fetchall())
            db.close()


            if not row:
                return {}, 404
            else:
                final = {}
                for x in row:
                    final[row.index(x)] = dict(x)
                return final, 200
        elif body["tipo"].upper() == "MUSICAS":
            aval = body["extra"]
            db = get_db_connection()
            row = list(db.execute('SELECT * FROM playlists WHERE id_avaliacao = ?', (aval,)).fetchall())
            db.close()


            if not row:
                return {}, 404
            else:
                final = {}
                for x in row:
                    final[row.index(x)] = dict(x)
                return final, 200

    elif request.method == "DELETE":

        body = request.get_json()
        if len(body) < 2:
            tipo = body["tipo"].lower()
            db = get_db_connection()
            row = db.execute('DELETE FROM '+tipo+'')
            db.commit()
            db.close()


            if not row:
                return {}, 404
            else:
                return "Success", 200

        elif body["tipo"].upper() == "MUSICAS_A":
            artista = body["extra"]
            db = get_db_connection()

            try:
                id_spot = db.execute('SELECT * FROM artistas WHERE id = ?', (artista,)).fetchone()[1]

            except TypeError:
                return "There is no such artist", 404 

            row = list(db.execute('SELECT * FROM musicas WHERE id_artista = ?', (id_spot,)).fetchall())
            final = []
            songs = []
            for x in row:
                final.append(dict(x)["id"])
                songs.append(dict(x))
            aval = list(db.execute('SELECT * FROM playlists').fetchall())

            dictAval = []
            count = 0
            for x in aval:
                if dict(x)["id_musica"] in final:
                    dictAval.append(final[final.index(dict(x)["id_musica"])])
            for y in dictAval:
                delAval = db.execute('DELETE FROM playlists WHERE id_musica = ?', (y,))
                db.commit()
                if not delAval:
                    return {}, 404
            db.close()
            return "Success", 200
        elif body["tipo"].upper() == "MUSICAS_U":

            user = body["extra"]
            db = get_db_connection()
            row = db.execute('DELETE FROM playlists WHERE id_user = ?', (user,))
            db.commit()
            db.close()


            if not row:
                return {}, 404
            else:
                return "Success", 200

        elif body["tipo"].upper() == "MUSICAS":
            aval = body["extra"]
            db = get_db_connection()
            row = db.execute('DELETE FROM playlists WHERE id_avaliacao = ?', (aval,))
            db.commit()
            db.close()


            if not row:
                return {}, 404
            else:

                return "Success", 200




if __name__ == '__main__':
    app.run(debug=True)
