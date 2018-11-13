import socket
import sys
import select
import argparse 

#    print('Ejemplo: python2 cliente_chat.py ip puerto')

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor")
parser.add_argument("-s", "--server", help="Nombre del servidor")
args = parser.parse_args()
 
enqueport = 10000
_serv  = "127.0.0.1"

if args.port:
    print "Conectarse al puerto: ", args.port
    enqueport = args.port


if args.server:
    print "El nombre del servidor es: ", args.server
    _serv = args.server


timeout_in_seconds=60
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print
print >>sys.stderr, 'Conectando a %s Puerto %d' % (_serv, enqueport)
print "\n Para terminar, ingrese 'Exit' ..."
print
nombre = raw_input("Ingrese tu nombre :")

cliente.connect(( _serv, enqueport))
cliente.sendall(nombre)


while True:
    mensaje = raw_input(nombre + "> ")
    cliente.sendall(mensaje)
    if mensaje=='Exit':
        break

    ready = select.select([cliente], [], [], timeout_in_seconds)
    if ready[0]:
        respuesta = cliente.recv(1024)
        if respuesta == "Exit":
            print ('Servidor> '+ respuesta)
            break

        else:
            print ('Servidor> '+ respuesta)
    else:
        break

print("Sesion finalizada")
cliente.close()


