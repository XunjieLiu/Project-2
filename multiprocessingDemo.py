from multiprocessing import Process

# 子进程要执行的代码
def f(name):
    print('hello ', name)

if __name__=='__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join() # join方法会让主进程等待子进程运行结束后再执行
    print('Child process end.')