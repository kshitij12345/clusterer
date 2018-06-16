from .base_cluster import BaseClient,BaseServer
import socket
from socket import *
import _thread
import select


class BroadcastServer(BaseServer):
    def __init__(self,port,authkey):
        super().__init__(port,authkey)
        try:
            self.comm_server = _thread.start_new_thread(self.comm_server,(port+1,))
        except:
            pass

    
    def comm_server(self,port):
        # Create a TCP/IP socket
        # from socket import *
        sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.bind( ("", port) )
        while 1:
            (rs,ws,es)=select.select([sock],[],[],1)
            if sock in rs:
                (data, addr) = sock.recvfrom(9999)
                if data == self.authkey:
                    sock.sendto(str(self.address).encode(),addr)
            else:
                pass

class BroadcastClient(BaseClient):
        def __init__(self,server_port,authkey):
            server_address = self.findserver(server_port,authkey)
            super().__init__(server_address,authkey)


        def findserver(self,server_port,authkey):
            sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            sock.settimeout(5.0)
            sock.sendto(authkey, ("<broadcast>", server_port+1) )

            from ast import literal_eval
            try:
                server_address = sock.recv(9999)
                server_address = literal_eval(server_address.decode())
                return server_address
            except:
                print('Server is not found. Make sure its active.')
                print('Exiting')
                exit(1)

