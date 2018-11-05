import socket
import sys
import select

arglen=len(sys.argv)
if arglen<3:
    print('Ejemplo: python2 cliente_chat.py ip puerto')
    exit()

addr=sys.argv[1]
port=int(sys.argv[2])

timeout_in_seconds=60
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print
print >>sys.stderr, 'Conectando a %s Puerto %d' % (addr, port)
print "\n Para terminar, ingrese 'Exit' ..."
print
nombre = raw_input("Ingrese tu nombre :")

cliente.connect((addr,port))
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


