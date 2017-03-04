#!/usr/bin/python3
import socket
import random

"""Operacion suma poniendo en URL 'operando+operando'"""

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.

Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1235))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

try:
    while True:
        # Creo el numero aleatorio
        num_aleatorio = str(random.randint(0, 999999999))
        print ('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print ('Request received:')
        # pasar de bytes a utf-8
        peticion = recvSocket.recv(2048).decode("utf-8", "strict")
        print (peticion)

        pagina = "http://localhost:1235/" + num_aleatorio
        recvSocket.send(
            bytes(
                "HTTP/1.1 301 \r\n\r\n" +
                "<html><meta http-equiv= 'Refresh'" +
                "content =5;url=" + pagina +
                "><body><h1>Hola</h1></body></html>" +
                "\r\n" +
                "<html><body><p> Vas a ser redirigido en 5 segundos" +
                " a la pagina: " + pagina +
                "</p></body></html>", "utf-8"
                )
            )
        recvSocket.close()
except KeyboardInterrupt:
    print ("Closing binded socket")
    mySocket.close()
