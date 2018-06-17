from clusterer.wrappers import io_wrap,i_wrap,o_wrap
import random
import time
from time import gmtime, strftime


# def Generate(input_queue):
#     while True:
#         number = random.randint(1,10)
#         print({'number':number,'time':strftime("%Y-%m-%d %H:%M:%S", gmtime())})
#         input_queue.put({'number':number,'time':strftime("%Y-%m-%d %H:%M:%S", gmtime())})
#         time.sleep(2)
@i_wrap
def Generate():
    time.sleep(2)
    number = random.randint(1,10)
    _time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print({'time':_time,'number':number})
    return {'time':_time,'number':number}

# def Cube(input_queue,output_queue):
#     while True:
#         if (not input_queue.empty()):
#             number = input_queue.get()
#             print(number,'from Cube')
#             out = number*number*number
#             output_queue.put(out)
@io_wrap
def Cube(x):
    print('Cube Got',x)
    return x*x*x

# def Square(input_queue,output_queue):
#     while True:
#         if (not input_queue.empty()):
#             number = input_queue.get()
#             print(number,'from Square',number['number']*number['number'],'to Cube')
#             number = number['number']
#             out = number*number
#             output_queue.put(out)
@io_wrap
def Square(x):
    print('Sqare',x)
    x = x['number']
    return x*x

@io_wrap
def Subtract1(x):
    print('Subtract',x)
    return x-1

@o_wrap
def Print(x):
    print('Print',x)