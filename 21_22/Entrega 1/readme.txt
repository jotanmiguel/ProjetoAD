"""
Aplicações Distribuídas - Projeto 1
Grupo: 33
Números de aluno: 56908, 56916
"""

EXEMPLO DE INICIALIZAÇÃO:

Cliente: python3 ticker_client.py 1 localhost 9999
Servidor: python3 ticker_server.py localhost 9999 4 3 100


EXEMPLO DE COMANDOS A CORRER:

SUBSCR 1 100 -> OK
SLEEP 10
SUBSCR 2 100 -> OK
SUBSCR 3 100 -> OK
SUBSCR 4 100 -> NOK
SUBSCR 1 10 -> OK
SLEEP 10
SUBSCR 4 100 -> OK
STATIS L 1 -> 0
STATUS 1 -> UNSUBSCRIBED
INFOS M -> [2,3,4]
EXIT

COMENTÁRIOS EXTRA:

O programa cumpre todos os objetivos, sendo que a única limitação que apresenta é ao fechar o servidor,
O servidor so fecha se depois do Ctrl+C receber um comando, por exemplo, subscr 1 10.


