import time
import sys
import datetime
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
        prefix = sys.argv[3]
    except:
        prefix = 'bot'
    try:
        pin = sys.argv[1]
        count = int(sys.argv[2])
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
    style = input('Add style to the names (y/n):')
    if style == 'y':
        style = True
        glitchname = False
    else:
        style = False
        glitchname = input('Glitched names (y/n):')
        if glitchname == 'y':
            glitchname = True
        else:
            glitchname = False
    epoch = int(datetime.datetime.now().strftime("%s"))
    r = requests.get(f'https://kahoot.it/reserve/session/{pin}/?{epoch}')
    if r.status_code != 200:
        print('Incorrect PIN')
        continue
    names = gen_names(prefix,count,style,glitchname)

    ids = []
    for i in range(count):
        ids.append(i)
    break

def guifunc(*args):
    global active
    f = Form(name='kahoot-annoyer',FIX_MINIMUM_SIZE_WHEN_CREATED=False)
    f.update_values(q)
def wrapper(q):
    npyscreen.wrapper_basic(guifunc)

def main_thread(queue):
    while True:
        get = queue.get()
        if get[0] != 'main':
            queue.put(get)
        else:
            time.sleep(2)
            print('=======================================================')
            print(f'Quiz URL: https://create.kahoot.it/details/{get[1]}')
            print('=======================================================')
            break

threads = []
quizid = ''

thread = Thread(target=main_thread,args=(q,),name='main')
threads.append(thread)
thread.start()

manager = manager(queue=q,bot_names=names)
thread = Thread(target=manager.run,name='bot-manager')
threads.append(thread)
thread.start()

for i in range(count):
    f_bot = bot(name=names[i],pin=pin,ackId=ids[i],queue=q)
    thread = Thread(target=f_bot.run,name=names[i])
    threads.append(thread)
    thread.start()
    time.sleep(0.01)

q.put(['gui',count,'init',pin])
thread = Thread(target=wrapper,args=(q,),name='gui')
threads.append(thread)
thread.start()

for thread in threads:
    thread.join()
