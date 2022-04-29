import sqlite3
from os.path import isfile
def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()

    if not db_is_created:
        cursor.execute("CREATE TABLE utilizadores (id INTEGER PRIMARY KEY, nome TEXT, senha TEXT);")
        connection.commit()

        cursor.execute("CREATE TABLE musicas (id INTEGER PRIMARY KEY, id_spotify TEXT, nome TEXT, id_artista INTEGER, FOREIGN KEY (id_artista) REFERENCES artistas(id) ON DELETE CASCADE);")
        connection.commit()
        
        cursor.execute("CREATE TABLE artistas (id INTEGER PRIMARY KEY, id_spotify TEXT, nome TEXT);")
        connection.commit()
        
        cursor.execute("CREATE TABLE avaliacoes (id INTEGER PRIMARY KEY, sigla TEXT, designacao TEXT);")
        connection.commit()

        cursor.execute("CREATE TABLE playlists (id_user INTEGER, id_musica INTEGER, id_avaliacao INTEGER, PRIMARY KEY (id_user, id_musica), FOREIGN KEY (id_user) REFERENCES utilizadores(id) ON DELETE CASCADE, FOREIGN KEY (id_musica) REFERENCES musicas(id) ON DELETE CASCADE, FOREIGN KEY (id_avaliacao) REFERENCES avaliacoes(id) ON DELETE CASCADE);")
        connection.commit()
    return connection, cursor

varios = [(131, 'Joao', '123'), (132, 'Miguel', '123'), (133, 'Pedro', '123'), (134, 'Daniel', '123')]
varios1 = [(1, 'M', 'Mediocre'), (2, 'm', 'Mau'), (3, 'S', 'Suficiente'), (4, 'B', 'Boa'), (5, 'MB', 'Muito Boa')]

if __name__ == '__main__':
    conn, cursor = connect_db('BD.db')

    for registo in varios:
        cursor.execute('INSERT INTO utilizadores VALUES (?, ?, ?)', registo)
        conn.commit()

    for registo in varios1:
        cursor.execute('INSERT INTO avaliacoes VALUES (?, ?, ?)', registo)
        conn.commit()

    conn.close()