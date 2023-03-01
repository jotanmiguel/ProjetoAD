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

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.resourceStatus = 0
        self.subList = [];

    def subscribe(self, client_id, time_limit):
            if self.status(client_id) == "UNSUBSCRIBED" and (self.writeSubCount < self.maxK or self.writeSubCount):
                self.writeLockCount += 1
                smax_acoestatus = 2
                deadline = time.time() + time_limit
                self.subList.append((client_id, deadline))
                return "OK"
            else:
                return "NOK"

    def unsubscribe (self, client_id):
        pass # Remover esta linha e fazer implementação da função

    def status(self, client_id):
        pass
    
    def __repr__(self):
        output = f'R %d %d',self.resource_id, self.subList 
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
        self.K = K
        self.N = N
        self.M = M
        
    def clear_expired_subs(self):
        pass # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        pass # Remover esta linha e fazer implementação da função

    def unsubscribe (self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função

    def status(self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função

    def infos(self, option, client_id):
        pass # Remover esta linha e fazer implementação da função

    def statis(self, option, resource_id):
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # Acrescentar no output uma linha por cada recurso
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
            resp = pool.subscribe(
                separado[1], int(separado[2]), int(separado[3]), int(separado[4])
            )

        elif comando == "CANCEL":
            resp = pool.unsubscribe(separado[1], int(separado[2]), int(separado[3]))

        elif comando == "STATUS":
            resp = pool.status(separado[1])

        elif comando == "INFOS":
            if separado[1] == "M":
                resp = pool.infos(separado[1], int(separado[2]))

            elif separado[1] == "K":
                resp = pool.infos(separado[1])

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
