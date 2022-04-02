#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_skel.py
Grupo: 2
Números de aluno: 56908, 56954
"""

import pickle
from lock_pool import lock_pool
class ListSkeleton:
    def __init__(self, tLim):
        self.tLim = tLim
        self.pool = lock_pool(None)

    def processMessage(self, msg_bytes):
        pedido = self.bytesToList(msg_bytes)
        resposta = []

        if pedido is None or len(pedido) == 0:
            resposta.append('INVALID MESSAGE')
        else:
            cmd = pedido[0]
            if cmd == 10:
                cId = pedido[4]
                resposta.append('11')
            elif cmd == 20:
                resposta.append('21')
            elif cmd == 30:
                resposta.append('31')
            elif cmd == 40:
                resposta.append('41')
            elif cmd == 50:
                resposta.append('51')
            elif cmd == 60:
                resposta.append('61')
            elif cmd == 70:
                resposta.append('71')
            else:
                resposta.append('INVALID MESSAGE')

        return self.listToBytes(resposta)

    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, msg):
        return pickle.dumps(msg)

