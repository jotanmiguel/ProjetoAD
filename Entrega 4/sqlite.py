#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - sqlite.py
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
        cursor.execute("CREATE TABLE weather (id INTEGER PRIMARY KEY, date TEXT, location TEXT, condition TEXT, mintemp_c INTEGER, maxtemp_c INTEGER, FOREIGN KEY(location) REFERENCES locations(wea_name) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE roundtrips (id TEXT PRIMARY KEY,cost INTEGER,id_leg0 TEXT,id_leg1 TEXT,FOREIGN KEY(id_leg0) REFERENCES legs(id) ON DELETE CASCADE, FOREIGN KEY(id_leg1) REFERENCES legs(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE legs (id TEXT PRIMARY KEY, dep_IATA TEXT, arr_IATA TEXT, dep_datetime TEXT, arr_datetime TEXT, duration_min INTEGER, airlineCodes TEXT NULL, FOREIGN KEY (airlineCodes) REFERENCES airline(code), FOREIGN KEY (dep_IATA) REFERENCES locations(IATA), FOREIGN KEY (arr_IATA) REFERENCES locations(IATA));")
        cursor.execute("CREATE TABLE airlines (code TEXT PRIMARY KEY,sigla TEXT);")
        cursor.execute("CREATE TABLE locations (id INTEGER PRIMARY KEY, name TEXT UNIQUE, IATA TEXT UNIQUE, wea_name TEXT UNIQUE);")
        cursor.execute("CREATE TABLE search_trips (search_id INTEGER PRIMARY KEY, trip_ids TEXT, FOREIGN KEY (search_id) REFERENCES searches(search_id))")
        cursor.execute("CREATE TABLE searches (search_id INTEGER PRIMARY KEY, client_id TEXT, search_params TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);")
        airlines = [('EI', 'Aer Lingus'), ('JU', 'Air Serbia'), ('OS', 'Austrian Airlines'), ('SN', 'Brussels Airlines'), ('U2', 'EasyJet'), ('EC', 'easyJet Europe'), ('EW', 'Eurowings'), ('IB', 'Iberia'), ('I2', 'Iberia Express'), ('LH', 'Lufthansa'), ('CL', 'Lufthansa CityLine'), ('AL', 'Malta Air'), ('NI', 'Portugália Airlines'), ('FR', 'Ryanair'), ('TP', 'TAP Air Portugal'), ('X3', 'TUIfly'), ('VY', 'Vueling Airlines'), ('W6', 'Wizz Air'), ('W9', 'Wizz Air UK')]
        locations = [ (1, 'Amsterdam', 'AMS', 'Amsterdam'), (2, 'Berlin', 'BER', 'Berlin'), (3, 'Brussels', 'BRU', 'Brussels'), (4, 'Dublin', 'DUB', 'Dublin'), (5, 'Rome', 'FCO', 'Rome'), (6, 'Ljubljana', 'LJU', 'Ljubljana'), (7, 'Madrid', 'MAD', 'Madrid'), (8, 'Paris Orly', 'ORY', 'Paris'), (9, 'Vienna', 'VIE', 'Vienna'), (10, 'Lisbon', 'LIS', 'Lisbon' )]
        cursor.executemany("INSERT INTO airlines VALUES (?,?)", airlines)
        cursor.executemany("INSERT INTO locations VALUES (?,?,?,?)", locations)
        connection.commit()
    return connection, cursor


if __name__ == '__main__':
    conn, cursor = connect_db('BD.db')
    conn.close()