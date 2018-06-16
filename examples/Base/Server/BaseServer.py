from clusterer import BaseServer

c = BaseServer(port=50000,authkey=b'password')
c.configure(['gen2sq_q','sq2sub_q','sub2pr_q'])
c.runserver()
