#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - cliente.py
Grupo: 33
Números de aluno: 56908, 56916
"""

import requests
import json
from kazoo.client import KazooClient
from google_auth_oauthlib.flow import InstalledAppFlow


# Conectar-se ao servidor ZooKeeper
zk = KazooClient(hosts='localhost:2181')
zk.start()

# Registrar o cliente no ZooKeeper
zk.create('/clients/client1', ephemeral=True)

BASE_URL = "http://localhost:5000"

def search(location, cost):
    data = {
        'location': location,
        'cost': cost
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{BASE_URL}/search", params=data, headers=headers, verify='root.pem',cert=('cli.crt','cli.key'))
    
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print("Erro ao buscar viagens")

def details(trip_id):
    data = {
        'trip_id': trip_id
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{BASE_URL}/details", params=data, headers=headers, verify='root.pem',cert=('cli.crt','cli.key'))
    
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print("Erro ao buscar detalhes da viagem")

def filter(location, airline, days_of_sun):
    data = {
        'location': location,
        'airline': airline,
        'days_of_sun': days_of_sun
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{BASE_URL}/filter", params=data, headers=headers, verify='root.pem',cert=('cli.crt','cli.key'))
    
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print("Erro ao filtrar viagens")

def filter_diversify(trip_ids):
    data = {
        'trip_ids': trip_ids,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{BASE_URL}/filter", params=data, headers=headers)
    
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print("Erro ao filtrar viagens")

def main():
    while True:
        print("Operações disponíveis: SEARCH, FILTER, DETAILS, EXIT")
        op = input("> ").split(' ')
        
        if op[0].upper() == "SEARCH" and len(op) == 3:
            location = op[1].capitalize()
            cost = int(op[2])
            search(location, cost)
        elif op[0] == "FILTER":
            if op[0] == "DIVERSiFY" and len(op) == 3:
                trip_ids = op[1].split(',')
                filter_diversify(trip_ids)
            elif op[0] == "FILTER" and len(op) == 4:
                location = op[1].capitalize()
                airline = op[2].upper()
                days_of_sun = int(op[3])
                filter(location, airline, days_of_sun)
        elif op[0] == "DETAILS" and len(op) == 2:
            trip_id = op[1]
            details(trip_id)
        elif op[0] == "EXIT":
            break
        else:
            print("Operação inválida. Tente novamente.")
    zk.stop()
    zk.close()

if __name__ == '__main__':
    main()
