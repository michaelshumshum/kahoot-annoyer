import os
os.sys.path.append('/usr/local/lib/python3.9/site-packages')
os.popen('reset')
import time
import sys
from threading import *
from pyfiglet import Figlet
import queue

from _token import *
from _payload import *
from _functions import *
from _bots import *
from _ui import *

q = queue.Queue()

f = Figlet(font='ogre')
time.sleep(1)
print('==========================================================================')
print(f.renderText('kahoot annoyer'))
print("Created by michaelshumshum\nBased on msemple's kahoot-hack and theusaf's kahootPY\nPress ctrl+c to exit. You may need to reset the screen if the terminal gets messed up.")
print('==========================================================================')
time.sleep(0.5)
while True:
    try:
        pin = sys.argv[1]
        count = int(sys.argv[2])
        prefix = sys.argv[3]
    except:
        pin = input('PIN:')
        while True:
            try:
                count = int(input('How many:'))
                break
            except:
                print('Please put a valid number')
        prefix = input('Custom name (leave blank if no):')
        if prefix == '':
            prefix = 'bot'

    names = gen_names(prefix,count+1)
    ids = []
    for i in range(count+1):
        ids.append(i)

    m_bot = mothership(name='testtesttest',pin=pin,ackId=999999,queue=q,bot_names=names)
    if m_bot.connect() == 'error':
        print('PIN is incorrect or your internet connection is bad')
    else:
        break

def guifunc(*args):
    f = Form(name='kahoot-annoyer')
    while True:
        f.update_values(q)
        f.display()
def wrapper(q):
    print(npyscreen.wrapper_basic(guifunc))

threads = []

m_bot = mothership(name=names[-1],pin=pin,ackId=ids[-1],queue=q,bot_names=names)
thread = Thread(target=m_bot.run,name='mothership')
threads.append(thread)
thread.start()
print(f'Started thread {thread}')

for i in range(count):
    f_bot = bot(name=names[i],pin=pin,ackId=ids[i],queue=q)
    thread = Thread(target=f_bot.run,name=names[i])
    threads.append(thread)
    thread.start()
    time.sleep(0.01)
    print(f'Started thread {thread}')

q.put(['gui',count+1,'init',pin,names[-1]])
thread = Thread(target=wrapper,args=(q,),name='gui')
threads.append(thread)
thread.start()
print(f'Started thread {thread}')

for thread in threads:
    thread.join()
