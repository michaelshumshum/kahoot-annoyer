import requests
import random
from threading import Thread
from queue import Queue
from datetime import datetime

pins = []
for i in range(0,10000000):
    x = str(i)
    g = 7 - len(x)
    y = ('0' * g) + x
    pins.append(y)
for i in range(0,1000000):
    x = str(i)
    g = 6 - len(x)
    y = ('0' * g) + x
    pins.append(y)

random.shuffle(pins)

def search(pins,queue):
    while True:
        random.shuffle(pins)
        for pin in pins:
            epoch = int(datetime.now().strftime("%s"))
            while True:
                try:
                    r = requests.get(f'https://kahoot.it/reserve/session/{pin}/?{epoch}')
                    break
                except:
                    continue
            if r.status_code == 200:
                queue.put(pin)

q = Queue()
threads = []

def recv(queue,):
    while True:
        found = queue.get()
        print('Found game with code ' + found)

thread = Thread(target=recv,args=(q,))
threads.append(thread)
thread.start()

for i in range(0,200):
    chunk = pins[:55000]
    del pins[:55000]
    thread = Thread(target=search,args=(list(chunk),q,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
