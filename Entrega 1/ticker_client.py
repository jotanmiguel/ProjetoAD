#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 33
Números de aluno: 56908, 56916
"""
# Zona para fazer imports

import sys
import socket as s
import time
import re
import net_client

#programa principal
    
def is_valid_ip_address(ip):
    """
    Método para verificar se um ip está no formato correto.

    Args:
        ip (str): ip a ser verificado.

    Returns:
        bool: True se válido, False se inválido.
    """
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return True if re.match(pattern, ip) else False
                 
if len(sys.argv) < 4:
    print("MISSING-ARGUMENTS")
    exit()
else:
    ID = int(sys.argv[1])
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
if type(ID) is not int:
    print("UNKNOWN-COMMAND")
    exit()
if HOST == "localhost":
    HOST = "127.0.0.1"
if (HOST != "localhost" and not is_valid_ip_address(HOST)):
    print("UNKNOWN-COMMAND")
    exit()
if type(PORT) is not int:
    print("UNKNOWN-COMMAND")
    exit()
    
cliente = net_client.server_connection(HOST,PORT)
print(f'Connected to {HOST}:{cliente.port}')

while True:
    comandosSup = ['SUBSCR','CANCEL','STATUS','INFOS','STATIS', 'SLEEP', 'EXIT']

    try:
        inputLinha = input("Comando > ")
        args = inputLinha.split()
        comando = args[0].upper()

        if comando in comandosSup:
            if comando == 'EXIT':
                exit()

            elif comando == 'SLEEP':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif len(args) > 3:
                    print("UNKNOWN COMMAND")
                else:
                    time.sleep(int(args[1]))
            elif comando == "SUBSCR":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                elif len(args) > 4:
                    print("UNKNOWN COMMAND")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(comando +' '+ args[1] +' '+ args[2]+' '+ str(ID))
                    print('Resposta: %s' % resposta.decode())
                    cliente.close()

            elif comando == "CANCEL":
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif len(args) > 3:
                    print("UNKNOWN COMMAND")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(comando +' '+ args[1] +' '+ str(ID))
                    print('Resposta: %s' % resposta.decode())
                    cliente.close()

            elif comando == 'STATUS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif len(args) > 3:
                    print("UNKNOWN COMMAND")
                else:
                    cliente.connect()
                    resposta = cliente.send_receive(comando +' '+ args[1] +' '+ str(ID))
                    print('Resposta: %s' % resposta.decode())
                    cliente.close()
                    
            elif comando == 'INFOS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif len(args) > 3:
                    print("UNKNOWN COMMAND")
                elif args[1].upper() in ['M','K']:
                    cliente.connect()
                    resposta = cliente.send_receive(comando +' '+ args[1].upper()+' '+ str(ID))
                    print('Resposta: %s' % resposta.decode())
                    cliente.close()

            elif comando == 'STATIS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif args[1].upper() in ['L','ALL']:
                    if args[1].upper() == 'L':
                        if len(args) < 3:
                            print("MISSING ARGUMENTS")
                        elif len(args) > 4:
                            print("UNKNOWN COMMAND")
                        else:
                            cliente.connect()
                            resposta = cliente.send_receive(comando +' '+ args[1].upper() +' '+ args[2])
                            print('Resposta: %s' % resposta.decode())
                            cliente.close()
                    elif args[1].upper() == 'ALL':
                        cliente.connect()
                        resposta = cliente.send_receive(comando +' '+ args[1].upper())
                        print('Resposta: \n%s' % resposta.decode())
                        cliente.close()
                
        else:
            print("UNKNOWN COMMAND")

    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()