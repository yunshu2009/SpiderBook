#coding:utf-8

# 1. threading模块创建多线程
'''
import random
import time, threading

# 创建线程的第一种方式：将一个函数传入并创建Thread实例，然后调用start方法开始执行


def thread_run(urls):
    print 'Current %s is running...' % threading.current_thread().name
    for url in urls:
        print '%s ---->>> %s' % (threading.current_thread().name,url)
        time.sleep(random.random())
    print '%s ended.' % threading.current_thread().name


print '%s is running...' % threading.current_thread().name
t1 = threading.Thread(target=thread_run, name='Thread_1',args=(['url_1','url_2','url_3'],))
t2 = threading.Thread(target=thread_run, name='Thread_2',args=(['url_4','url_5','url_6'],))
t1.start()
t2.start()
t1.join()
t2.join()
print '%s ended.' % threading.current_thread().name
'''
'''
MainThread is running...
Current Thread_2 is running...
Thread_2 ---->>> url_4
Thread_2 ---->>> url_5
Thread_1 ---->>> url_2
Thread_2 ---->>> url_6
Thread_1 ---->>> url_3
Thread_1 ended.
Thread_2 ended.
MainThread ended.
'''


# 通过从threading.Thread继承创建线程类的方式
''''
import random
import threading
import time


class myThread(threading.Thread):
    def __init__(self,name,urls):
        threading.Thread.__init__(self,name=name)
        self.urls = urls

    def run(self):
        print('Current %s is running...' % threading.current_thread().name)
        for url in self.urls:
                print('%s ---->>> %s' % (threading.current_thread().name,url))
                time.sleep(random.random())
        print('%s ended.' % threading.current_thread().name)
        print('%s is running...' % threading.current_thread().name)


t1 = myThread(name='Thread_1',urls=['url_1','url_2','url_3'])
t2 = myThread(name='Thread_2',urls=['url_4','url_5','url_6'])
t1.start()
t2.start()
t1.join()
t2.join()
print('%s ended.' % threading.current_thread().name)
'''

'''
运行结果：
Current Thread_1 is running...
Thread_1 ---->>> url_1
Current Thread_2 is running...
Thread_2 ---->>> url_4
Thread_1 ---->>> url_2
Thread_2 ---->>> url_5
Thread_1 ---->>> url_3
Thread_2 ---->>> url_6
Thread_2 ended.
Thread_2 is running...
Thread_1 ended.
Thread_1 is running...
MainThread ended.
'''

# 线程同步

import threading
mylock = threading.RLock()
num=0


class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self,name=name)

    def run(self):
        global num
        while True:
            mylock.acquire()
            print('%s locked, Number: %d'%(threading.current_thread().name, num))
            if num>=4:
                mylock.release()
                print('%s released, Number: %d'%(threading.current_thread().name, num))
                break
            num+=1
            print('%s released, Number: %d'%(threading.current_thread().name, num))
            mylock.release()

'''
运行结果：
Thread_1 locked, Number: 0
Thread_1 released, Number: 1
Thread_1 locked, Number: 1
Thread_1 released, Number: 2
Thread_1 locked, Number: 2
Thread_1 released, Number: 3
Thread_1 locked, Number: 3
Thread_1 released, Number: 4
Thread_1 locked, Number: 4
Thread_1 released, Number: 4
Thread_2 locked, Number: 4
Thread_2 released, Number: 4
'''

if __name__== '__main__':
    thread1 = myThread('Thread_1')
    thread2 = myThread('Thread_2')
    thread1.start()
    thread2.start()