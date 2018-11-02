
import select
import socket
import sys
import signal
from communication import send, receive

BUFSIZ = 1024


class ChatServer(object):
    def __init__(self, port=3490, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',port))
        print '\nPara cliente ingrese: python2  chatid   host  3490'
        print '\nEscuchando el puerto ',port,'...'
        self.server.listen(backlog)
        signal.signal(signal.SIGINT, self.sighandler)
        
    def sighandler(self, signum, frame):
        print 'Desconectando el server...'
        # Cierra los clientes conectados
        for o in self.outputs:
            o.close()
        self.server.close()

    def getname(self, client):
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))
        
    def serve(self):
        inputs = [self.server,sys.stdin]
        self.outputs = []
        running = 1

        while running:

            try:
                inputready,outputready,exceptready = select.select(inputs, self.outputs, [] )
            except select.error, e:
                break
            except socket.error, e:
                break

            for s in inputready:
                if s == self.server:
                    client, address = self.server.accept()
                    print 'Server Chat-Echo: conexion %d desde %s' % (client.fileno(), address)
                    # Obtiene el nombre de ingreso.
                    cname = receive(client).split('NAME: ')[1]
                    
                    #Incrementa el contador de clientes.
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)

                    msg = '\n(Nuevo cliente (%d) desde %s)' % (self.clients, self.getname(client))
                    for o in self.outputs:
                         if o == s:
                            send(o, msg)
                    
                    self.outputs.append(client)

                elif s == sys.stdin:
                    # Cuando se pulsa algo en el server, termina ejecucion.
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    try:
                        data = receive(s)
                        print 'Recibido de ',self.getname(s),data

                        if data != 'Exit':
                            msg = '\n   Echo ' + data
                            for o in self.outputs:
                                if o == s:
                                    send(o, msg)
                        else:
                            print 'Desconecta cliente ...', self.getname(s)
                            self.clients -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            msg = '\n(Cliente desconectado desde  %s)' % self.getname(s)
                            for o in self.outputs:
                                if o == s:
                                    send(o, msg)
                                
                    except socket.error, e:
                        inputs.remove(s)
                        self.outputs.remove(s)
                        


        self.server.close()

if __name__ == "__main__":
    ChatServer().serve()



