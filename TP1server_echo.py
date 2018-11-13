import socket
import argparse 


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor")
parser.add_argument("-s", "--server", help="Nombre del servidor")
args = parser.parse_args()
 
enqueport = 10000
servidor  = "127.0.0.1"

if args.port:
    print "Conectarse al puerto: ", args.port
    enqueport = args.port


if args.server:
    print "El nombre del servidor es: ", args.server
    servidor = args.server


# Stream = TCP
serversocket    =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(( servidor, enqueport ))
serversocket.listen(1)

nombreservidor = raw_input('Cual es su nombre Servidor ? ') 
archivo = open(nombreservidor, 'a')

print ''
print "Ejecute 'cliente_echo.py' en una nueva terminal ..."
print '' 

while True:
    print 'Esperando clientes ...'
    clientsocket, clientaddress = serversocket.accept()
    print 'Conexion desde: ', clientaddress 
    while 1:
        data = clientsocket.recv(1024) 
        print data

        if data:
            sent = clientsocket.send(nombreservidor+' > '+data) 

            if 'Exit' in data:
                clientsocket.close() 
                print 'Se cierra cliente ...'
                recibido = 'Fin cliente.------------- ' + '\n'
                archivo.write(recibido)
                recibido = '\n'
                archivo.write(recibido)
                break

            recibido = 'Datos: ' + data + '\n'
            archivo.write(recibido)


archivo.close()



