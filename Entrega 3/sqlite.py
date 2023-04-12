#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - sqlite.py
Grupo: 33
Números de aluno: 56908, 56916
"""

import sqlite3

from os.path import isfile
def connect_db(dbname: str):
    """
    Connects to the database.

    Args:
        dbname (str): name of the database file.

    Returns:
       any : connection and cursor to the database.
    """
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("CREATE TABLE weather (id INTEGER PRIMARY KEY, date TEXT, location TEXT, FOREIGN KEY(location) REFERENCES locations(wea_name) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE roundtrips (id INTEGER PRIMARY KEY,cost INTEGER,id_leg0 INTEGER,id_leg1 INTEGER,FOREIGN KEY(id_leg0) REFERENCES legs(id) ON DELETE CASCADE, FOREIGN KEY(id_leg1) REFERENCES legs(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE legs (id INTEGER PRIMARY KEY, dep_IATA TEXT, arr_IATA TEXT, dep_datetime TEXT, arr_datetime TEXT, duration_min INTEGER, airlineCodes TEXT NULL, FOREIGN KEY (airlineCodes) REFERENCES airline(code), FOREIGN KEY (dep_IATA) REFERENCES locations(IATA), FOREIGN KEY (arr_IATA) REFERENCES locations(IATA));")
        cursor.execute("CREATE TABLE airlines (id INTEGER PRIMARY KEY,sigla TEXT,designacao TEXT);")
        cursor.execute("CREATE TABLE locations (id INTEGER PRIMARY KEY, name TEXT UNIQUE, IATA TEXT UNIQUE, wea_name TEXT UNIQUE);")
        airlines = [(1, "TAP", "Companhia aérea baseada em portugal"), (2, "KLM", "Companhia aérea baseada na Holanda"), (3, "Lufthansa", "Companhia aérea baseada na Alemanha"), (4, "Air France", "Companhia aérea baseada em França"), (5, "British Airways", "Companhia aérea baseada no Reino Unido"), (6, "Iberia", "Companhia aérea baseada em Espanha"), (7, "Alitalia", "Companhia aérea baseada em Itália"), (8, "Air Europa", "Companhia aérea baseada em Espanha"), (9, "Ryanair", "Companhia aérea baseada na Irlanda"), (10, "Easyjet", "Companhia aérea baseada no Reino Unido")]
        locations = [(1, "Lisboa", "LIS", "portela"), (2, "Madrid", "MAD", "barajas"), (3, "Paris", "CDG", "charles de gaulle"), (4, "Londres", "LHR", "heathrow"), (5, "Roma", "FCO", "fiumicino"), (6, "Amesterdão", "AMS", "schiphol"), (7, "Berlim", "TXL", "tegel"), (8, "Barcelona", "BCN", "el prat"), (9, "Milão", "MXP", "malpensa"), (10, "Dublin", "DUB", "dublin" )]
        cursor.executemany("INSERT INTO airlines VALUES (?,?,?)", airlines)
        cursor.executemany("INSERT INTO locations VALUES (?,?,?,?)", locations)
        connection.commit()
    return connection, cursor


if __name__ == '__main__':
    conn, cursor = connect_db('BD.db')
    conn.close()