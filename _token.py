import base64
import array

def challenge_handle(challenge):
    s1 = challenge.find('this,')+7
    s2 = challenge.find("');")
    message = challenge[s1:s2]
    s1 = challenge.find('var offset')+13
    s2 = challenge.find('; if')
    offset = str("".join(challenge[s1:s2].split()))
    offset = eval(offset)
    def repl(char, position):
        return chr((((ord(char)*position) + offset)% 77)+ 48)
    res = ""
    for i in range(0,len(message)):
        res+=repl(message[i],i)
    return res

def gen_session(header_session,challenge_token):
    kahoot_session_bytes = base64.b64decode(header_session)
    challenge_bytes = str(challenge_token).encode("ASCII")
    bytes_list = []
    for i in range(len(kahoot_session_bytes)):
        bytes_list.append(kahoot_session_bytes[i] ^ challenge_bytes[i%len(challenge_bytes)])
    return array.array('B',bytes_list).tobytes().decode("ASCII")
