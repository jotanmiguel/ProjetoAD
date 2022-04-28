"""
Aplicações distribuídas - Projeto 3 - server.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import json, sqlite3
from flask import Flask, request, make_response, g
from os.path import isfile

from isort import file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def root():
    # query = 'SELECT * FROM utilizadores;'
    query1 = 'SELECT * FROM musicas;'
    query2 = 'SELECT * FROM playlists;'
    query3 = 'SELECT * FROM artistas;'
    query4 = 'SELECT * FROM avaliacoes;'

    cursor = g.db.cursor()
    
    # cursor.execute(query)
    # cenas = cursor.fetchall()
    # print("utilizadores: " + cenas)

    cursor.execute(query1)
    cenas = cursor.fetchall()
    print("musicas: " + cenas)

    cursor.execute(query2)
    cenas = cursor.fetchall()
    print("playlists: " + cenas)

    cursor.execute(query3)
    cenas = cursor.fetchall()
    print("artistas: " + cenas)

    cursor.execute(query4)
    cenas = cursor.fetchall()
    print("avaliacoes: " + cenas)
    
    return 'OK'    

@app.route('/utilizadores', methods=['GET', 'POST', 'PUT', 'DELETE'])
def utilizadores():
    pass

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def artistas():
    pass

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def musicas():
    pass

@app.before_request
def before_request():
    g.db = sqlite3.connect('teste.db')


@app.teardown_request
def teardown_request(exception):
    g.db.close()

def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    print(db_is_created)
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        f = file('BD.sql','r')
        print(f.readlines())
        for linha in f.readlines():
            cursor.execute(linha)
            connection.commit()
    return connection, cursor


if __name__ =='__main__':
    db, cursor = connect_db('teste.db')
    #app.run()
    app.run(debug=True)