#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - cliente.py
Grupo: 33
Números de aluno: 56908, 56916
"""

import requests
import json
import os

# while True:
comandosSup = ['SEARCH', 'FILTER', 'DETAILS']
inputUser = input("Introduza o comando: ")
args = inputUser.split()
op = args[0].upper()
URL = 'http://localhost:5000'

tokenVoos = "6436cbfb1418ec0f60b11ade"
tokenTempo = "fda1c4c770e842d197b140037231204"

if op in comandosSup:
    if op == "SEARCH":
        dados = {
            'location': args[1], 
            'cost': args[2]
            }
        r = requests.get(URL + '/search', json=json.dumps(dados), headers={'Content-type': 'application/json'})
        print(r.content.decode())
    # elif op == "FILTER":
    #     if args[1] == "DIVERSIFY":
    #         dados = {
    #             'roundtrips': list(args[2])
    #             }
    #         r = requests.get(URL + '/filter/diversify', json=json.dumps(dados), headers={'Content-type': 'application/json'})
    #         print(r.content.decode())
    elif op == "DETAILS":
        dados = {
            'trip_ids': args[1], 
        }
        r = requests.get(URL + '/search', json=json.dumps(dados), headers={'Content-type': 'application/json'})
        print(r.content.decode())
else:
    print("UNKNOWN-COMMAND")
    
# import requests
# import json

# BASE_URL = "http://localhost:5000"

# def search(location, cost):
#     response = requests.get(f"{BASE_URL}/search", params={"location": location, "cost": cost})
    
#     if response.status_code == 200:
#         viagens = response.json()
#         print("Viagens encontradas:")
#         for viagem in viagens:
#             print(viagem)
#     else:
#         print("Erro ao buscar viagens")

# def filter(viagem_ids, location=None, airline=None, sun=None):
#     data = {
#         "viagem_ids": viagem_ids,
#         "location": location,
#         "airline": airline,
#         "sun": sun
#     }
#     response = requests.post(f"{BASE_URL}/filter", json=data)
    
#     if response.status_code == 200:
#         viagens_filtradas = response.json()
#         print("Viagens filtradas:")
#         for viagem in viagens_filtradas:
#             print(viagem)
#     else:
#         print("Erro ao filtrar viagens")

# def details(viagem_id):
#     response = requests.get(f"{BASE_URL}/details", params={"viagem_id": viagem_id})
    
#     if response.status_code == 200:
#         viagem_details = response.json()
#         print("Detalhes da viagem:")
#         print(viagem_details)
#     else:
#         print("Erro ao buscar detalhes da viagem")

# def main():
#     while True:
#         print("Operações disponíveis: SEARCH, FILTER, DETAILS, EXIT")
#         op = input("Escolha uma operação: ")
        
#         if op.upper() == "SEARCH":
#             location = input("Informe a localização: ")
#             cost = float(input("Informe o custo máximo: "))
#             search(location, cost)
#         elif op.upper() == "FILTER":
#             viagem_ids = input("Informe os IDs das viagens separados por vírgula: ").split(',')
#             location = input("Informe a localização (opcional, pressione Enter para pular): ")
#             airline = input("Informe o código da companhia aérea (opcional, pressione Enter para pular): ")
#             sun = input("Informe a quantidade de dias de sol (opcional, pressione Enter para pular): ")
#             sun = int(sun) if sun else None
#             filter(viagem_ids, location, airline, sun)
#         elif op.upper() == "DETAILS":
#             viagem_id = input("Informe o ID da viagem: ")
#             details(viagem_id)
#         elif op.upper() == "EXIT":
#             break
#         else:
#             print("Operação inválida. Tente novamente.")

# if __name__ == '__main__':
#     main()