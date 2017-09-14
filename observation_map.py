#!/usr/bin/python

import os, readchar, time

class Observation:

    def __init__(self, shower, magnitude, time):
        self.shower = shower
        self.magnitude = magnitude
        self.time = time
    
    def print_all(self):
        print(self.shower + ' ' + self.magnitude + ' ' + self.time)
        
    def commit(self):
        if(self.shower == '' or self.magnitude == '' or self.time == ''):
            play_sound(error_sound)
            print('\nError')
        else:
            self.complete = self.shower + ' ' + self.magnitude + ' ' + self.time
            os.system('echo ' + self.complete + ' >> ' + file_name)
            print('\nSuccessfuly commited ' + self.complete + ' to ' + file_name)
            self.shower = ''
            self.magnitude = ''
            self.time = ''

def beep(num):
    for i in range (1, num + 1):
        if(i == num+1):
            break
        play_sound(beep_sound)
        time.sleep(0.3)
        if(i%5 == 0 and not i == 0):
            time.sleep(0.3)

def play_sound(x):
    os.system('nohup mpv Sounds/' + x + ' &')

def get_time():
    time = str(os.popen('date -u +%H:%M:%S').read())[0:-1]
    return(time)

def read_map():
    global mapa, keys, mappings

    keys, mappings = [], []

    mapa = open('map.txt', 'r')
    mapa = mapa.readlines()
    for line in mapa:
        keys.append(line.split()[0])
        mappings.append(line.split()[2])
    return

def decode(x):
    try:
        Index = keys.index(x)
        return(mappings[Index])
    except:
        print('\nNot mapped')

def is_shower(x):
    try:  
        if(len(x) == 3):
            return (True)
        else:
            return (False)
    except:
        return(False)

def is_magnitude(x):
    try:
        int(x)
        return(True)
    except:
        return(False)
      
def cancel():
    Times.pop(-1)

def pause():
    decoded = ''
    Time = get_time() 
    os.system('echo PAUZA S ' + Time + ' >> ' + file_name)
    print('\nPocetak pauze ' + Time)
    while(not decoded == 'pause'):
        Input = readchar.readchar()
        decoded = decode(Input)
    print('\nKraj pauze ' + Time)
    Time = get_time()
    os.system('echo PAUZA E ' + Time + ' >> ' + file_name)

def show_times():
    print('\nlength:    ' + str(len(Times)))
    print(Times)

Times = []
def observe():
    global Times
    obs = Observation('', '', '')
    #play_sound(start_sound)
    while (True):
        Input = readchar.readchar()
        os.system('pkill mpv')
        decoded = decode(Input)

        if(is_magnitude(decoded)):
            obs.magnitude = decoded
            obs.print_all()
        if(is_shower(decoded)):
            obs.shower = decoded
            obs.print_all()
        if(decoded == 'marker'):
            Time = get_time()
            Times.append(Time)
            obs.print_all()
            play_sound(time_sound)
            show_times()
        if(decoded == 'show_times'):
            show_times()
        if(decoded == 'commit'):
            try:
                obs.time = Times.pop(0)
                obs.commit()
                play_sound(commit_sound)
            except:
                play_sound(error_sound)
            obs.print_all()
        if(decoded == 'pause'):
            pause()
        if(decoded == 'clear_times'):
            Times = []
        if(decoded == 'quit'):
            break

start_sound = 'start.wav'
error_sound = 'error3.wav'
beep_sound = 'beep1.wav'
time_sound = 'commit4.wav'
commit_sound = 'commit1.wav'
pause_start_sound = ''
pause_during_sound = ''
pause_stop_sound = ''


file_name = '23_24.txt'

os.system('touch ' + file_name)

play_sound(start_sound)

read_map()
observe()
