#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo:
Números de aluno:
"""

# Zona para fazer importação

import sys
import time
import sock_utils
import random
import socket as s

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.subList = {};
        self.maxN = 0
        self.value = 0
        self.name = ''
        self.simbol = ''

    def subscribe(self, client_id, time_limit):
            if self.status(client_id) == "UNSUBSCRIBED" and len(self.subList) < self.maxN:
                deadline = time.time() + time_limit
                self.subList[client_id] = deadline
                return "OK"
            else:
                return "NOK"

    def unsubscribe(self, client_id):
        if self.status(client_id) == "SUBSCRIBED":
            self.subList.pop(client_id)
            return "OK"
        elif self.status(client_id) == "UNSUBSCRIBED":
            return "NOK"
        else:
            return "NOK"

    def status(self, client_id):
        if client_id not in self.subList.keys():
            return "UNSUBSCRIBED"
        elif client_id in self.subList.keys():
            return "SUBSCRIBED"
    
    def __repr__(self):
        output = f'R %d %d %d',self.resource_id, len(self.subList.keys()), self.subList.keys()
        # R <resource_id> <list of subscribers>
        return output

###############################################################################

class resource_pool:
    def __init__(self, N:int, K:int, M:int):
        """
        Construtor da classe resouce_pool

        Args:
            N (int): Número máximo de subscritores por ação.
            K (int): Número máximo de ações por cliente.
            M (int): Número de ações/recursos que serão geridos pelo servidor.
        """                   
        self.N = N
        self.maxK = K
        self.clientList = {}
        self.lista = [resource(x) for x in range(1, M + 1)]
        for x in self.lista:
            x.maxN = self.N
            x.name = ''.join((random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(7)))
            x.value = random.randint(100,200)
            x.simbol = x.name[0:2]
        
    def clear_expired_subs(self):
        pass # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        for x in self.lista:
            if x.resource_id == resource_id:
                if client_id not in self.clientList.keys():
                    self.clientList[client_id] = [resource_id]
                elif client_id in self.clientList.keys() and resource_id not in self.clientList[client_id] and len(self.clientList[client_id]) < self.maxK:
                    self.clientList[client_id].append(resource_id)
                elif client_id in self.clientList.keys() and resource_id not in self.clientList[client_id] and len(self.clientList[client_id]) >= self.maxK:
                    return "NOK"
                return x.subscribe(client_id, time_limit)
        if resource_id < 1 or resource_id > len(self.lista):
            return "UNKNOWN-RESOURCE"

    def unsubscribe(self, resource_id, client_id):
        for x in self.lista:
            if x.resource_id == resource_id:
                return x.unsubscribe(client_id)
        if resource_id < 1 or resource_id > len(self.lista):
            return "UNKNOWN-RESOURCE"

    def status(self, resource_id, client_id):
        for x in self.lista:
            if int(x.resource_id) == int(resource_id):
                return str(x.status(client_id))
        if int(resource_id) < 1 or int(resource_id) > len(self.lista):
            return str("UNKNOWN-RESOURCE")


    def infos(self, option, client_id):
        if option == "M":
            if client_id in self.clientList.keys():
                return str(self.clientList[client_id])

        elif option == "K":
            for x in self.lista:
                return str(x.stats())

    def statis(self, option, resource_id=None):
        if option == "L":
            for x in self.lista:
                if x.resource_id == resource_id:
                    return str(len(x.subList))

            if resource_id < 1 or resource_id > len(self.lista):
                return "UNKNOWN-RESOURCE"

        elif option == "ALL":
            for x in self.lista:
                return str(self.__repr__)

    def __repr__(self):
        output = ""
        for x in self.lista:
            output += x.__repr__()
        return output

###############################################################################

# código do programa principal

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

while True:
    try:
        (conn_sock, (addr, port)) = socket.accept()
        print(f'Connected to {addr}:{port}')
        msg = conn_sock.recv(1024)
        print("Recebi: %s" % msg)

        pool.clear_expired_subs()

        separado = msg.decode().split()
        comando = separado[0].upper()

        if comando == "SUBSCR":
            resp = pool.subscribe(int(separado[1]), int(separado[3]), int(separado[2]))

        elif comando == "CANCEL":
            resp = pool.unsubscribe(int(separado[1]), int(separado[2]))

        elif comando == "STATUS":
            resp = pool.status(int(separado[1]), int(separado[2]))

        elif comando == "INFOS":
            if separado[1] == "M":
                resp = pool.infos(separado[1], int(separado[2]))

            elif separado[1] == "K":
                resp = pool.infos(separado[1], int(separado[2]))

        elif comando == "STATIS":
            if separado[1] == "L":
                resp = pool.statis(separado[1], int(separado[2]))

            elif separado[1] == "ALL":
                resp = pool.statis(separado[1])

        conn_sock.sendall(resp.encode())
        conn_sock.close()

    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()
