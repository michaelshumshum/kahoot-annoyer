import os
os.sys.path.append('/usr/local/lib/python3.9/site-packages')
import requests
import datetime
import queue
import random
import sys
from threading import *

from _token import *
from _payload import *
from _functions import *

class mothership:

    def __init__(self, pin, name, ackId, queue, bot_names):
        self.pin = pin
        self.name = name
        self.bot_names = bot_names
        self.s = requests.Session()
        self.subId = 12
        self.ackId = ackId
        self.url = ''
        self.token = ''
        self.clientId = ''
        self.queue = queue
        self.epoch = int(datetime.datetime.now().strftime("%s"))

        self.thread = Thread(target=self.getbotdata)

        self.streaks = []
        self.points = []

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

    def maintain_connection(self):
        self.subId += 1
        r = self.s.post(self.url,data=first_con_payload(self.ackId,self.clientId,self.subId))
        response = json.loads(r.text)
        if len(response) > 0:
          for i,x in enum(response):
            if x['channel'] != "/meta/connect":
              self.put_queue(x['data'])
        while True:
            self.subId += 1
            r = self.s.post(self.url,data=second_con_payload(self.ackId,self.clientId,self.subId))
            response = json.loads(r.text)
            if len(response) > 0:
              for i,x in enum(response):
                if x['channel'] == "/service/player":
                    self.put_queue(x['data'])

    def getbotdata(self):
        while True:
            get = self.queue.get()
            if get[0] == 'mothership':
                if get[2]:
                    if get[2] == True:
                        correct = 'correctly'
                    if get[2] == False:
                        correct = 'incorrectly'
                    self.queue.put(['gui',get[1],'correct',correct,get[4]])

                streaks_repeated = [string for string in self.streaks if get[1] in string]
                points_repeated = [string for string in self.points if get[1] in string]

                for i in range(len(streaks_repeated)-1):
                    self.streaks.remove(streaks_repeated[i])
                for i in range(len(points_repeated)-1):
                    self.points.remove(points_repeated[i])

                self.streaks.append(f'{get[5]} = {get[1]}')
                self.points.append(f'{int(get[3])} = {get[1]}')

                self.streaks.sort(reverse=True,key=getints)
                self.points.sort(reverse=True,key=getints)
                self.queue.put(['gui',None,'streaks debug',self.streaks])
                self.queue.put(['gui',None,'points debug',self.points])
                self.queue.put(['gui',None,'botdata',self.streaks[0],self.points[0],self.points[-1]])
            else:
                self.queue.put(get)

    def put_queue(self,data):
        data = json.dumps(data)
        data = json.loads(data)
        data_content = json.loads(data['content'])
        if data['id'] == 4:
            self.queue.put(['gui',None,'end'])
        if data['id'] == 2:
            self.queue.put(['gui',None,'next'])
            question_num = data_content["questionIndex"]
            answers = data_content["quizQuestionAnswers"]
            foo = answers[question_num]-1
            if data_content['gameBlockType'] == 'multiple_select_quiz':
                type = 'multi'
            elif data_content['gameBlockType'] == 'jumble':
                type = 'jumble'
            elif data_content['gameBlockType'] == 'open_ended':
                type = 'open'
            else:
                type = 'quiz'
            self.queue.put(['gui',None,'index',question_num,len(answers)])
            for name in self.bot_names:
                self.queue.put([name,foo,type])

    def run(self):
        if self.connect() == 'success':
            put = ['gui',f'mothership({self.name})','join']
            self.queue.put(put)
            self.thread.start()
            self.maintain_connection()
        else:
            print('bad')
            sys.exit()

class bot:

    def __init__(self, pin, name, ackId, queue):
        self.pin = pin
        self.name = name
        self.s = requests.Session()
        self.subId = 12
        self.ackId = ackId
        self.url = ''
        self.token = ''
        self.clientId = ''
        self.queue = queue
        self.thread = Thread(target=self.maintain_connection)
        self.epoch = int(datetime.datetime.now().strftime("%s"))

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

    def maintain_connection(self):
        self.subId += 1
        self.s.post(self.url,data=first_con_payload(self.ackId,self.clientId,self.subId))
        while True:
            self.subId += 1
            r = self.s.post(self.url,data=second_con_payload(self.ackId,self.clientId,self.subId))
            response = json.loads(r.text)
            if len(response) > 0:
              for i,x in enum(response):
                if x['channel'] == "/service/player":
                    data = json.dumps(x['data'])
                    data = json.loads(data)
                    if data['id'] == 8:
                        data_content = json.loads(data['content'])
                        pointsdata = data_content['pointsData']
                        streakdata = pointsdata['answerStreakPoints']
                        try:
                            correct = data_content['isCorrect']
                        except:
                            correct = None
                        self.queue.put(['mothership',self.name,correct,data_content['totalScore'],pointsdata['questionPoints'],streakdata['streakLevel']])
                else:
                    continue


    def answer_question(self):
        while True:
            if self.queue.empty() == False:
                get = self.queue.get()
                if get[0] != self.name:
                    self.queue.put(get)
                    continue
                foo = get[1]
                type = get[2]
                if type == 'multi':
                    choice = [*range(foo+1)]
                    random.shuffle(choice)
                    for i in range(0,random.randint(0,foo)):
                        del choice[-1]
                    choice.sort()
                elif type == 'jumble':
                    choice = [*range(4)]
                    random.shuffle(choice)
                elif type == 'open':
                    choice = randomString(random.randint(0,20))
                else:
                    choice = random.randint(0,foo)
                put = ['gui',self.name,'answer',choice,self.name,type]
                self.queue.put(put)
                #wait()
                self.s.post(self.url,data=answer_payload(self.pin,self.clientId,self.subId,choice,type))

    def run(self):
        while True:
            if self.connect() == 'success':
                self.queue.put(['gui',self.name,'join'])
                self.thread.start()
                self.answer_question()
            else:
                self.queue.put(['gui',self.name,'fail'])
                wait()
