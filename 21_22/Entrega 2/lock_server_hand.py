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

pool = lock_pool(num_recursos, num_locks)    
skel = ListSkeleton(pool)

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
            pool.clear_expired_locks()          
            msg = self.request.recv(1024)
            print('ligado a ', self.client_address)    
            recebido = pickle.loads(msg)
            print('Recebi: ',recebido)
            enviado = skel.bytesToList(skel.processMessage(msg)) 
            print('Enviei: ', enviado)
            self.request.sendall(skel.listToBytes(enviado))                  

server = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
server.serve_forever(2.0)


