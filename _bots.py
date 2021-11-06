import sys
import requests
import datetime
from _token import *
from _payload import *
from _functions import *

class manager:

    def __init__(self,queue,bot_names,event):
        self.bot_names = bot_names
        self.active_bots = bot_names
        self.answered_bots = 0
        self.counter = 0
        self.counter_max = int(len(bot_names)/16)
        self.quizid = ''
        self.queue = queue
        self.event = event
        self.streaks = []
        self.points = []
        self.question = 0
        self.startedq = False
        self.datarow = [0,0,0,0]
        self.gui_ready = False

#['manager','data',self.name,correct,pointsdata['questionPoints'],data_content['totalScore'],streakdata['streakLevel'],data_content['rank']]
#['manager','answer',self.name,choice,type,index,amount]
    def getbotdata(self):
        while self.event.is_set():
            get = self.queue.get()
            if get[0] == 'manager':
                if get[1] == 'answer':
                    self.counter += 1
                    self.answered_bots += 1
                    if get[5] != self.question:
                        self.question = get[5]
                        if self.question == 0:
                            self.question = 1
                        self.startedq = True
                        self.queue.put(['gui',None,'index',self.question])
                    if self.gui_ready == False:
                        self.queue.put(['gui',None,'nums',get[6],self.question])
                        for i in range(get[6]):
                            self.streaks.append([])
                            self.points.append([])
                        self.gui_ready = True
                        time.sleep(1)
                    if (get[4] == 'multiple_select_quiz') or (get[4] == 'jumble'):
                        for choice in get[3]:
                            if choice == 0:
                                self.datarow[0] += 1
                            elif choice == 1:
                                self.datarow[1] += 1
                            elif choice == 2:
                                self.datarow[2] += 1
                            elif choice == 3:
                                self.datarow[3] += 1
                    elif get[4] == 'quiz':
                        if get[3] == 0:
                            self.datarow[0] += 1
                        elif get[3] == 1:
                            self.datarow[1] += 1
                        elif get[3] == 2:
                            self.datarow[2] += 1
                        elif get[3] == 3:
                            self.datarow[3] += 1
                    if (self.counter >= self.counter_max) or (self.answered_bots >= len(self.bot_names) - self.counter_max):
                        self.queue.put(['gui',None,'answerstat',self.question,self.datarow])
                        self.counter = 0
                elif get[1] == 'data':
                    self.answered_bots -= 1
                    self.counter += 1
                    if self.startedq:
                        self.queue.put(['gui',None,'done index'])
                        self.startedq = False
                    self.datarow = [0,0,0,0]
                    # if get[3] == True:
                    #     correct = 'correctly'
                    # elif get[3] == False:
                    #     correct = 'incorrectly'
                    # self.queue.put(['gui',get[2],'correct',correct,get[4]])
                    try:
                        self.streaks[self.question].append(f'{get[6]} : {get[2]}')
                        self.points[self.question].append(f'{get[7]} : {get[5]} : {get[2]}')
                        self.streaks[self.question].sort(reverse=True,key=getfirstnum)
                        self.points[self.question].sort(key=getfirstnum)
                    except:
                        pass
                    if (self.counter >= self.counter_max) or (self.answered_bots <= self.counter_max):
                        self.queue.put(['gui',None,'streaks',self.streaks[self.question]])
                        self.queue.put(['gui',None,'points',self.points[self.question]])
                        self.counter = 0
                elif get[1] == 'leave':
                    self.active_bots.remove(get[2])
                    self.quizid = get[3]
                    self.queue.put(['gui',None,'end',self.quizid])
                    sys.exit()
            else:
                self.queue.put(get)
    def run(self):
        self.getbotdata()

class bot:

    def __init__(self, pin, name, ackId, queue, event):
        self.pin = pin
        self.name = name
        self.s = requests.Session()
        self.subId = 12
        self.ackId = ackId
        self.url = ''
        self.token = ''
        self.clientId = ''
        self.queue = queue
        self.event = event
        self.epoch = int(datetime.datetime.now().timestamp())

    def connect(self):
        try:
            token_response = self.s.get(f'https://kahoot.it/reserve/session/{self.pin}/?{self.epoch}')
            header_token = token_response.headers['x-kahoot-session-token']
            content = json.loads(token_response.content)
            challenge = str(content['challenge'])
            challenge_token = challenge_handle(challenge)
            self.token = gen_session(header_token,challenge_token)
            self.url = f'https://kahoot.it/cometd/{self.pin}/{self.token}/'
            response = self.s.post(f'{self.url}/handshake',data=handshake_payload(self.ackId))
            resp = json.loads(response.text)
            self.clientId = str(resp[0]["clientId"])
            self.s.post(self.url,data=name_payload(self.name,self.pin,self.clientId))
            return 'success'
        except:
            return 'error'

    def connected(self):
        self.subId += 1
        self.s.post(self.url,data=first_con_payload(self.ackId,self.clientId,self.subId))
        while self.event.is_set():
            self.subId += 1
            r = self.s.post(self.url,data=second_con_payload(self.ackId,self.clientId,self.subId))
            if not self.event.is_set():
                break
            response = json.loads(r.text)
            if len(response) > 0:
              for i,x in enum(response):
                if x['channel'] == "/service/player":
                    data = json.dumps(x['data'])
                    data = json.loads(data)
                    if data['id'] == 3:
                        data_content = json.loads(data['content'])
                        quizid = data_content['quizId']
                        wait()
                        self.queue.put(['gui',self.name,'leave'])
                        self.queue.put(['manager','leave',self.name,quizid])
                        sys.exit()
                    elif data['id'] == 2:
                        data_content = json.loads(data['content'])
                        question_num = data_content["questionIndex"]
                        answers = data_content["quizQuestionAnswers"]
                        foo = answers[question_num]-1
                        gameType = data_content['gameBlockType']
                        self.answer_question([foo, gameType, question_num, len(answers)])
                    elif data['id'] == 8:
                        data_content = json.loads(data['content'])
                        pointsdata = data_content['pointsData']
                        streakdata = pointsdata['answerStreakPoints']
                        try:
                            correct = data_content['isCorrect']
                        except:
                            correct = True
                        self.queue.put(['manager','data',self.name,correct,pointsdata['questionPoints'],data_content['totalScore'],streakdata['streakLevel'],data_content['rank']])
                    elif data['id'] == 4:
                        break
                else:
                    continue

    def answer_question(self,get):
        foo, gameType, index, amount = get
        if gameType == 'multiple_select_quiz':
            choice = [*range(foo+1)]
            random.shuffle(choice)
            for i in range(0,random.randint(0,foo)):
                del choice[-1]
            choice.sort()
        elif gameType == 'jumble':
            choice = [*range(4)]
            random.shuffle(choice)
        elif gameType == 'open_ended':
            choice = randomString(random.randint(0,20))
        else:
            choice = random.randint(0,foo)
            gameType = 'quiz'
        self.queue.put(['manager','answer', self.name, choice, gameType, index, amount])
        wait()
        self.s.post(self.url, data=answer_payload(self.pin, self.clientId, self.subId, choice, gameType))

    def run(self):
        while True:
            if self.connect() == 'success':
                self.queue.put(['gui',self.name,'join'])
                self.connected()
                break
            else:
                wait()
