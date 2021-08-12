from threading import *
from _bots import *
from sys import argv
q = queue.Queue()

def Check_code(pin):
    epoch = int(datetime.datetime.now().timestamp())
    r = requests.get(f'https://kahoot.it/reserve/session/{pin}/?{epoch}')
    if r.status_code != 200:
        print('Incorrect PIN')
        return False
    return True

#### Command-arguments section ####

pin = None
count = None
interactive = False
prefix = "bot"
style = False
glitchname = False
gui = False

args = argv[1:]
for i in range(len(args)):
    arg = args[i-1].lower()
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
            print('The majority of this open-source code was written by michaelshumshum, and therefore much of this is their copyright.\n')
            print("Edited by andmagdo to be headless and allow for better commandline support (maybe eventually will make into a website)")
            print('\n\n')
            print("I'm too lazy to check if you have done a command multiple times, so subsequent arguments will overwrite previous")
            print('\n')
            print('Required arguments are marked with a *. They are required unless interactive mode is on\n')
            print('-h will bring up this menu\n')
            print('--gui will turn on the curses gui. Please note, a workaround is required to run this on Windows\n')
            print('-i will bring up an interactive prompt for all below arguments\n')
            print('-n will set the name of the bots defaults to "bot" ex: python flood.py -n bot\n')
            print('-b * will set the number of bots, must be an integer (please note, many bots may lag your computer) ex: python flood.py -b 100\n')
            print('-c or -p * will set the kahoot code, must be an integer ex: python flood.py -c 9999999\n')
            print('-s will turn on 𝓈𝓉𝓎𝓁𝑒 (style) for names\n')
            print('-g will turn on g̵̲͈̠̺̺̃l̴̢͈͙͚̃̽̍̕͘͝i̷̜͛͛̐́̾̃̽t̷͚̠̾͐c̶̢̝̦̩̹̾̄̈̅͆́͜ͅĥ̷̛̺̘̈́̓̏́͒̅y̶̝̙̗͓͍̝͔̰̌͝  (glitchy) names\n')
            print("You cannot have both styled and glitchy names.")
            exit()
        if "i" in arg:
            print('INFO: Interactive mode on')
            interactive = True
        if "s" in arg:
            style = True
            glitchname = False
            print("INFO: Adding style to names")
        if "g" in arg:
            style = False
            glitchname = True
            print("INFO: Adding glitchiness to names")
    if "-b" in arg:
        try:
            count = int(args[i])
            print(f"INFO: Using {count} bots.")
        except ValueError:
            print('WARN: Number of bots must be an integer. Ignoring')
    if "-n" in arg:
        prefix = args[i]
        print(f"INFO: The bots will be named a derivative of {prefix}.")
    if "-c" in arg or "-p" in arg:
        try:
            code = int(args[i])
            if not Check_code(code):
                print('WARN: Code not valid. Ignoring')
            else:
                pin = code
                print(f"INFO: Using {pin} as the code.")
        except ValueError:
            print('WARN: Code must be an integer. Ignoring')
    if "--gui" in arg:
        print("INFO: Using gui")
        gui = True


if (pin and count) or interactive:
    pass
else:
    print('ERR: Missing arguments, use -h for help')
    exit()

if interactive:
    while True:
        try:
            prefix = argv[3]
        except:
            prefix = 'bot'
        try:
            pin = argv[1]
            count = int(argv[2])
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

        if not Check_code(pin):
            continue
        break
names = gen_names(prefix,count,style,glitchname)

ids = []
for i in range(count):
    ids.append(i)


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
thread.setDaemon(True)
threads.append(thread)
thread.start()

manager = manager(queue=q,bot_names=names)
thread = Thread(target=manager.run,name='bot-manager')
thread.setDaemon(True)
threads.append(thread)
thread.start()

for i in range(count):
    f_bot = bot(name=names[i],pin=pin,ackId=ids[i],queue=q)
    thread = Thread(target=f_bot.run,name=names[i])
    thread.setDaemon(True)
    threads.append(thread)
    thread.start()
    time.sleep(0.01)

q.put(['gui',count,'init',pin])
threads.append(thread)

for thread in threads:
    thread.join()
