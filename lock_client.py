#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo: 2
Números de aluno: 56908, 56954
"""
# Zona para fazer imports

import sys
import socket as s
import net_client
import time

# Programa principal

if len(sys.argv) > 1 and sys.argv[2] == 'localhost':
    HOST = '127.0.0.1'
    PORT = int(sys.argv[3])
elif len(sys.argv) > 1:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
else:
    HOST = '127.0.0.1'
    PORT = 9999

cliente = net_client.server_connection(HOST,PORT)
clientid = sys.argv[1]

while True:
    comandosSup = ['EXIT','LOCK','UNLOCK','STATUS','STATS','PRINT','SLEEP'] # lista de comandos suportados

    try:
        inputLinha = input("Comando: ")
        args = inputLinha.split()
        comando = args[0].upper()

        if comando in comandosSup:
            if comando == 'EXIT':
                exit()

            elif comando == 'SLEEP':
                time.sleep(args[1])

            elif comando == "LOCK":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ clientid+' '+ args[2]+' '+args[3])
                    print('Resposta: %s' % resposta)
                    cliente.close()

            elif comando == "UNLOCK":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2]+' '+ clientid)
                    print('Resposta: %s' % resposta)
                    cliente.close()

            elif comando == 'STATUS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1])
                    print('Resposta: %s' % resposta)
                    cliente.close()

            elif comando =='STATS':
                if args[1].upper() in ['K','N','D']:
                    if args[1].upper() == 'K':
                            cliente.connect()
                            resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2])
                            print('Resposta: %s' % resposta)
                            cliente.close()
                    else:
                            cliente.connect()
                            resposta = cliente.send_receive(args[0] +' '+ args[1])
                            print('Resposta: %s' % resposta)
                            cliente.close()

            elif comando == "PRINT":
                    cliente.connect()
                    resposta = cliente.send_receive(args[0])
                    print('Resposta: %s' % resposta)
                    cliente.close()
                
        else:
            print("UNKNOWN COMMAND")



    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()