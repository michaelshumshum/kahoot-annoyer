import os
os.sys.path.append('/usr/local/lib/python3.9/site-packages')
import npyscreen
import datetime
import random
from time import sleep

rows, columns = os.popen('stty size').read().split()
rows = int(rows)
columns = int(columns)

class status(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SimpleGrid
    entry_widget = npyscreen.SimpleGrid

class questions(npyscreen.BoxTitle):
	_contained_widget = npyscreen.SimpleGrid
	entry_widget = npyscreen.SimpleGrid

class dateTime(npyscreen.BoxTitle):
    _contained_widget = npyscreen.FixedText
    entry_widget = npyscreen.FixedText

class logs(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager
    entry_widget = npyscreen.Pager

class Form(npyscreen.Form):
    def create(self):
        self.pin = ''
        self.init = True
        self.num = 0
        self.question = 0
        self.totalquestions = ''
        self.count = ''
        self.mothership = ''

        rows, columns = os.popen('stty size').read().split()
        self.rows = int(rows)
        self.columns = int(columns)

        self.lh = self.rows-17
        self.sw = int(self.columns/3)
        self.qw = self.columns-self.sw-5

        self.longest = None
        self.highest = None
        self.lowest = None
        self.q_1 = 0
        self.q_2 = 0
        self.q_3 = 0
        self.q_4 = 0
        self.early_answers = []
        self.ended = True

        self.s_values = [['PIN',self.pin],['Connected Bots',f'{self.num}/{self.count}'],['Mothership Name',self.mothership],['Longest Streak',self.longest],['Top Ranking',self.highest],['Lowest Ranking',self.lowest]]
        self.q_values = [['Question','Red','Blue','Yellow','Green']]

        self.dateTime_widget = self.add(dateTime,editable=False,max_height=3)
        self.status_widget = self.add(status,editable=False,max_width=self.sw,max_height=8,contained_widget_arguments={'column_width' : int((self.sw-5)/2)})
        self.questions_widget = self.add(questions,editable=False,max_width=self.qw,relx=self.sw+2,rely=-(self.rows-5),contained_widget_arguments={'column_width' : int((self.qw-5)/6)})
        self.logs_widget = self.add(logs,editable=False,max_width=self.sw,rely=13,values=['START'])

    def update_values(self,queue):
        #Update time
        date_obj = datetime.datetime.now()

        if len(str(date_obj.hour)) < 2:
            hour = '0'+str(date_obj.hour)
        else:
            hour = date_obj.hour
        if len(str(date_obj.minute)) < 2:
            minute = '0'+str(date_obj.minute)
        else:
            minute = date_obj.minute
        if len(str(date_obj.second)) < 2:
            second = '0'+str(date_obj.second)
        else:
            second = date_obj.second

        self.date = f'{date_obj.year}/{date_obj.month}/{date_obj.day}'
        self.time = f'{hour}:{minute}:{second}'
        self.dateTime_widget.value = self.date+' '+self.time

        if queue.empty() == False:
            get = queue.get()
            if get[0] == 'gui':
                #Get values from queue
                if get[2] == 'streaks debug':
                    self.logs_widget.values.append(f'Streaks : {get[3]}')
                if get[2] == 'points debug':
                    self.logs_widget.values.append(f'Points : {get[3]}')
                if get[2] == 'init':
                    self.count = get[1]
                    self.pin = get[3]
                    self.mothership = get[4]
                if get[2] == 'join':
                    self.num += 1
                    self.logs_widget.values.append(f'{get[1]} joined.')
                if get[2] == 'fail':
                    self.logs_widget.values.append(f'{get[1]} failed. Retrying...')
                if get[2] == 'correct':
                    self.logs_widget.values.append(f'{get[1]} answered {get[3]} and got {get[4]} points.')
                if get[2] == 'botdata':
                    self.longest = get[3]
                    self.highest = get[4]
                    self.lowest = get[5]
                if get[2] == 'end':
                    self.logs_widget.values.append(f'Question {self.question} ended.')
                    self.q_1 = 0
                    self.q_2 = 0
                    self.q_3 = 0
                    self.q_4 = 0
                    self.ended = True
                if get[2] == 'next':
                    self.ended = False
                    self.logs_widget.values.append(f'Question {self.question} started.')
                    for answer in self.early_answers:
                        self.logs_widget.values.append(f'[{self.question}] : Receieved answer {answer[1]} from {answer[0]}.')
                        if (answer[2] == 'multi') or (answer[2] == 'jumble'):
                            choices = answer[1]
                            for choice in choices:
                                if choice == 0:
                                    self.q_1 += 1
                                elif choice == 1:
                                    self.q_2 += 1
                                elif choice == 2:
                                    self.q_3 += 1
                                elif choice == 3:
                                    self.q_4 += 1
                        elif (answer[2] == 'quiz'):
                            choice = answer[1]
                            if choice == 0:
                                self.q_1 += 1
                            elif choice == 1:
                                self.q_2 += 1
                            elif choice == 2:
                                self.q_3 += 1
                            elif choice == 3:
                                self.q_4 += 1
                    self.early_answers = []
                if get[2] == 'index':
                    self.question = get[3]
                    if self.init == True:
                        self.totalquestions = get[4]
                        self.logs_widget.values.append(f'Got total questions ({self.totalquestions})')
                        self.init = False
                        for i in range(0,self.totalquestions):
                            self.questions_widget.values.append([i,0,0,0,0])
                if get[2] == 'answer':
                    if self.ended == True:
                        self.early_answers.append([get[1],get[3],get[5]])
                    else:
                        self.logs_widget.values.append(f'[{self.question}] : Receieved answer {get[3]} from {get[1]}.')
                        if (get[5] == 'multi') or (get[5] == 'jumble'):
                            choices = get[3]
                            for choice in choices:
                                if choice == 0:
                                    self.q_1 += 1
                                elif choice == 1:
                                    self.q_2 += 1
                                elif choice == 2:
                                    self.q_3 += 1
                                elif choice == 3:
                                    self.q_4 += 1
                        elif (get[5] == 'quiz'):
                            choice = get[1]
                            if choice == 0:
                                self.q_1 += 1
                            elif choice == 1:
                                self.q_2 += 1
                            elif choice == 2:
                                self.q_3 += 1
                            elif choice == 3:
                                self.q_4 += 1
                #Apply values to widgets
                self.s_values = [['PIN',self.pin],['Connected Bots',f'{self.num}/{self.count}'],['Mothership Name',self.mothership],['Longest Streak',self.longest],['Top Ranking',self.highest],['Lowest Ranking',self.lowest]]
                self.status_widget.values = self.s_values
                if self.ended != True:
                    try:
                        self.q_values[self.question+1] = [self.question,self.q_1,self.q_2,self.q_3,self.q_4]
                    except:
                        pass
                self.questions_widget.values = self.q_values
                if len(self.logs_widget.values) > self.lh:
                    start = len(self.logs_widget.values)-self.lh
                    self.logs_widget.values = self.logs_widget.values[start:]
            else:
                queue.put(get)
