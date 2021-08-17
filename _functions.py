import string
import random
import time
from _longname import *

def enum(sequence,start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def gen_names(prefix,count,style,glitchname):
    names = []
    characters = list(string.ascii_uppercase+string.ascii_lowercase)
    digits = list(string.digits)
    for i in range(0,count):
        if glitchname == True:
            prefix = longname()
        names.append(prefix+'_'+randomString(5))
    if style == True:
        for name in names:
            new_name = ''
            c_no = [156,312,260]
            c_offset = random.choice(c_no)
            while c_offset in c_no:
                c_offset = random.randint(1,12) * 52

            d_offset = random.randint(1,4) * 10
            for c in [char for char in name]:
                if c in characters:
                    new = characters.index(c) + 119808 + c_offset
                    new = chr(new)
                elif c in digits:
                    new = digits.index(c) + 120782 + d_offset
                    new = chr(new)
                else:
                    new = c
                new_name = new_name + new
            index = names.index(name)
            names[index] = new_name
    return names

def wait():
    wait = random.randint(1,100) / 10
    time.sleep(wait)

def getfirstnum(string):
    end = string.find(' : ')
    new = int(string[:end])
    return new
