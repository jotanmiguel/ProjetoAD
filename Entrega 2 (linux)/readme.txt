"""
Aplicações Distribuídas - Projeto 2
Grupo: 2
Números de aluno: 56908, 56954
"""

EXEMPLO DE INICIALIZAÇÃO:

Cliente: python lock_client.py 1 localhost 9999
Servidor: python lock_server.py localhost 9999 4 3


EXEMPLO DE COMANDOS A CORRER:

LOCK W 1 30
SLEEP 5
STATUS 0
STATS K 0
STATS N
UNLOCK W 0
PRINT
EXIT

LOCK W 0 10
LOCK W 1 10
LOCK W 2 10
LOCK R 3 10
LOCK R 4 10
STATS N
SLEEP 20
PRINT
EXIT


COMENTÁRIOS EXTRA:

O programa não suporta na totalidade mais do que um utilizador.
