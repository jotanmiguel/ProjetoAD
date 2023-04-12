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
    elif op == "FILTER":
        if args[1] == "DIVERSIFY":
            dados = {
                'roundtrips': list(args[2])
                }
            r = requests.get(URL + '/filter/diversify', json=json.dumps(dados), headers={'Content-type': 'application/json'})
            print(r.content.decode())
    elif op == "DETAILS":
        pass
else:
    print("UNKNOWN-COMMAND")