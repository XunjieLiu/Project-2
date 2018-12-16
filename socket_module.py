import threading
from socket import *
from random import *
from threading import Lock
from DV_Demo import *

def test():
    lock = Lock()
    temp_list = []

    class add(threading.Thread):
        def _init__(self):
            threading.Thread.__init__(self)

        def run(self):
            counter = 0

            while counter < 20:     
                random_num = random() * 10
                lock.acquire()
                temp_list.append(random_num)
                lock.release()
                counter+=1
                print(temp_list)
                print('this is add')

    class delete(threading.Thread):
        def _init__(self):
            threading.Thread.__init__(self)

        def run(self):
            counter = 0
            while counter < 20:
                print("value")
                lock.acquire() 
                try:
                    temp_list.pop()
                except Exception as e:
                    print("It is empty!")

                lock.release()
                print(temp_list)
                counter+=1
                print('This is delete')

    thread1 = add()
    thread2 = delete()

    thread1.start()
    thread2.start()

# test()

for i in range(5): 
    client_socket = get_client_socket(12001)
    client_socket.sendall(b'Hello!')
    client_socket.close()





    