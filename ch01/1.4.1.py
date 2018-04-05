# coding:utf-8

# 第一种方式：使用os模块中的fork方式实现多进程
'''
import os
if __name__ == '__main__':
    print('current Process (%s) start ...' % (os.getpid()))
    pid = os.fork()
    if pid < 0:
        print('error in fork')
    elif pid == 0:
        print('I am child process(%s) and my parent process is (%s)' % (os.getpid(),os.getppid()))
    else:
        print('I(%s) created a chlid process (%s).' % (os.getpid(),pid))
'''
'''
输出结果：
current Process (19821) start ...
I(19821) created a chlid process (19822).
I am child process(19822) and my parent process is (19821)
'''
''''
# 第二种方法：使用multiprocessing模块创建多进程
import os
from multiprocessing import Process

# 子进程要执行的代码


def run_proc(name):
    print('Child process %s (%s) Running...' % (name, os.getpid()))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p_list=[]
    for i in range(5):
        # 使用Process创建进程时，需要传入一个执行函数和参数的参数
        p = Process(target=run_proc, args=(str(i),))
        p_list.append(p)
        print('Process will start.')
        # 使用start方法启动进程
        p_list[i].start()
    for p in p_list:
        # 使用join方法实现进程的同步
        p.join()
    print('Process end.')
'''
'''
运行结果：
Parent process 20379.
Process will start.
Process will start.
Process will start.
Child process 0 (20380) Running...
Process will start.
Child process 1 (20381) Running...
Process will start.
Child process 2 (20382) Running...
Child process 3 (20383) Running...
Child process 4 (20384) Running...
'''

# multiprocessing模块提供了一个Pool类来代表进程池对象
'''
from multiprocessing import Pool
import os, time, random


def run_task(name):
    print('Task %s (pid = %s) is running...' % (name, os.getpid()))
    time.sleep(random.random() * 3)
    print('Task %s end.' % name)


if __name__=='__main__':
    print 'Current process %s.' % os.getpid()
    # 创建容量为3的进程池，默认为CPU核数
    p = Pool(processes=3)
    # 向进程池中添加5个任务
    for i in range(5):
        p.apply_async(run_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    # 等待所有的子进程执行完毕
    p.join()
    print 'All subprocesses done.'
'''
'''
结果是：
Current process 1407.
Waiting for all subprocesses done...
Task 0 (pid = 1408) is running...
Task 1 (pid = 1409) is running...
Task 2 (pid = 1410) is running...
Task 1 end.
Task 3 (pid = 1409) is running...
Task 2 end.
Task 4 (pid = 1410) is running...
Task 4 end.
Task 0 end.
Task 3 end.
All subprocesses done.
'''

# Queue进程间通信 - 用于多个进程间通信
'''
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:


def proc_write(q,urls):
    print('Process(%s) is writing...' % os.getpid())
    for url in urls:
        q.put(url)
        print('Put %s to queue...' % url)
        time.sleep(random.random())


# 读数据进程执行的代码:
def proc_read(q):
    print('Process(%s) is reading...' % os.getpid())
    while True:

        url = q.get(True)
        print('Get %s from queue.' % url)


if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    proc_writer1 = Process(target=proc_write, args=(q,['url_1', 'url_2', 'url_3']))
    proc_writer2 = Process(target=proc_write, args=(q,['url_4','url_5','url_6']))
    proc_reader = Process(target=proc_read, args=(q,))
    # 启动子进程proc_writer，写入:
    proc_writer1.start()
    proc_writer2.start()
    # 启动子进程proc_reader，读取:
    proc_reader.start()
    # 等待proc_writer结束:
    proc_writer1.join()
    proc_writer2.join()
    # proc_reader进程里是死循环，无法等待其结束，只能强行终止:
    proc_reader.terminate()
'''
'''
运行结果：
rocess(1697) is writing...
Process(1696) is writing...
Put url_4 to queue...
Put url_1 to queue...
Process(1698) is reading...
Get url_4 from queue.
Get url_1 from queue.
Put url_2 to queue...
Get url_2 from queue.
Put url_5 to queue...
Get url_5 from queue.
Put url_3 to queue...
Get url_3 from queue.
Put url_6 to queue...
Get url_6 from queue.
'''


# pipe进程间通信

import multiprocessing
import random
import time,os


def proc_send(pipe,urls):
    for url in urls:
        print "Process(%s) send: %s" %(os.getpid(),url)
        pipe.send(url)
        time.sleep(random.random())


def proc_recv(pipe):
    while True:
        print "Process(%s) rev:%s" %(os.getpid(),pipe.recv())
        time.sleep(random.random())

if __name__ == '__main__':
    # Pipe()返回(conn1, conn2)代表一个管道的两端。参数duplex默认为True值，表示这个管道是全双工模式，这时conn1和conn2
    # 均可收发
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc_send, args=(pipe[0], ['str_'+str(i) for i in range(10)]))
    p2 = multiprocessing.Process(target=proc_recv, args=(pipe[1], ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

'''
运行结果：
Process(2007) send: str_0
Process(2008) rev:str_0
Process(2007) send: str_1
Process(2008) rev:str_1
Process(2007) send: str_2
Process(2008) rev:str_2
Process(2007) send: str_3
Process(2007) send: str_4
Process(2008) rev:str_3
Process(2008) rev:str_4
Process(2007) send: str_5
Process(2007) send: str_6
Process(2007) send: str_7
Process(2008) rev:str_5
Process(2007) send: str_8
Process(2007) send: str_9
'''