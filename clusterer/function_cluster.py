from .broadcast_cluster import BroadcastClient,BroadcastServer
import _thread,pickle
import socket
from socket import *
import _thread
import select
from .utils import ListFilesInDir,HashFile


class FunctionServer(BroadcastServer):
    def __init__(self,port,authkey,functions):
        self.comm_server = _thread.start_new_thread(self.comm_serv,(port+1,))
        super().__init__(port,authkey)
        self.functions = self.pickle_fuctions(functions)

    def pickle_fuctions(self,functions):
        for function in functions:
            functions[function] = pickle.dumps(functions[function])
        return functions

    def comm_serv(self,port):
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
                
                if data == b'send_func':
                    func_list = []
                    for key in self.functions:
                        func_list.append(self.functions[key])
                    sock.sendto(pickle.dumps(func_list),addr)
            else:
                pass


class FunctionClient(BroadcastClient):
    def __init__(self,server_port,authkey):
        super().__init__(server_port,authkey)
        funcs,args,num_process = self.get_function(self.server_address)
        self.process(funcs,args,num_process)

    def get_function(self,server_address):
        sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.settimeout(5.0)
        sock.sendto('send_func'.encode(), (server_address[0],server_address[1]+1) )

        import pickle
        
        pickled_funcs = sock.recv(9999)
        funcs = pickle.loads(pickled_funcs)
        func = []
        arg = []
        num_process = []
        for _func in funcs:
            obj = pickle.loads(_func)
            func.append(obj[0])
            arg.append(obj[1])
            num_process.append(1)

        return func,arg,num_process