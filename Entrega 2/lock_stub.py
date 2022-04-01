#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_stub.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import pickle
import socket as s
import struct
import sys
from typing import List, Union
from net_client import server_connection

sys.path.insert(0, '..')
import sock_utils

class ListStub:
    def __init__(self, host, port):
        self.server =  server_connection(host, port)

    def connect(self):
        """
        Metodo para conexao com o servidor.
        """
        self.server.connect()

    def close(self):
        """
        Metodo para a desconexao(?) com o servidor.
        """
        self.server.close()

    def send_msg(self, msg: list):
        """
        Metodo para a comunicacao com o servidor.

        Args:
            msg (list): lista em que cada elemento representa um parametro especifico do comando a ser enviado.

        Returns:
            _type_: _description_
        """

        #Não sei bem como é que vamos defenir o cId mas por enquanto fica como msg[4]

        if msg[0] == "LOCK":
            resp = self.lock(msg[1], msg[2], msg[3], msg[4])
        elif msg[0] == "UNLOCK":
            resp = self.unlock(msg[1], msg[2], msg[4])
        elif msg[0] == "STATUS":
            resp = self.status(msg[4])
        elif msg[0] == "STATS":
            if msg[1] == "K":
                resp = self.statsK(msg[4])
            elif msg[1] == "N":
                resp = self.statsN()
            elif msg[1] == "D":
                resp = self.statsD()
            else:
                return "INVALID COMMAND" #Não sei tmb se estas msgs de erro vão dar nike dps no código, mas yha é uma questão de dps se experimentar
        elif msg[0] == "PRINT":
            resp = self.print()
        else:
            return "UNKNOWN COMMAND"
        return resp
            

    def lock(self, type, rId, tLim, cId):
        """
        Metodo para bloquear um ficheiro rId para leitura ou escrita (type = R or typer = W, respetivamente)
        pelo cliente cId durante tLim segundos.

        Args:
            type (str): tipo de bloqueio.
            rId (int): ficheiro a ser bloqueado.
            tLim (int): limite de tempo do bloqueio.
            cId (int): identificacao do cliente que vai bloquear o ficheiro rId.

        Returns:
            _type_: _description_
        """

        msg = [10, type, rId, tLim, cId]
        return self.server.send_receive(msg) 

    def unlock(self, type, rId, cId):
        """
        Metodo para desbloquear um ficheiro rId para leitura ou escrita (type = R or typer = W, respetivamente)
        pelo cliente cId.

        Args:
            type (str): tipo de UNLOCK.
            rId (int): ficheiro a ser desbloqueado.
            cId (int): identificacao do cliente que vai desbloquear o ficheiro rId.

        Returns:
            _type_: _description_
        """

        msg = [20, type, rId, cId]
        return self.server.send_receive(msg)

    def status(self, rId):
        """
        Metodo que retorna o estado atual do ficheiro rId.

        Args:
            rId (int): ficheiro a ser desbloqueado.
        
        Returns:
            _type_: _description_
        """

        msg = [30, rId]
        return self.server.send_receive(msg)

    def statsK(self, rId):
        """
        Metodo para obter informacao atual sobre o numero de bloqueios do ficheiro rId.

        Args:
            rId (int): ficheiro a ser consultado.

        Returns:
            _type_: _description_
        """
        msg = [40, rId]
        return self.server.send_receive(msg)

    def statsN(self):
        """
        Metodo para obter a informacao relativa ao numero de ficheiros UNLOCKED.

        Returns:
            _type_: _description_
        """
        msg = [50]
        return self.server.send_receive(msg)

    def statsD(self):
        """
        Metodo para obter a informacao relativa ao numero de ficheiros DISABLED.

        Returns:
            _type_: _description_
        """
        msg = [60]
        return self.server.send_receive(msg)

    def print(self):
        """
        Metodo que retorna o estado atual de todos os recursos.

        Returns:
            _type_: _description_
        """

        msg = [70]
        return self.server.send_receive(msg)