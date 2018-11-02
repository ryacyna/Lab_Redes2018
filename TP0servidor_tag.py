import socket
import sys
import argparse
 
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
args = parser.parse_args()
 
enqueport = 10000
#archivo   = 'Palabras_Recibidas.txt'
#archivo   = open(archivo, 'a')

# Aqui procesamos lo que se tiene que hacer con cada argumento. Sin son pasados.

if args.port:
    print "Conectarse al puerto: ", args.port
    enqueport = args.port


if args.file:
    print "El nombre de archivo a procesar es: ", args.file
    archivo = open(args.file, 'a')

print ""


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Relaciona con el puerto.
server_address = ('localhost', enqueport)

print >>sys.stderr, 'Iniciando en %s port %s' % server_address

sock.bind(server_address)

#El mensaje es leido usando recvfrom()

while True:
    print >>sys.stderr, '\n Esperando para recibir mensaje ... '
    data, address = sock.recvfrom(4096)
    
    print >>sys.stderr, 'Recibidos %s bytes desde %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'Envia %s bytes de regreso a %s' % (sent, address)
        
        if data=='FIN':
            break

	recibido = 'Datos: ' + data + '\n'

	archivo.write(recibido)


sock.close()

archivo.close()






