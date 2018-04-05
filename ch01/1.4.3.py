#coding:utf-8
# gevent的使用流程

'''
from gevent import monkey; monkey.patch_all()
import gevent
import urllib.request


def run_task(url):
    print('Visit --> %s' % url)
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        print('%d bytes received from %s.' % (len(data), url))
    except Exception as e:
        print(e)
if __name__=='__main__':
    urls = ['https://github.com/','https://www.python.org/','http://www.cnblogs.com/']
    # 形成协程
    greenlets = [gevent.spawn(run_task, url) for url in urls  ]
    # 添加协程任务，并且启动执行
    gevent.joinall(greenlets)
'''
'''
运行结果：
Visit --> https://github.com/
Visit --> https://www.python.org/
Visit --> http://www.cnblogs.com/
46366 bytes received from http://www.cnblogs.com/.
49278 bytes received from https://www.python.org/.
52755 bytes received from https://github.com/.
'''


# gevent pool对象使用

from gevent import monkey
monkey.patch_all()
import urllib.request
from gevent.pool import Pool
def run_task(url):
    print('Visit --> %s' % url)
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        print('%d bytes received from %s.' % (len(data), url))
    except Exception as e:
        print(e)
    return 'url:%s --->finish'% url

if __name__=='__main__':
    pool = Pool(2)
    urls = ['https://github.com/','https://www.python.org/','http://www.cnblogs.com/']
    results = pool.map(run_task,urls)
    print(results)

'''
运行结果：
Visit --> https://github.com/
Visit --> https://www.python.org/
49278 bytes received from https://www.python.org/.
Visit --> http://www.cnblogs.com/
46310 bytes received from http://www.cnblogs.com/.
52755 bytes received from https://github.com/.
['url:https://github.com/ --->finish', 'url:https://www.python.org/ --->finish', 'url:http://www.cnblogs.com/ --->finish']
'''