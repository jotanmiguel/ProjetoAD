#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_stub.py
Grupo: 33
Números de aluno: 56908, 56916
"""

# Zona para fazer importação
import sys
from net_client import server_connection
sys.path.insert(0, '..')

class ListStub:
    def __init__(self, host, port):
        self.server = server_connection(host, port)
        
    def connect(self):
        """
        Metodo para conexao com o servidor.
        """
        self.server.connect()
        
    def close(self):
        """
        Metodo para a desconexao com o servidor.
        """
        self.server.close()
        
    def send_msg(self, msg:list):
        """
        Metodo para a comunicacao com o servidor.

        Args:
            msg (list): lista em que cada elemento representa um parametro especifico do comando a ser enviado.

        Returns:
            list: lista com a resposta 
        """
        if msg[0] == 10:
            resp = self.subscribe(msg[1], msg[2], msg[3])
        elif msg[0] == 20:
            resp
        elif msg[0] == 30:
            resp
        elif msg[1] == 40:
            resp
        elif msg[1] == 50:
            resp
        elif msg[1] == 60:
            resp
        elif msg[0] == 70:
            resp
        else:
            return "UNKNOWN COMMAND"
        return resp
    
    def subscribe(self, rId:int, time:int, cId:int):
        """
        O método subscribe subscreve do recurso, durante um tempo de concessão 
        específico (em segundos) para o cliente que está a enviar o pedido (Deadline = 
        tempo do relógio atual do servidor + tempo concessão).
        
        Retorna [11, True] se foi subscrito, [11, False] se já estava subscrito ou [11, 'UNKNOWN-RESOURCE'] se o recurso nao existe. 

        Args:
            rId (int): Id do recurso a subscrever.
            cId (int): Id do cliente a subscrever este recurso.
            time (int): tempo de subscrição.

        Returns:
            list: [11, True] or [11, False]
        """
        return self.server.send_receive([10, rId, time, cId])
    
    def unsubscribe(self, rId:int, cId:int):
        """
        O método unsubscribe cancela a subscrição do recurso para o cliente que está a 
        enviar o pedido.
        
        Retorna [21, True] se foi cancelada, [21, False] se não estava subscrito ou [21, 'UNKNOWN-RESOURCE'] se o recurso nao existe.

        Args:
            rId (int): Id do recurso a cancelar a subscrição.
            cId (int): Id do cliente a cancelar a subscrição deste recurso.

        Returns:
            list: [21, True], [21, False] or [21, 'UNKNOWN-RESOURCE']
        """
        return self.server.send_receive([20, rId, cId])
    
    def status(self, rId:int, cId:int):
        """        
        Método que retorna o estado a atual do recurso com o id "resource_id" para o cliente com 
        o id "client_id".
        Retorna [31, 'SUBSCRIBED'] se subscrito, [31, 'UNSUBSCRIBED'] se não subscrito ou [31 ,'UNKNOWN-RESOURCE'] se o recurso nao existe.

        Args:
            rId (int): Id do recurso a verificar o estado.
            cId (int): Id do cliente a verificar o estado deste recurso.

        Returns:
            list: [31, 'SUBSCRIBED'], [31, 'UNSUBSCRIBED'] or [31 ,'UNKNOWN-RESOURCE']
        """
        return self.server.send_receive([30, rId, cId])
    
    def infosM(self, cId):
        return self.server.send_receive([40, cId])
    
    def infosK(self, cId):
        return self.server.send_receive([50, cId])
    
    def statisL(self, rId):
        return self.server.send_receive([60, rId])
    
    def statisAll(self):
        return self.server.send_receive([70])