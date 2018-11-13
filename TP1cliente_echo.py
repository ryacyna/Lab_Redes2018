 
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

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((servidor, enqueport ))
 

nombrecliente = raw_input('Cual es su nombre Cliente ? ') 


while 1:
    data = raw_input("'Exit' para terminar - "+nombrecliente+' > ') 
    clientsocket.send( nombrecliente+' > '+  data) 
    if 'Exit' in data:
        break 

    newdata = clientsocket.recv(1024) 
    print  newdata 


clientsocket.close() 


