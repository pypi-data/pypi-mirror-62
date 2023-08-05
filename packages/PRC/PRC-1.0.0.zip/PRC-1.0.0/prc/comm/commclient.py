from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import bytes
from . import comm
import socket
import time

######################################################################################
################################### Classes ##########################################
######################################################################################

class CommClientException(comm.CommException): pass

class CommClient(comm.Comm):
    """
        This class is responsible for Client communication

        Constants:

        Variables:
        socket_reference    - socket handle
        connection_attempt  - Number of connection retry
    """
    def __init__(self):
        self.open()
        self.connection_attempt = 1

    def connect(self,ip,port):
        """
            This function connects to ip on port.
            It retrys MAX_RETRY times.

            Variables:
            ip          - Ip address
            port        - port

            Returns:
            Nothing
        """
        try:
            self.socket_reference.connect((ip, port))
        except socket.error:
            self.close()
            reload(socket)
            raise CommClientException("Cannot connect to " + ip + ":" + str(port))

    def _lowLevelRecv(self,buffer):
        """
            Low level receive function.

            Input:
            buffer  - Buffer size

            Returns:
            Received data
        """
        try: 
            data = self.socket_reference.recv(buffer)
        except socket.error as error: 
            raise CommClientException(str(error))

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
      
        try: 
            size = self.socket_reference.send(data)
        except socket.error as error: 
            raise CommClientException(str(error)) 
        
        return  size

    def _lowLevelClose(self):
        """
            Low level close function.

            Input:
            Nothing

            Returns:
            Nothing
        """
        self.socket_reference.close()

    def _lowLevelOpen(self):
        """
            Low level open function.

            Input:
            Nothing

            Returns:
            Nothing
        """
        self.socket_reference = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

######################################################################################
################################### Functions ########################################
######################################################################################

def sendAndReceive(ip, port, data_to_send, retry=3):
    """
        This function sends and receives frames from server

        Input:
        data_to_send    - frame to send

        Returns:
        Received data
    """
    connection = CommClient()
    
    if isinstance(data_to_send, str):
        data_to_send = data_to_send.encode('ascii')
    
    try:
        connection.connect(ip, port)
        connection.send(data_to_send)
        data_received = connection.receive()
        connection.close()
    except comm.CommException as error:
        if retry == 0: 
            raise CommClientException(error)
        print(str(error) + "  Retrying ... " + str(retry))
        retry -= 1
        data_received = sendAndReceive(ip, port, data_to_send, retry)

    return data_received
