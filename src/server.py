import socket
import threading
import sys
import pickle



class Servidor():

    def __init__(self, host="", port=3250):

        self.clientes = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(5)
        self.sock.setblocking(False)

        aceitar = threading.Thread(target=self.aceitarCon)
        processar = threading.Thread(target=self.processarCon)

        aceitar.daemon = True
        aceitar.start()

        processar.daemon = True
        processar.start()

        while True:
            print('Para fechar o servidor digite: close')
            msg = input('->')
            if msg == 'close' or msg == 'CLOSE':
                self.sock.close()
                sys.exit()
            else:
                pass

    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except Exception:
                self.clientes.remove(c)

    def aceitarCon(self):
        print("aceitarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
                print("{} se conectou ao servidor!".format(addr))
            except Exception:
                pass

    def teste(self):
        print('it works')

    def processarCon(self):
        print("ProcessarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        print(pickle.loads(data))
                        if data:
                            self.msg_to_all(data, c)
                    except Exception:
                        pass


s = Servidor()
