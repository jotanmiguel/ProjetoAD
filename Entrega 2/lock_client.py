#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_client.py
Grupo: 2
Números de aluno: 56908, 56954
"""
# Zona para fazer imports

import sys
import socket as s
import net_client
import time
import pickle
import struct

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
    cliente.connect()
    try:
        
        inputLinha = input("Comando: ")
        args = inputLinha.split()
        comando = args[0].upper()

        if comando in comandosSup:
            if comando == 'EXIT':
                cliente.close() 
                break

            elif comando == 'SLEEP':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                else:
                    time.sleep(int(args[1]))

            elif comando == "LOCK":
                if len(args) < 4:
                    print("MISSING ARGUMENTS")
                else:
                    
                    msg = [10,args[1],int(args[2]),int(args[3]),int(ID)]
                    msg_bytes = pickle.dumps(msg, -1)
                    resposta = cliente.send_receive(msg_bytes)
                    print('Resposta: ',pickle.loads(resposta))
                     
                    

            elif comando == "UNLOCK":
                if len(args) < 3:
                    print("MISSING ARGUMENTS")
                else:
                    
                    msg = [20,args[1],int(args[2]),int(ID)]
                    msg_bytes = pickle.dumps(msg, -1) 
                    resposta = cliente.send_receive(msg_bytes)
                    print('Resposta: ',pickle.loads(resposta))
                     
                    

            elif comando == 'STATUS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                else:
                    
                    msg = [30,int(args[1])]
                    msg_bytes = pickle.dumps(msg, -1) 
                    resposta = cliente.send_receive(msg_bytes)
                    print('Resposta: ',pickle.loads(resposta))
                     
                    

            elif comando == 'STATS':
                if len(args) < 2:
                    print("MISSING ARGUMENTS")
                elif args[1].upper() in ['K','N','D']:
                    if args[1].upper() == 'K':
                        if len(args) < 3:
                            print("MISSING ARGUMENTS")
                        else:
                            
                            msg = [40,args[1], int(args[2])]
                            msg_bytes = pickle.dumps(msg, -1) 
                            resposta = cliente.send_receive(msg_bytes)
                            print('Resposta: ',pickle.loads(resposta))
                             
                            
                    elif args[1].upper() == 'N':
                            if len(args) < 2:
                                print("MISSING ARGUMENTS")
                            else:
                                
                                msg = [50, args[1]]
                                msg_bytes = pickle.dumps(msg, -1) 
                                resposta = cliente.send_receive(msg_bytes)
                                print('Resposta: ',pickle.loads(resposta))
                                 
                                
                    elif args[1].upper() == 'D':

                            if len(args) < 2:
                                print("MISSING ARGUMENTS")
                            else:
                                
                                msg = [60, args[1]]
                                msg_bytes = pickle.dumps(msg, -1) 
                                resposta = cliente.send_receive(msg_bytes)
                                print('Resposta: ',pickle.loads(resposta))
                                 
                                

            elif comando == "PRINT":
                    
                    msg = [70]
                    msg_bytes = pickle.dumps(msg, -1) 
                    resposta = cliente.send_receive(msg_bytes)
                    print('Resposta: ',pickle.loads(resposta))

                                 
        else:
            print("UNKNOWN COMMAND")
        cliente.close()
    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()

