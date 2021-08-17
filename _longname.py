from random import randint

def longname():
    return ''.join(chr(randint(0,143859)) for i in range(10000)).encode('utf-8','ignore').decode()
