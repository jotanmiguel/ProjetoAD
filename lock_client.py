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

if len(sys.argv) > 2 and sys.argv[2] == 'localhost':
    HOST = '127.0.0.1'
    PORT = int(sys.argv[3])
    ID = sys.argv[1]
elif len(sys.argv) > 2:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    ID = sys.argv[1]
elif len(sys.argv) == 2:
    HOST = '127.0.0.1'
    PORT = 9999
    ID = sys.argv[1]
else:
    print("MISSING CLIENT ID")
    exit()

cliente = net_client.server_connection(HOST,PORT)

while True:
    comandosSup = ['EXIT','LOCK','UNLOCK','STATUS','STATS','PRINT','SLEEP']

    try:
        inputLinha = input("Comando: ")
        args = inputLinha.split()
        comando = args[0].upper()

        if comando in comandosSup:
            if comando == 'EXIT':
                exit()

            elif comando == 'SLEEP':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                else:
                    time.sleep(int(args[1]))

            elif comando == "LOCK":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2]+' '+ ID +' '+args[3])
                    print('Resposta: %s' % resposta)
                    cliente.close()

            elif comando == "UNLOCK":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2]+' '+ ID)
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

            elif comando == 'STATS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif args[1].upper() in ['K','N','D']:
                    if args[1].upper() == 'K':
                            if len(args) < 3:
                                print("MISSING ARGUMENTS")
                            else:
                                cliente.connect()
                                resposta = cliente.send_receive(args[0] +' '+ args[1] +' '+ args[2])
                                print('Resposta: %s' % resposta)
                                cliente.close()
                    else:
                            if len(args) < 2:
                                print("MISSING ARGUMENTS")
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