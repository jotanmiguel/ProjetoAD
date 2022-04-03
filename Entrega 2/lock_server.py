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
import select

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
    exit()

pool = lock_pool(num_recursos, num_locks)
socket = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
skel = ListSkeleton(num_recursos, num_locks)

socket_list = [socket]


while True:
    try:
        (conn_sock,addr) = socket.accept()
        msg = conn_sock.recv(1024)
        recebido = pickle.loads(msg)
        print('Recebi: ',recebido)

        pool.clear_expired_locks()

        enviado = skel.bytesToList(skel.processMessage(msg))
        print('Enviei: ', enviado)

        conn_sock.sendall(skel.processMessage(msg))
        conn_sock.close()
        
    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()
