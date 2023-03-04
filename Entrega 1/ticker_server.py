#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 33
Números de aluno: 56908, 56916
"""

# Zona para fazer importação

import sys
import time
import sock_utils
import random
import socket as s

class resource:
    def __init__(self, resource_id: int):
        """
        Construtor da classe "resource", que recebe como argumento o resource_id(int)
        e inicializa um novo "resource".

        Args:
            resource_id (int): Id do novo recurso.
        """
        self.resource_id = resource_id
        self.subList = {};
        self.maxN = 0
        self.value = 0
        self.name = ''
        self.simbol = ''

    def subscribe(self, client_id:int, time_limit: int):
        """
        O método subscribe subscreve do recurso, durante um tempo de concessão 
        específico (em segundos) para o cliente que está a enviar o pedido (Deadline = 
        tempo do relógio atual do servidor + tempo concessão).
        
        Retorna 'OK' ou 'NOK'. 

        Args:
            client_id (int): Id do cliente a subscrever este recurso.
            time_limit (int): tempo de subscrição.

        Returns:
            str: 'OK' se a subscrição for bem sucedida, 'NOK' se houve algum problema.
        """
        if len(self.subList) < self.maxN:
            deadline = time.time() + time_limit
            self.subList[client_id] = deadline
            return "OK"
        else:
            return "NOK"

    def unsubscribe(self, client_id:int):
        """
        O método unsubscribe remove a subscrição do recurso ao cliente com o id
        "cliente_id".
        
        Retorna 'OK' ou 'NOK'.

        Args:
            client_id (int): Id do cliente a remover a subscrição deste recurso.

        Returns:
            str: 'OK' se a remoção da subscrição for bem sucedida, 'NOK' se houve algum 
            problema.
        """
        if self.status(client_id) == "SUBSCRIBED":
            self.subList.pop(client_id)
            return "OK"
        elif self.status(client_id) == "UNSUBSCRIBED" and client_id in self.subList.keys():
            self.subList.pop(client_id)
            return "OK"
        else:
            return "NOK"

    def status(self, client_id:int):
        """
        Método que retorna o estado a atual do recurso para o cliente com o id "client_id".
        
        Retorna 'SUBSCRIBED' ou 'UNSUBSCRIBED'.

        Args:
            client_id (int): Id do cliente.

        Returns:
            str: 'SUBSCRIBED' se está subscrito, 'UNSUBSCRIBED' se não está subscrito.
        """
        if client_id not in self.subList.keys():
            return "UNSUBSCRIBED"
        elif client_id in self.subList.keys():
            return "SUBSCRIBED"
    
    def __repr__(self):
        """
        Representação textual de um recurso no formato R <resource_id> <list of subscribers>.
        Ex: R 1 [1,2,5,42,98]

        Returns:
            str: output apresentável do estado do recurso.
        """
        output = 'R ' + str(self.resource_id) + " " + str(list(self.subList.keys()))
        return output

###############################################################################

class resource_pool:
    def __init__(self, N:int, K:int, M:int):
        """
        Construtor da classe "resource_pool", que recebe como argumentos o N(int), K(int)
        e M(int), e inicializa um novo "resource_pool".
        
        Atributes:
            N (int): Número máximo de subscritores por ação.
            maxK (int): Número máximo de ações por cliente.
            clientList (dict(int:[int])): Dicionário que guarda os recursos atualmente 
            subscritos por cada cliente. Ex: (id:[resource_id, resource_id]).
            lista (list[resource]): Lista de "M" recursos que são inicialiazados.           

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
        """
        Método que verifica se existem recursos em que a concessão tenha expirado, e por 
        sua vez, procede a remoção da conceção, de modo a libertar o recurso em questão.
        """
        for x in self.lista:
            if len(x.subList) > 0:
                for y in x.subList.copy(): 
                    if time.time() > x.subList[y]:
                        self.clientList[y].pop(self.clientList[y].index(x.resource_id))
                        x.unsubscribe(y) 

    def subscribe(self, resource_id:int, client_id:int, time_limit:int):
        """
        Método que subscreve o recurso com o id "resource_id", durante um tempo de concessão 
        específico (em segundos), para o cliente com o id "client_id".
        
        Retorna 'OK', 'NOK' ou 'UNKNOWN-RESOURCE'. 

        Args:
            resource_id (int): Id do recurso a subscrever.
            client_id (int): Id do cliente que fez o pedido.
            time_limit (int): tempo de subscrição.

        Returns:
            str: 'OK' se foi subscrito com sucesso, 'NOK' se houve algum problema e 
            'UNKNOWN-RESOURCE' se o recurso não existe.
        """
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

    def unsubscribe(self, resource_id:int, client_id:int):
        """
        O método unsubscribe remove a subscrição do recurso com o id "resource_id" ao cliente 
        com o id "cliente_id".    
        Retorna: 'OK', 'NOK' ou 'UNKNOWN-RESOURCE'. 

        Args:
            resource_id (int): Id do recurso a subscrever.
            client_id (int): Id do cliente que fez o pedido.

        Returns:
            str: 'OK' se a subscrição foi removida com sucesso, 'NOK' se houve algum problema e 
            'UNKNOWN-RESOURCE' se o recurso não existir.        
        """
        for x in self.lista:
            if x.resource_id == resource_id:
                x.subList.pop(client_id)
                return x.unsubscribe(client_id)
        if resource_id < 1 or resource_id > len(self.lista):
            return "UNKNOWN-RESOURCE"

    def status(self, resource_id:int, client_id:int):
        """
        Método que retorna o estado a atual do recurso com o id "resource_id" para o cliente com 
        o id "client_id".
        Retorna: 'SUBSCRIBED', 'UNSUBSCRIBED' ou 'UNKNOWN-RESOURCE'.

        Args:
            resource_id (int): Id do recurso a subscrever.
            client_id (int): Id do cliente que fez o pedido.

        Returns:
            str: 'SUBSCRIBED' se está subscrito, 'UNSUBSCRIBED' se não está subscrito ou 
            UNKNOWN-RESOURCE se o recurso em questão não existe.
        """
        for x in self.lista:
            if int(x.resource_id) == int(resource_id):
                return str(x.status(client_id))
        if int(resource_id) < 1 or int(resource_id) > len(self.lista):
            return str("UNKNOWN-RESOURCE")


    def infos(self, option:str, client_id:int):
        """
        Método que, dependendo da opção "option", devolve informação sobre o cliente com o
        id "cliente_id".
        Option = 'M': Lista de todos os recursos subscritos pelo cliente.
        Option = 'K': Número de ações que o cliente ainda pode subscrever.
        Retorna: list[int] ou int.
        Ex: se k = 2, [1,2] ou 0.

        Args:
            option (str): Opção do comando.
            client_id (int): Id do cliente que fez o pedido.

        Returns:
            str: Se 'M', lista de recursos, se 'K', números de ações disponíveis.
        """
        if option == "M":
            if client_id in self.clientList.keys():
                return str(self.clientList[client_id])

        elif option == "K":
            if client_id in self.clientList.keys():
                return str(self.maxK - len(self.clientList[client_id]))

    def statis(self, option, resource_id=None):
        """
        O método statis é utilizado para obter informação genérica do servidor,
        tendo duas opções.
        Option = 'L': Número de subscritores do recurso com o id "resource_id".
        Option = 'ALL': Número de subscritores de todos os recursos.
        Retorna: int, str ou 'UNKNOWN-RESOURCE'.
        Ex: se resource_id = 1, 1 ou R 1 1 [1]; R 2 2 [1,2]; R 3 0 []
        
        Args:
            option (str): Opção do comando.
            resource_id (int, optional): Id do recurso a analisar. Defaults to None.

        Returns:
            str: Se 'L', número de subs, se 'ALL', representação textual de todos 
            os recuros e se 'UNKNOWN-RESOURCE', o recurso não existe.
        """
        if option == "L":
            for x in self.lista:
                if x.resource_id == resource_id:
                    return str(len(x.subList))

            if resource_id < 1 or resource_id > len(self.lista):
                return "UNKNOWN-RESOURCE"

        elif option == "ALL":
            return self.__repr__()

    def __repr__(self):
        """
        Representação textual todos os recursos no formato R <resource_id> <number of subscribers> 
        <list of subscribers>.
        Ex: R 1 5 [1,2,5,42,98]

        Returns:
            str: Representação de cada recurso.
        """
        output = ""
        for x in self.lista:
            Srepr = x.__repr__().split()
            output += Srepr[0] + ' ' + Srepr[1] + ' ' + str(len(x.subList.keys())) + ' ' + str(list(x.subList.keys())) + '\n'
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
        pool.clear_expired_subs()
        msg = conn_sock.recv(1024)
        print("Recebi: %s" % msg.decode())

        separado = msg.decode().split()
        comando = separado[0].upper()

        if comando == "SUBSCR":
            resp = pool.subscribe(int(separado[1]), int(separado[3]), int(separado[2]))

        elif comando == "CANCEL":
            resp = pool.unsubscribe(int(separado[1]), int(separado[2]))

        elif comando == "STATUS":
            resp = pool.status(separado[1], int(separado[2]))

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
        print("Connection Closed")

    except KeyboardInterrupt:
        print("\n KeyboardInterrupt")
        exit()
