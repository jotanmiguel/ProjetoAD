#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_server.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import sys
import sock_utils
import time
import socket as s
import pickle
from lock_pool import lock_pool
from lock_skel import ListSkeleton
import select as sel
import socketserver

if len(sys.argv) == 5:
        if sys.argv[1] == 'localhost':
            HOST = '127.0.0.1'
            PORT = int(sys.argv[2])
            num_recursos = int(sys.argv[3])
            num_locks = int(sys.argv[4])
        else:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            num_recursos = int(sys.argv[3])
            num_locks = int(sys.argv[4])
else:
    print("Utilização errada do comando!")
    


socket = sock_utils.create_tcp_server_socket("", PORT, 5)
pool = lock_pool(num_recursos, num_locks)
skel = ListSkeleton(pool)

socket_list = [socket]


while True:
    try:
        R,W,X = sel.select(socket_list, [], [])
        for sock in R:
            if sock is socket:
                    (conn_sock,addr) = socket.accept()                
                    socket_list.append(conn_sock)
                    addr, port = conn_sock.getpeername()
                    print("Novo cliente connectado")
                    print(f'Novo cliente ligado desde {addr}:{port}')                    
            else:
                try:



                    pool.clear_expired_locks()                    
                    msg = conn_sock.recv(1024)
                    recebido = pickle.loads(msg)
                    print('Recebi: ',recebido)

                    if recebido:
                        enviado = skel.bytesToList(skel.processMessage(msg))                        
                        print('Enviei: ', enviado)
                        conn_sock.sendall(skel.listToBytes(enviado))
                        conn_sock.close()  
                      
                    
                    else:
                        print("Conexão interrompida")
                        conn_sock.close()  
                        socket_list.remove(sock)
                        
                except:
                    None
    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()
socket.close() 
