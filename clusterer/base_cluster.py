from multiprocessing.managers import SyncManager
from queue import Queue
from .utils import *
import sys

# ########## Server ##############################################################################

# class ClusterServer:

#     def __init__(self, port, authkey,broadcast):
#         self.queues = {}
#         self.ip = get_ip_address()
#         self.port = port
#         self.address = (self.ip, self.port)
#         self.authkey = authkey
#         self.manager = SyncManager(address=('',port),authkey=authkey)
#         self.server = self.manager.get_server()

#         if broadcast:
#             self.comm_server = _thread.start_new_thread(self.comm_server,(port+1,))

#     def configure(self,queues):
#         # Handle closure issue due to lambda.
#         def register(manager,element,ele_q):
#             manager.register(element,callable=lambda:ele_q)
        
#         for element in queues:
#             ele_q = Queue()
#             register(self.manager,element,ele_q)
#             self.queues[element] = ele_q

#     def runserver(self):
#         print('Queue manager is serving on ',self.address)
#         self.server.serve_forever()
        
#     def shutdown(self):
#         self.server.shutdown()

#     def comm_server(self,port):
#         # Create a TCP/IP socket
#         # from socket import *
#         sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
#         sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
#         sock.bind( ("", port) )

#         while 1:
#             (rs,ws,es)=select.select([sock],[],[],1)
#             if sock in rs:
#                 (data, addr) = sock.recvfrom(9999)
#                 if data == self.authkey:
#                     sock.sendto(str(self.address).encode(),addr)
#             else:
#                 pass



# ############# Client ##########################################################################

# class ClusterClient:
#     def __init__(self, server_ip='',server_port=0, authkey=''):
#         self.queues = {}
#         self.ip = get_ip_address()
#         self.manager = SyncManager
#         self.server_address = (server_ip,server_port)
#         self.authkey = authkey
#         self.findserver(self.server_address[1],authkey)
#         if self.server_address[0] != '':
#             self.connect()


#     def connect(self):
#         print(self.server_address)
#         self.manager = SyncManager(address=self.server_address,authkey=self.authkey)
#         self.manager.connect()
#         print('Connected to queue manager')


#     def configure(self,queues):
#         for element in queues:
#             self.manager.register(element)
#             ele_q = getattr(self.manager,element)()
#             self.queues[element] = ele_q
    

#     def process(self,func,args,num_process=1):

#         def HandleList(args):
#             _args = []
#             for arg in args:
#                 __args = ()
#                 for a in arg:
#                     __args = __args + (self.queues[a],)
#                 _args.append(__args)
            
#             return _args

#         if type(func) is list:
#             assert type(args) is list,'Expected args to be list'
#             assert type(num_process) is list,'Expected num_processes to be list'
#             _args = HandleList(args)

#         else:
#             _args = ()
#             for arg in args:
#                 _args = _args + (self.queues[arg],)
        
#         SpawnProcesses(func,_args,num_process)


#     def findserver(self,server_port,authkey):
#         sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
#         sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
#         sock.settimeout(5.0)
#         sock.sendto(authkey, ("<broadcast>", server_port+1) )

#         from ast import literal_eval
#         try:
#             server_address = sock.recv(9999)
#             server_address = literal_eval(server_address.decode())
#             self.server_address = server_address
#         except:
#             print('Server is not found. Make sure its active.')
#             print('Exiting')
#             exit(1)
        

########## Server ##############################################################################

class BaseServer:

    def __init__(self, port, authkey):
        self.queues = {}
        self.ip = get_ip_address()
        self.port = port
        self.address = (self.ip, self.port)
        self.authkey = authkey
        self.manager = SyncManager(address=('',port),authkey=authkey)
        self.server = self.manager.get_server()

    def configure(self,queues):
        # Handle closure issue due to lambda.
        def register(manager,element,ele_q):
            manager.register(element,callable=lambda:ele_q)
        
        for element in queues:
            ele_q = Queue()
            register(self.manager,element,ele_q)
            self.queues[element] = ele_q

    def runserver(self):
        print('Queue manager is serving on ',self.address)
        self.server.serve_forever()
        
    def shutdown(self):
        self.server.shutdown()



############# Client ##########################################################################

class BaseClient:
    def __init__(self, server_address, authkey):
        self.queues = {}
        self.ip = get_ip_address()
        self.manager = SyncManager
        self.server_address = server_address
        self.authkey = authkey
        self.connect()

    def connect(self):
        self.manager = SyncManager(address=self.server_address,authkey=self.authkey)
        self.manager.connect()
        print('Connected to queue manager')


    def configure(self,queues):
        for element in queues:
            self.manager.register(element)
            ele_q = getattr(self.manager,element)()
            self.queues[element] = ele_q
    

    def process(self,func,args,num_process=1):

        def HandleList(args):
            _args = []
            for arg in args:
                __args = ()
                self.configure(arg)
                for a in arg:
                    __args = __args + (self.queues[a],)
                _args.append(__args)
            
            return _args

        if type(func) is list:
            assert type(args) is list,'Expected args to be list'
            assert type(num_process) is list,'Expected num_processes to be list'
            assert len(func) == len(args) == len(num_process),'len(func)!= len(args) or len!=len(num_process)'
            _args = HandleList(args)

        else:
            _args = ()
            self.configure(args)
            for arg in args:
                _args = _args + (self.queues[arg],)
        
        SpawnProcesses(func,_args,num_process)
