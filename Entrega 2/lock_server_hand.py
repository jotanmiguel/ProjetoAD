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
from ticker_pool import resource_pool
from ticker_skel import ListSkeleton
import select as sel
import socketserver
import struct

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
skel = ListSkeleton(pool)

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
            pool.clear_expired_subs()          
            msg = self.request.recv(1024)
            print('ligado a ', self.client_address)    
            recebido = pickle.loads(msg)        
            print('Recebi: ',recebido)
            enviado = skel.bytesToList(skel.processMsg(msg)) 
            print('Enviei: ', enviado)
            self.request.sendall(skel.listToBytes(enviado))                

server = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
server.serve_forever(2.0)