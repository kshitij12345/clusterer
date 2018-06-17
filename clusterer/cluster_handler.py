import pickle
import socket
import _thread
import select
from .utils import *
import os
from .base_cluster import BaseClient,BaseServer

########## Protocol Server #######################################################

class ProtocolServer:
    def __init__(self,port,cluster_server,functions,scheduler):
        self.cluster_server = cluster_server
        self.server_address = (get_ip_address(),port)
        self.authkey = cluster_server.authkey
        self.scheduler = scheduler
        self.functions = pickle_functions(functions)
        self.udp_listener = _thread.start_new_thread(self.server_broadcater,(port+1,))
        self.tcp_sock = self.TCP_LISTENER(port+2)
        self.tcp_listener = _thread.start_new_thread(self.await_connection,())
        self.handle = {b'get_func':self.get_func_handler,b'get_env':self.get_env_handler}
        cluster_server.runserver()
    
    def TCP_LISTENER(self,port):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(('',port))
        tcp_socket.listen(5)
        return tcp_socket

    def server_broadcater(self,port):
        # Create a UDP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind( ("", port) )

        while 1:
            (rs,ws,es)=select.select([sock],[],[],1)
            if sock in rs:
                (data, addr) = sock.recvfrom(9999)
                if data == self.authkey:
                    sock.sendto(str(self.server_address).encode(),addr)
            else:
                pass

    def await_connection(self):
        while True:
            print('Awaiting TCP connection on port',self.server_address[1]+2)
            (clientsocket,clientaddress) = self.tcp_sock.accept()
            _thread.start_new_thread(self.client_thread,(clientsocket,clientaddress))

    def client_thread(self,clientsocket,clientaddress):
        cmd = clientsocket.recv(1024)

        try:
            self.handle[cmd](clientsocket,clientaddress)
        except:
            print('incorrect request ',cmd)
            clientsocket.send(b'incorrect request '+cmd)
            clientsocket.close()
        # if cmd == b'get_env':
        #     self.get_env_handler(clientsocket,clientaddress)
        # elif cmd == b'get_func':
        #     self.get_func_handler(clientsocket,clientaddress)

    def get_env_handler(self,client_socket,client_address):
        files = ListFilesInDir(os.curdir)
        num_files = len(files)

        # Send the number of files
        client_socket.send(pickle.dumps(num_files))

        for i in range(0,num_files):
            # Receive file number to send
            num_index = client_socket.recv(1024)
            num_index = pickle.loads(num_index)
            client_socket.send(pickle.dumps(files[num_index]))
            data = client_socket.recv(1024)
            if data != b'ok':
                pass

            with open(files[num_index],'rb') as f:
                data = f.read()
                send_one_message(client_socket,data)

    def get_func_handler(self,client_socket,client_address):
        client_socket.send(b'ok')
        clienf_info = client_socket.recv(1024)

        func_list = self.scheduler.schedule(clienf_info,self.functions)

        send_one_message(client_socket,pickle.dumps(func_list))

        ack = client_socket.recv(9999)
        if ack == b'ok':
            pass

######## Protocol Client ######################################################

class ProtocolClient():
    def __init__(self,server_port,authkey):
        self.funcs = []
        self.args = []
        self.num_process = []
        self.server_address = self.find_server(server_port+1,authkey)
        self.cluster_client = BaseClient(self.server_address,authkey)
      
    def find_server(self,server_port,authkey):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(5.0)
        sock.sendto(authkey, ("<broadcast>", server_port) )

        from ast import literal_eval
        try:
            server_address = sock.recv(9999)
            server_address = literal_eval(server_address.decode())
            return server_address
        except:
            print('Server is not found. Make sure its active.')
            print('Exiting')          

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_address[0],self.server_address[1]+2))

    def run(self):
        self.get_env()
        self.get_func()
        self.cluster_client.process(self.funcs,self.args,self.num_process)      

    def get_env(self):
        self.connect()
        # Send get_env
        self.sock.send(b'get_env')

        # Receive number_of_files
        num_files = self.sock.recv(100)
        num_files = pickle.loads(num_files)
        
        for file in range(0,num_files):
            # Send file number to receive
            self.sock.send(pickle.dumps(file))

            # Receive file name
            path_name = self.sock.recv(9999)
            path_name = pickle.loads(path_name)
            file_handler = make_file(path_name)

            # Send ack.
            self.sock.send(b'ok')

            # Receive file data
            file_data = recv_one_message(self.sock)

            file_handler.write(file_data)
            file_handler.close()

    def get_func(self):
        
        def unpickle_func_data(pickled_data):
            funcs = pickle.loads(pickled_data)
            func = []
            arg = []
            num_process = []
            for _func in funcs:
                obj = pickle.loads(_func)
                func.append(obj[0])
                arg.append(obj[1])
                num_process.append(obj[2])

            return func,arg,num_process
        
        self.connect()

        # Send get_func
        self.sock.send(b'get_func')

        # Confirm acknowledgement
        ack = self.sock.recv(1024)

        # Send client info
        self.sock.send(b'1')

        # Receive pickled functions.
        pickled_data = recv_one_message(self.sock)
        
        self.funcs,self.args,self.num_process = unpickle_func_data(pickled_data)
