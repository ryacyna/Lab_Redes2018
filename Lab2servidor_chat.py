import socket
import sys
import select

arglen=len(sys.argv)
if arglen<2:
    print('Ejemplo: python2 servidor_chat.py 5000')
    exit()

puerto=int(sys.argv[1])

timeout_in_seconds=60

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(("", puerto))
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



