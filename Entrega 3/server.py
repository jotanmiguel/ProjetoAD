from multiprocessing import connection
from webbrowser import get
from colorama import Cursor
from flask import Flask, request, make_response, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('BD.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

@app.route('/', methods=["GET"])
def root():
    db, cursor = get_db_connection()

    cursor.execute('SELECT * FROM utilizadores')
    cursor.fetchall()

    print(cursor)
    db.close()

    return "OK"

@app.route('/utilizadores/<int:numero>', methods=["GET"])
def utilizadores(numero=None):
    if request.method == "GET":
        # Ler dados do aluno com id na base de dados
        connection, Cursor = get_db_connection()
        row = connection.execute('SELECT * FROM utilizadores WHERE id = ' + str(numero) + '').fetchone()
        connection.close()

        if not row:
            return "NOT FOUND", 404
        else:
            return {'data': dict(row)}, 200

@app.route('/avaliacoes/<int:numero>', methods=["GET"])
def avaliacoes(numero=None):
    if request.method == "GET":
        # Ler dados do aluno com id na base de dados
        connection, Cursor = get_db_connection()
        row = connection.execute('SELECT * FROM avaliacoes WHERE id = ' + str(numero) + '').fetchone()
        connection.close()

        if not row:
            return "NOT FOUND", 404
        else:
            return {'data': dict(row)}, 200

if __name__ == '__main__':
    app.run(debug=True)