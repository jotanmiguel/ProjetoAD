#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_skel.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import pickle
from tkinter import RIDGE
from lock_pool import lock_pool
import struct

class ListSkeleton:
    def __init__(self, pool):
        self.pool = pool

    def processMessage(self, msg_bytes):
        pedido = self.bytesToList(msg_bytes)
        resposta = []

        if pedido is None or len(pedido) == 0:
            resposta.append('INVALID MESSAGE')
        else:
            cmd = pedido[0]
            if cmd == 10:
                cId = pedido[4]
                rId = pedido[2]
                tLim = pedido[3]
                type = pedido[1]
                resposta = [11,self.pool.lock(type, rId, cId, tLim)]
            elif cmd == 20:
                cId = pedido[3]
                rId = pedido[2]
                type = pedido[1]
                resposta = [21,self.pool.unlock(type, rId, cId)]
            elif cmd == 30:
                rId = pedido[1]
                resposta = [31,self.pool.status(rId)]
            elif cmd == 40:
                rId = pedido[2]
                opt = pedido[1]
                resposta = [41,self.pool.stats(opt, rId)]
            elif cmd == 50:
                opt = pedido[1]
                resposta = [51, self.pool.stats(opt)]
            elif cmd == 60:
                opt = pedido[1]
                resposta = [61, self.pool.stats(opt)]
            elif cmd == 70:
                resposta = [71, self.pool.__repr__()]
            else:
                resposta.append('INVALID MESSAGE')

        return self.listToBytes(resposta)

    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, msg):
        return pickle.dumps(msg,-1)

