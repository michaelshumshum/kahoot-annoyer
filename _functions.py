import string
import random
import time

def enum(sequence,start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def gen_names(prefix,count):
    names = []
    for i in range(0,count):
        names.append(prefix+'_'+randomString(5))
    return names

def wait():
    wait = random.randint(1,25) / 10
    time.sleep(wait)

def getfirstnum(string):
    end = string.find(' : ')
    new = int(string[:end])
    return new
