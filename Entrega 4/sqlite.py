#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Aplicações Distribuídas - Projeto 4 - sqlite.py
Grupo: 2
Números de aluno: 56908, 56954
"""


import sqlite3

from os.path import isfile
def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("CREATE TABLE utilizadores (id INTEGER PRIMARY KEY, nome TEXT, senha TEXT);")
        cursor.execute("CREATE TABLE musicas (id INTEGER PRIMARY KEY,id_spotify TEXT,nome TEXT,id_artista INTEGER,FOREIGN KEY(id_artista) REFERENCES artistas(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE artistas (id INTEGER PRIMARY KEY,id_spotify TEXT,nome TEXT);")
        cursor.execute("CREATE TABLE avaliacoes (id INTEGER PRIMARY KEY,sigla TEXT,designacao TEXT);")
        cursor.execute("CREATE TABLE playlists (id_user INTEGER,id_musica INTEGER,id_avaliacao INTEGER,PRIMARY KEY (id_user, id_musica),FOREIGN KEY(id_user) REFERENCES utilizadores(id) ON DELETE CASCADE,FOREIGN KEY(id_musica) REFERENCES musicas(id) ON DELETE CASCADE,FOREIGN KEY(id_avaliacao) REFERENCES avaliacoes(id) ON DELETE CASCADE);")
        aval = [(1, "M", "Medíocre"),(2, "m", "Mau"),(3, "S", "Suficiente"),(4, "B", "Boa"),(5, "MB", "Muito Boa")]
        cursor.executemany("INSERT INTO avaliacoes (id, sigla, designacao) VALUES(?,?,?)",aval)
        connection.commit()
    return connection, cursor


if __name__ == '__main__':
    conn, cursor = connect_db('BD.db')


    conn.close()