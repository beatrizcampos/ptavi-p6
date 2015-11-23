#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

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
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(((IP, int(PORT))), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
