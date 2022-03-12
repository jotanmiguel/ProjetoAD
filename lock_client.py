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

cliente = net_client.server_connection(HOST,PORT)

while True:
    comandosSup = ['EXIT', 'LOCK', 'UNLOCK','STATUS','STATS','PRINT'] # lista de comandos suportados

    try:
        inputLinha = input("comando > ")
        args = inputLinha.split()
        comando = args[0].upper()

        if comando in comandosSup:
            if comando == 'EXIT':
                exit()

            elif comando == "LOCK" or comando == "UNLOCK":
                if len(args) < 3:
                    print("NUMERO INSUFICIENTE DE AGRUMENTOS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2])
                    print('Resposta: %s' % resposta)
                    cliente.close()

            elif comando == 'STATUS':
                if len(args) < 3:
                    print("NUMERO INSUFICIENTE DE AGRUMENTOS")
                else:
                    pass

            elif comando =='STATS':
                if args[1].upper() in ['K','N','D']:
                    if len(args) >= 3:
                        print("ARGUMENTOS A MAIS")
                    else:
                        cliente.connect()
                        resposta = cliente.send_receive(args[0] +' '+ args[1])
                        print('Resposta: %s' % resposta)
                        cliente.close()
        else:
            print("COMANDO DESCONHECIDO")



    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()