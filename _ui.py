import os
import npyscreen
import datetime
import random
import shutil
from time import sleep

rows, columns = shutil.get_terminal_size()
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
        self.question = 'X'
        self.totalquestions = 'X'
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

        self.s_values = [['PIN',self.pin],['Connected Bots',f'{self.num}/{self.count}'],['Mothership Name',self.mothership],['Longest Streak',self.longest],['Top Ranking',self.highest],['Lowest Ranking',self.lowest]]
        self.q_values = [['Question','Red','Blue','Yellow','Green']]

        self.dateTime_widget = self.add(dateTime,editable=False,max_height=3)
        self.status_widget = self.add(status,editable=False,max_width=self.sw,max_height=8,contained_widget_arguments={'column_width' : int((self.sw-5)/2)})
        self.questions_widget = self.add(questions,editable=False,max_width=self.qw,relx=self.sw+2,rely=-(self.rows-5),contained_widget_arguments={'column_width' : int((self.qw-5)/6)})
        self.logs_widget = self.add(logs,editable=False,max_width=self.sw,rely=13,values=['START'])

    def update_values(self,queue):
        while True:
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
                    if get[2] == 'end':
                        self.logs_widget.values.append('All bots have left the game.')
                        self.logs_widget.values.append('Ending script.')
                        for i in range(7):
                            self.logs_widget.values[-1] = self.logs_widget.values[-1]+'.'
                            sleep(1)
                        queue.put(['main',get[3]])
                        break
                    if get[2] == 'nums':
                        self.totalquestions = get[3]
                        self.question = get[4]
                        self.logs_widget.values.append(f'Receieved total number of questions.')
                        for i in range(self.totalquestions):
                            self.q_values.append([i+1,0,0,0,0])
                    elif get[2] == 'streaks':
                        #self.logs_widget.values.append(f'Streaks : {get[3]}')
                        data = get[3]
                        self.longest = data[0]
                    elif get[2] == 'points':
                        #self.logs_widget.values.append(f'Points : {get[3]}')
                        data = get[3]
                        self.highest = '#'+data[0]
                        self.lowest = '#'+data[-1]
                    elif get[2] == 'init':
                        self.count = get[1]
                        self.pin = get[3]
                        self.mothership = get[4]
                    elif get[2] == 'leave':
                        self.num -= 1
                        self.logs_widget.values.append(f'<{self.num}/{self.count}> {get[1]} left.')
                    elif get[2] == 'join':
                        self.num += 1
                        self.logs_widget.values.append(f'<{self.num}/{self.count}> {get[1]} joined.')
                    elif get[2] == 'fail':
                        self.logs_widget.values.append(f'<{self.num}/{self.count}> {get[1]} failed. Retrying...')
                    # elif get[2] == 'correct':
                    #     self.logs_widget.values.append(f'{get[1]} answered {get[3]} and got {get[4]} points.')
                    elif get[2] == 'answerstat':
                        index = get[3]+1
                        data = get[4]
                        try:
                            row = self.q_values[index]
                            for i in range(4):
                                row[i+1] = data[i]
                        except:
                            pass
                    elif get[2] == 'index':
                        self.question = get[3]+1
                        self.logs_widget.values.append(f'Started question #{self.question}.')
                    #Apply values to widgets
                    self.s_values = [['PIN',self.pin],['Connected Bots',f'{self.num}/{self.count}'],['Current Question',f'{self.question}/{self.totalquestions}'],['Longest Streak',self.longest],['Top Ranking',self.highest],['Lowest Ranking',self.lowest]]
                    self.status_widget.values = self.s_values
                    self.questions_widget.values = self.q_values
                    if len(self.logs_widget.values) > self.lh:
                        start = len(self.logs_widget.values)-self.lh
                        self.logs_widget.values = self.logs_widget.values[start:]
                else:
                    queue.put(get)
            self.display()
