import socket
import sys
import select
import argparse 


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

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(( _serv, enqueport))
servidor.listen(1)

print ' Esperando para conectarse'

cliente, cliente_addr = servidor.accept()

cliente.setblocking(0)

print "\n Para terminar ingrese 'Exit' ..."
print '\n Conexion desde', cliente_addr

preparado = select.select([cliente], [], [], timeout_in_seconds)
if preparado[0]:
    nombre = cliente.recv(4096)

while True:
    preparado = select.select([cliente], [], [], timeout_in_seconds)
    if preparado[0]:
        recibido = cliente.recv(4096)
        print (nombre +"> "+recibido)
	if recibido=='Exit':
            break
        mensaje_a_enviar= raw_input("Servidor> ")
        cliente.sendall(mensaje_a_enviar)
	if mensaje_a_enviar=='Exit':
            break
	
    else:
        cliente.sendall("Exit")
        cliente.close()
        break

servidor.close()



