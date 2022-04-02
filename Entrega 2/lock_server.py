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

while True:
    try:
        (conn_sock,addr) = socket.accept()
        msg = conn_sock.recv(1024)
        separado = pickle.loads(msg)
        print('Recebi: ',separado)

        pool.clear_expired_locks()

        comando = separado[0] 

        if comando == 10:
            resp = [11,pool.lock(separado[1],int(separado[2]),int(separado[4]),int(separado[3]))]

        elif comando == 20:
            resp = [21,pool.unlock(separado[1],int(separado[2]),int(separado[3]))]
        
        elif comando == 30:
            resp = [31,pool.status(separado[1])]
        
        elif comando == 40:
            resp = [41,pool.stats("K",int(separado[1]))]

        elif comando == 50:
            resp = [51,pool.stats("N")]

        elif comando == 60:
            resp = [61,pool.stats("D")]
            
        elif comando == 70:      
            resp = [71,pool.__repr__()]

        print('Enviei: ',resp)

        conn_sock.sendall(pickle.dumps(resp, -1) )
        conn_sock.close()
        
    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()