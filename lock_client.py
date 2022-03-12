#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports

import sys
import socket as s
import net_client

# Programa principal

if len(sys.argv) > 1 and sys.argv[1] == 'localhost':
    HOST = '127.0.0.1'
    PORT = sys.argv[2]
elif len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = sys.argv[2]
else:
    HOST = '127.0.0.1'
    PORT = 9999

while True:
    comandosSup = ['EXIT', 'LOCK', 'RELEASE'] # lista de comandos suportados


    try:
        inputLinha = input("comando > ") # l
        args = inputLinha.split()
        comando = args[0].upper()



    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()