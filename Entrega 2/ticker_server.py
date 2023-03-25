#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 33
Números de aluno: 56908, 56916
"""
import pickle
import sys
import sock_utils
import select as sel
import socket as s
from ticker_pool import resource_pool
from ticker_skel import ListSkeleton

if len(sys.argv) == 6:
    if sys.argv[1] == "localhost":
        HOST = "127.0.0.1"
        PORT = int(sys.argv[2])
        num_acoes = int(sys.argv[3])
        max_acoes = int(sys.argv[4])
        max_subs = int(sys.argv[5])
    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        num_acoes = int(sys.argv[3])
        max_acoes = int(sys.argv[4])
        max_subs = int(sys.argv[5])
else:
    print("UNKNOWN-COMMAND")
    exit()

pool = resource_pool(max_subs, max_acoes, num_acoes)
socket = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
skel = ListSkeleton(pool)

socket_list = [socket]

while True:
    try:
        R,W,X = sel.select(socket_list, [], [])
        for sock in R:
            if sock is socket:
                (conn_sock, addr) = socket.accept()
                socket_list.append(conn_sock)
                addr, port = conn_sock.getpeername()
                print(f'Connected to {addr}:{port}')
            else:
                try:
                    pool.clear_expired_subs()
                    msg = conn_sock.recv(1024)
                    recebido = pickle.load(msg)
                    print(recebido)
                    print("Recebi: ", recebido)

                    if recebido:
                        enviado = skel.bytesToList(skel.processMsg(recebido))
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