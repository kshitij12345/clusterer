from clusterer import ProtocolServer
from clusterer import BaseServer
from functions import *

functions_dict = {}
functions_dict['Generate'] = [Generate,['gen2sq_q'],1]
functions_dict['Square'] = [Square,['gen2sq_q','sq2sub_q'],1]
functions_dict['Subtract1'] = [Subtract1,['sq2sub_q','sub2pr_q'],1]
functions_dict['Print'] = [Print,['sub2pr_q'],1]


class Scheduler:
    def schedule(self,info,functions):
        return [functions['Generate'],functions['Square'],functions['Subtract1'],functions['Print']]

cluster_server = BaseServer(50000,b'chironx')
cluster_server.configure(['gen2sq_q','sq2sub_q','sub2pr_q'])


c = ProtocolServer(50000,cluster_server,functions_dict,Scheduler())

