#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:

    IP = sys.argv[1]
    PORT = sys.argv[2]
    FILE = sys.argv[3]

except IndexError:
    print("Usage: python server.py IP port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP_CLIENT = str(self.client_address[0])
        print("LA IP DEL CLIENTE ES: " + IP_CLIENT)
        #self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            method_client = line.decode('utf-8').split(' ')[0]
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

            print("El cliente nos manda " + line.decode('utf-8'))
            if not method_client in methods:
                answer = ("SIP/2.0 405 Method Not Allowed" + '\r\n\r\n')
                self.wfile.write(bytes(answer, 'utf-8'))

            elif method_client == 'INVITE':
                rcv_answer = ("SIP/2.0 100 Trying" + '\r\n\r\n' +
                              "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                              "SIP/2.0 200 OK" + '\r\n\r\n')
                self.wfile.write(bytes(rcv_answer, 'utf-8'))

            elif method_client == 'BYE':
                answer = ("SIP/2.0 200 OK" + '\r\n\r\n')
                self.wfile.write(bytes(answer, 'utf-8'))
                print("Finish. . .")

            elif method_client == 'ACK':
                aEjecutar = ('./mp32rtp -i ' +
                             IP_CLIENT + ' -p 23032 < ' + FILE)
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)

            else:
                answer = ("SIP/2.0 400 Bad Request" + '\r\n\r\n')
                self.wfile.write(bytes(answer, 'utf-8'))


if __name__ == "__main__":
    """
    Creamos servidor eco y escuchamos
    """
    methods = ['INVITE', 'ACK', 'BYE']
    serv = socketserver.UDPServer(((IP, int(PORT))), EchoHandler)
    print("Listening...")
    serv.serve_forever()
