from clusterer import BaseClient
from functions import *

if __name__=='__main__':
    c = BaseClient(('server_ip',50000),authkey=b'password')
    funcs = [Generate,Square,Subtract1,Print]
    args = [['gen2sq_q'],['gen2sq_q','sq2sub_q'],['sq2sub_q','sub2pr_q'],['sub2pr_q']]
    num_process = [1,1,1,1]
    
    c.process(funcs,args,num_process)
    #c.process(Generate,['gen2square_q'],1)