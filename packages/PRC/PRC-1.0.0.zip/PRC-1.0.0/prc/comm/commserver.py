from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
import socketserver
import socket
from . import comm

################################################################################
################################### Constants ##################################
################################################################################
REQUEST_QUEUE_SIZE = 10

################################################################################
################################### Classes ####################################
################################################################################


class CommServerException(comm.CommException): 
    pass

    
class CommServer(socketserver.BaseRequestHandler, comm.Comm):
    """
        This class is responsible for Server communication
        A thread that servs client

        Constants:


        Variables:
    """

    def handle(self):
        """
            This function handles all communication from clients
            Default CommServer behavior is to do communication loop back.
            This function should be overloaded

            Input:
            Nothing

            Returns:
            Nothing
        """
        data = self.receive()
        self.send(data)
        self.close()

    def _lowLevelRecv(self,buffer):
        """
            Low level receive function.

            Input:
            buffer  - Buffer size

            Returns:
            Received data
        """
        try: 
            data = self.request.recv(buffer)
        except socket.error as error: 
            raise CommServerException(str(error))
        
        if isinstance(data, bytes):
            data = data.decode()
        
        return data

    def _lowLevelSend(self,data):
        """
            Low level send function.

            Input:
            data    - data to send

            Returns:
            Send data size
        """
        if isinstance(data, str):
            data = data.encode("ascii")
        
        try: size = self.request.send(data)
        except socket.error as error: raise CommServerException(str(error))

        return size

    def _lowLevelClose(self):
        """
            Low level close function.

            Input:
            Nothing

            Returns:
            Nothing
        """
        self.request.close()

################################################################################
################################### Functions ##################################
################################################################################

def server_factory(ip,port,request_handler,socket_server=None):
    """
        Prepares Socket server

        Input:
        ip                  - Server address
        port                - Server port
        request_handler     - Request handler function
        socket_server       - Custom Socket server class

        Returns:
        Server handle
    """
    class Handler(CommServer): 
        handle = request_handler

    socket_server = socket_server if socket_server else socketserver.ThreadingTCPServer

    socket_server.request_queue_size=3
    try:
        server_handle = socket_server((ip,port),Handler)
    except socket.error as error:
        raise CommServerException(str(error))

    return server_handle
