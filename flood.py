from threading import Thread, Event
from _bots import *
from sys import argv
from contextlib import suppress
import queue
q = queue.Queue()
e = Event()
e.set()


def check_code(pin):
    epoch = int(datetime.datetime.now().timestamp())
    r = requests.get(f'https://kahoot.it/reserve/session/{pin}/?{epoch}')
    if r.status_code != 200:
        return False
    return True

#### Command-arguments section ####


pin = None
count = None
interactive = False
prefix = "bot"
style = False
glitch_name = False
gui = True
verbose = False

args = argv[1:]
for i in range(len(args)):
    arg = args[i - 1].lower()
    if "-" in arg:
        if "h" in arg or '--help' in arg:
            print(r''' _   __      _                 _      ___
| | / /     | |               | |    / _ \
| |/ /  __ _| |__   ___   ___ | |_  / /_\ \_ __  _ __   ___  _   _  ___ _ __
|    \ / _` | '_ \ / _ \ / _ \| __| |  _  | '_ \| '_ \ / _ \| | | |/ _ | '__|
| |\  | (_| | | | | (_) | (_) | |_  | | | | | | | | | | (_) | |_| |  __| |
\_| \_/\__,_|_| |_|\___/ \___/ \__| \_| |_|_| |_|_| |_|\___/ \__, |\___|_|
                                                              __/ |
                                                             |___/           ''')
            print("Created by michaelshumshum\nBased on msemple's kahoot-hack and theusaf's kahootPY\nPress ctrl+c to exit or ctr+z to immediately abort. You may need to reset the screen if the terminal gets messed up.\n")
            print('usage: python3 flood.py -p <PIN> -b <# of bots> [optional arguments]\n')
            print('required arguments:\n-b: # of bots. depending on hardware, performance may be significantly affected at higher values.\n-p: code for kahoot game.\n')
            print('optional arguments:\n-h / --help: shows this help information.\n-i: input arguments in an "interactive" fashion.\n-t: disable terminal output.\n-n <name>: set a custom name. by default, name is "bot".\n-s: styled names.\n-g: glitched names (selecting glitched names will override custom name and styled name options).\n-v: verbose.\n')
            exit()
        if "v" in arg:
            print('INFO: Verbose mode ON')
            verbose = True
        if "i" in arg:
            print('INFO: Interactive mode ON')
            interactive = True
        if "g" in arg:
            glitch_name = True
            print("INFO: Glitched names ON")
        if "t" in arg:
            print("INFO: Output to terminal DISABLED.")
            gui = False
        if "s" in arg:
            if not glitch_name:
                style = True
                print("INFO: Styled names ON")
            else:
                print("WARN: -s and -g are conflicting arguments. Ignoring -s option.")
    if "-b" in arg:
        try:
            count = int(args[i])
            print(f"INFO: Using {count} bots.")
        except ValueError:
            print('ERR: Number of bots must be an integer.')
            exit()
    if "-n" in arg:
        if not glitch_name:
            prefix = args[i]
            print(f"INFO: The bots will be named a derivative of {prefix}.")
        else:
            print("WARN: -n and -g are conflicting arguments. Ignoring -n option.")
    if "-p" in arg:
        try:
            pin = int(args[i])
            if not check_code(pin):
                raise ValueError
            else:
                print(f"INFO: Using {pin} as the code.")
        except ValueError:
            print('ERR: Code is invalid!')
            exit()


if (pin and count) or interactive:
    pass
else:
    print('ERR: Missing arguments, use -h for help')
    exit()

if interactive:
    while True:
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
            glitch_name = False
        else:
            style = False
            glitch_name = input('Glitched names (y/n):')
            if glitch_name == 'y':
                glitch_name = True
            else:
                glitch_name = False

        if not check_code(pin):
            print('ERR: Missing arguments, use -h for help')
            exit()
        break
names = gen_names(prefix, count, style, glitch_name)

ids = []
for i in range(count):
    ids.append(i)

if gui:
    from _ui import *

    def guifunc(*_):
        # global active
        f = Form(name='kahoot-annoyer', FIX_MINIMUM_SIZE_WHEN_CREATED=False)
        f.update_values(q, e)

    def wrapper(_, e):
        npyscreen.wrapper_basic(guifunc)
        e.clear()
        with suppress(KeyboardInterrupt):
            raise KeyboardInterrupt

quiz_url = ''


def main_thread(queue):
    global quiz_url
    while e.is_set():
        get = queue.get()
        if get[0] != 'main':
            queue.put(get)
        else:
            quiz_url = get[1]
            break


threads = []
quizid = ''

thread = Thread(target=main_thread, args=(q,), name='main')
threads.append(thread)

manager = manager(queue=q, bot_names=names, event=e)
thread = Thread(target=manager.run, name='bot-manager')
threads.append(thread)

for i in range(count):
    f_bot = bot(name=names[i], pin=pin, ackId=ids[i], queue=q, event=e)
    thread = Thread(target=f_bot.run, name=names[i])
    threads.append(thread)
    time.sleep(0.01)

if gui:
    q.put(['gui', count, 'init', pin])
    thread = Thread(target=wrapper, args=(q, e,), name='gui')
    threads.append(thread)

for thread in threads:
    thread.start()
    print(f'INFO: Thread[{thread.name} - {thread.ident}] started.') if verbose else None

while e.is_set():
    try:
        time.sleep(0.0001)
        if not e.is_set():
            e.clear()
    except KeyboardInterrupt:
        e.clear()
        print('done')
        break

for thread in threads:
    thread.join()
    print(f'INFO: Thread[{thread.name} - {thread.ident}] killed.') if verbose else None

print(quiz_url)
