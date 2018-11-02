#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys


import argparse
 
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
parser.add_argument("-s", "--server", help="Dirección IP del Servidor")

args = parser.parse_args()
 
enqueport = 10000
servidor  = 'localhost'

# Aquí procesamos lo que se tiene que hacer con cada argumento
if args.port:
    print "Conectarse al puerto: ", args.port
    enqueport = args.port

if args.server:
    print "Direccion del Servidor: ", args.server
    servidor = args.server

if args.file:
    print "El nombre de archivo a procesar es: ", args.file




# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (servidor, enqueport)
message = ' Mensaje a enviar ...'


while(1) :
    message = raw_input('Ingrese mensaje a enviar (Termina con "FIN" ): ')
   
    # Send data
    print >>sys.stderr, 'Enviando "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    print >>sys.stderr, ' Esperando recepcion '
    data, server = sock.recvfrom(4096)

    print >>sys.stderr, ' Recibido  "%s"' % data

    if message=="FIN":
        break



print >>sys.stderr, 'Cerrando  socket'
sock.close()
