
import socket
import sys
import select
from communication import send, receive

BUFSIZ = 1024

class ChatClient(object):
    def __init__(self, name, host='127.0.0.1', port=3490):
        self.name = name
        self.flag = False
        self.port = int(port)
        self.host = host
        self.prompt='[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print "Conectado al server @%d - con 'Exit' termina ..." % self.port
            # Send my name...
            send(self.sock,'NAME: ' + self.name) 
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error, e:
            print 'No se puede conectar al server @%d' % self.port
            sys.exit(1)


    def cmdloop(self):
        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Esperando ingreso desde teclado
                inputready, outputready,exceptrdy = select.select([0, self.sock], [],[])
                
                for i in inputready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        #if data: 
                        send(self.sock, data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print ' Desconectando ...'
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()
                            
            except KeyboardInterrupt:
                print ' Interrumpido ...'
                self.sock.close()
                break
            
            
if __name__ == "__main__":
    import sys

    if len(sys.argv)<3:
        sys.exit('Uso: %s  chatid   host   port.no' % sys.argv[0])
        
    client = ChatClient(sys.argv[1],sys.argv[2], int(sys.argv[3]))
    client.cmdloop()

 


