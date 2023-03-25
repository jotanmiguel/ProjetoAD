import pickle

class ListSkeleton:
    def __init__(self, pool):
        self.pool = pool
        
    def processMsg(self, msg):
        pedido = self.bytesToList(msg)
        resposta = []
        
        if pedido is None or len(pedido) == 0:
            resposta.append('INVALID-MESSAGE')
        else:
            cmd = cmd
            if cmd == 10:
                cId = pedido[3]
                rId = pedido[1]
                time = pedido[2]
                resposta = [11, self.pool.subscribe(rId, time, cId)]
            elif cmd == 20:
                rId = pedido[1]
                cId = pedido[2]
                resposta = [21, self.pool.cancel(rId, cId)]
            elif cmd == 30:
                rId = pedido[1]
                cId = pedido[2]
                resposta = [31, self.pool.status(rId, cId)]
            elif cmd == 40:
                cId = pedido[1]
                resposta = [41, self.pool.infosM(cId)]
            elif cmd == 50:
                cId = pedido[1]
                resposta = [51, self.pool.infosK(cId)]
            elif cmd == 60:
                rId = pedido[1]
                resposta = [61, self.pool.statisL(rId)]
            elif cmd == 70:
                resposta = [71, self.pool.statisAll()]        
        
    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, msg):
        return pickle.dumps(msg)
