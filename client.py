#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
try:

    METHOD = sys.argv[1]
    RECEIVER = sys.argv[2].split('@')[0]
    IP = sys.argv[2].split('@')[1].split(':')[0]
    PORT = sys.argv[2].split('@')[1].split(':')[1]

except IndexError:
    print("Usage: python client.py method receiver@IP:SIPport")

# Contenido que vamos a enviar (peticion SIP: INVITE sip:receptor@IP SIP/2.0)
LINE = METHOD + ' sip:' + RECEIVER + '@' + IP + ' SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, int(PORT)))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

# Metodo de asentimiento. Se envia de manera automática
rcv_answer = data.decode('utf-8').split('\r\n\r\n')[0:-1]
if rcv_answer == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ringing',
                  'SIP/2.0 200 OK']:
    METHOD = 'ACK'
    LINE_ACK = METHOD + ' sip:' + RECEIVER + '@' + IP + ' SIP/2.0\r\n\r\n'
    print("Enviando: " + LINE_ACK)
    my_socket.send(bytes(LINE_ACK, 'utf-8'))
    data = my_socket.recv(1024)
    print(data)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
