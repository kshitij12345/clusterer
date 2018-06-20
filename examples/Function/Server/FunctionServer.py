from clusterer import ProtocolServer
from clusterer import BaseServer
from functions import *
from clusterer import PipelineReplicate

functions_dict = {}
functions_dict['Generate'] = [Generate,['gen2sq_q'],1]
functions_dict['Square'] = [Square,['gen2sq_q','sq2sub_q'],1]
functions_dict['Subtract1'] = [Subtract1,['sq2sub_q','sub2pr_q'],1]
functions_dict['Print'] = [Print,['sub2pr_q'],1]

cluster_server = BaseServer(50000,b'password')
cluster_server.configure(['gen2sq_q','sq2sub_q','sub2pr_q'])

Scheduler = PipelineReplicate()

c = ProtocolServer(50000,cluster_server,functions_dict,Scheduler)

