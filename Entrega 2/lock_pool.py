#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_pool.py
Grupo: 2
Números de aluno: 56908, 56954
"""

# zona para fazer importação

import sock_utils, time
class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.resource_id = resource_id
        self.lockStatus = 0 #0 - Unlocked 1 - Locked Read 2 - Locked Write 3 - Disabled
        self.clientLockId = None
        self.writeLockList = []
        self.readLockList = []
        self.writeLockCount = 0
        self.maxK = 0


    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        if type == "W":

            if self.status() == "UNLOCKED" and self.writeLockCount < self.maxK:
                self.writeLockCount += 1                
                self.lockStatus = 2
                deadline = time.time() + time_limit
                self.writeLockList.append((client_id,deadline))
                return True
                
            elif self.status() == "LOCKED-W" or self.status() == "LOCKED-R" or self.status() == "DISABLED":
                return False

        elif type == "R":

            if self.status() == "UNLOCKED" or self.status() == "LOCKED-R":
                self.lockStatus = 1
                deadline = time.time() + time_limit
                self.readLockList.append((client_id,deadline))
                return True

            elif self.status() == "LOCKED-W" or self.status() == "DISABLED":
                return False


    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.lockStatus = 0

    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        if type == "W":

            if self.lockStatus == 2 and int(self.writeLockList[0][0]) == int(client_id) and self.writeLockCount < self.maxK:
                self.writeLockList.pop(0)
                self.lockStatus = 0
                return True

            elif self.lockStatus == 2 and self.writeLockCount == self.maxK and int(self.writeLockList[0][0]) == int(client_id):
                self.writeLockList.pop(0)
                self.lockStatus = 3
                return True

            else:
                return False

        elif type == "R":

            if self.lockStatus == 1:
                clientsList = []
                for x in range(len(self.readLockList)):
                    clientsList.append(self.readLockList[x][0])

                if client_id in clientsList:
                    self.readLockList.pop(clientsList.index(client_id))
                    if len(self.readLockList) == 0:
                        self.lockStatus = 0
                    return True

                else:
                    return False

    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        if self.lockStatus == 0:
            return "UNLOCKED"
        elif self.lockStatus == 1:
            return "LOCKED-R"
        elif self.lockStatus == 2:
            return "LOCKED-W"
        elif self.lockStatus == 3:
            return "DISABLED"

    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        return self.writeLockCount
   
    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.lockStatus = 3

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

        if self.lockStatus == 0:
            output += "R "+str(self.resource_id)+" UNLOCKED "+str(self.writeLockCount)+"\n" 
        elif self.lockStatus == 1:
            output += "R "+str(self.resource_id)+" LOCKED-R "+ str(self.writeLockCount) +" "+ str(len(self.readLockList))+ " " + str(self.readLockList[len(self.readLockList)-1][1])+"\n"
        elif self.lockStatus == 2: 
            output += "R "+str(self.resource_id)+" LOCKED-W "+ str(self.writeLockCount) +" "+ str(self.writeLockList[0][0])+ " " + str(self.writeLockList[0][1])+"\n"
        else:
            output += "R "+str(self.resource_id)+" DISABLED "+str(self.writeLockCount)+"\n"   

        return output

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de resource_locks para N recursos. 
        Os locks podem ser manipulados pelos métodos desta classe. 
        Define K, o número máximo de bloqueios de escrita permitidos para cada 
        recurso. Ao atingir K bloqueios de escrita, o recurso fica desabilitado.
        """
        self.K = K
        self.lista = [resource_lock(x) for x in range(1,N+1)]
        for x in self.lista:
            x.maxK = self.K
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for x in self.lista:
            if len(x.writeLockList) > 0:

                if time.time() > x.writeLockList[0][1] and x.writeLockCount < x.maxK:
                    x.writeLockList = []
                    x.lockStatus = 0

                elif time.time() > x.writeLockList[0][1] and x.writeLockCount == x.maxK:
                    x.writeLockList = []
                    x.lockStatus = 3

            elif len(x.readLockList) > 0:

                for y in range(len(x.readLockList)):

                    if time.time() > x.readLockList[y][1]:
                        x.readLockList.pop(y)

                        if len(x.readLockList) == 0:
                            x.lockStatus = 0


    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        for x in self.lista:
            if x.resource_id == resource_id:
                return x.lock(type,client_id,time_limit)
        if resource_id < 1 or resource_id > len(self.lista):
            return None
            
            

    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        for x in self.lista:
            if x.resource_id == resource_id:
                return x.unlock(type,client_id)
        if resource_id < 1 or resource_id > len(self.lista):
            return None

    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        for x in self.lista:
            if int(x.resource_id) == int(resource_id):
                return str(x.status())
        if int(resource_id) < 1 or int(resource_id) > len(self.lista):
            return str(None)

    def stats(self, option, resource_id=None):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == "K":

            for x in self.lista:
                if x.resource_id == resource_id:
                    return str(x.stats())

            if resource_id < 1 or resource_id > len(self.lista):
                return None

        elif option == "N":

            count = 0
            for x in self.lista:
                if x.status() == "UNLOCKED" :
                    count += 1
            return str(count)

        elif option == "D":

            count = 0
            for x in self.lista:
                if x.status() == "DISABLED":
                    count += 1
            return str(count)


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
        for x in self.lista:
            output += x.__repr__()
        return output