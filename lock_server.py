#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_server.py
Grupo:
Números de aluno:
"""

# Zona para fazer importação

import sys
import sock_utils
import time
import socket as s

###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.resource_id = resource_id
        pass # Remover esta linha e fazer implementação da função

    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        pass # Remover esta linha e fazer implementação da função

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        pass # Remover esta linha e fazer implementação da função

    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        pass # Remover esta linha e fazer implementação da função

    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        pass # Remover esta linha e fazer implementação da função

    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        pass # Remover esta linha e fazer implementação da função
   
    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        # Se o recurso está bloqueado para a escrita:
        # R <num do recurso> LOCKED-W <vezes bloqueios de escrita> <id do cliente> <deadline do bloqueio de escrita>
        # Se o recurso está bloqueado para a leitura:
        # R <num do recurso> LOCKED-R <vezes bloqueios de escrita> <num bloqueios de leitura atuais> <último deadline dos bloqueios de leitura>
        # Se o recurso está desbloqueado:
        # R <num do recurso> UNLOCKED
        # Se o recurso está inativo:
        # R <num do recurso> DISABLED

        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de resource_locks para N recursos. 
        Os locks podem ser manipulados pelos métodos desta classe. 
        Define K, o número máximo de bloqueios de escrita permitidos para cada 
        recurso. Ao atingir K bloqueios de escrita, o recurso fica desabilitado.
        """
        self.lista = [resource_lock() for x in range(N)]
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        pass # Remover esta linha e fazer implementação da função

    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def stats(self, option, resource_id):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        #
        # Acrescentar no output uma linha por cada recurso
        #
        return output

###############################################################################

# código do programa principal

if len(sys.argv) == 4:
        if sys.argv[1] == 'localhost':
            HOST = '127.0.0.1'
            PORT = int(sys.argv[2])
            num_recursos = int(sys.argv[3])
            num_locks = int(sys.argv[4])
        else:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            num_recursos = int(sys.argv[3])
            num_locks = int(sys.argv[4])
else:
    print("Utilização errada do comando!")
    exit()

pool = lock_pool(num_recursos, num_locks)
socket = sock_utils.create_tcp_server_socket(HOST, PORT, 1)

while True:

    final = ''

    (conn_sock,addr) = socket.accept()
    msg = conn_sock.recv(1024)
    print('Recebi: %s' %msg)

    separado = msg.split(' ')
    comando = separado[0].upper() 

    if comando == "LOCK":
        resp = pool.lock(separado[1],int(separado[2]),int(separado[3]),int(separado[4]))
        #Fazer ifs

    elif comando == "UNLOCK":
        resp = pool.unlock(separado[1],int(separado[2]),int(separado[3]))
        #Fazer ifs
    
    elif comando == "STATUS":
        resp = pool.status(separado[1])
        final = resp
    
    elif comando == "STATS":
        if separado[1] == "K":
            resp = pool.stats(separado[1],int(separado[2]))
            final = resp
        elif separado[1] == "N":
            resp = pool.stats(separado[1])
            final = resp
        elif separado[1] == "D":
            resp = pool.stats(separado[1])
            final = resp
        
    elif comando == "PRINT":
        #por acabar (ler enunciado)       
        resp = []
        for x in pool.lista:
            resp.append(x.status())
        final = resp

    conn_sock.sendall(resp)
    conn_sock.close()
