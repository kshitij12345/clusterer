from clusterer import BroadcastServer

c = BroadcastServer(50000,b'password')
c.configure(['gen2sq_q','sq2sub_q','sub2pr_q'])
c.runserver()
