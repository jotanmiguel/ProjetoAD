#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_pool.py
Grupo: 2
Números de aluno: 56908, 56954
"""

# zona para fazer importação

import sock_utils

class lock_pool:
    """
    
    """
    def __init__(self, rId, file, state):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        # isto ta mal
        self.files = {}
        self.rId = None
        self.file = None
        self.state = None
