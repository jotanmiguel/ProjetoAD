import pickle
import socket as s
import struct
import sys
from typing import List, Union
from net_client import server_connection

# Para ficar no root da pasta, por causa do sock_utils
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
        """

        if msg[0] == 10:
            resp = self.lock

    def lock(self, type, rId, tLim, cId):
        """
        Metodo para bloquear um ficheiro rId para leitura ou escrita (type = R or typer = W, respetivamente)
        pelo cliente cId durante tLim segundos.

        Args:
            type (str): tipo de bloqueio.
            rId (int): ficheiro a ser bloqueado.
            tLim (int): limite de tempo do bloqueio.
            cId (int): identificacao do cliente que vai bloquear o ficheiro rId.
        """
        msg = [10, type, rId, tLim, cId]
        return self.server.send_receive(msg) 

    def lock(self):
        pass

    def lock(self):
        pass

    def lock(self):
        pass

    def lock(self):
        pass