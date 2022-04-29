import sqlite3
from os.path import isfile
def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()

    if not db_is_created:
        cursor.execute("CREATE TABLE utilizadores (id INTEGER PRIMARY KEY, nome TEXT, senha TEXT);")
        connection.commit()
    return connection, cursor

um_registo = (131, '2021/2022', 'AD')


if __name__ == '__main__':
    conn, cursor = connect_db('BD.db')

    cursor.execute('INSERT INTO utilizadores VALUES (?, ?, ?)', um_registo)
    conn.commit()

    cursor.execute('SELECT * FROM utilizadores') # Fazer query e obter todos
    todos = cursor.fetchall() # os resultados
    print ("Todos: ", todos)

    conn.close()