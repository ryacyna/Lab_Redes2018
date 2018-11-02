 
import socket
 

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost',8000))
 

nombrecliente = raw_input('Cual es su nombre Cliente ? ') 


while 1:
    data = raw_input("'Exit' para terminar - "+nombrecliente+' > ') 
    clientsocket.send( nombrecliente+' > '+  data) 
    if 'Exit' in data:
        break 

    newdata = clientsocket.recv(1024) 
    print  newdata 


clientsocket.close() 


