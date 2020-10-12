#! /usr/bin/env python3.8
import ctypes
import datetime
import random
import threading
import time

schedule = {
    'Sunday': {
        'next_alarm_day': 'Monday',
        'next_day_offset': 1,   # Monday
        'start': None,          # No reminder today
        'stop': None            # No reminder today
    },
    'Monday': {
        'next_alarm_day': 'Tuesday',
        'next_day_offset': 1,   # Tuesday
        'start': 9*3600,        # 9:00AM
        'stop': 16*3600         # 3:00PM
    },
    'Tuesday': {
        'next_alarm_day': 'Wednesday',
        'next_day_offset': 1,   # Wednesday
        'start': 9*3600,        # 9:00AM
        'stop': 16*3600         # 10:30AM
    },
    'Wednesday': {
        'next_alarm_day': 'Thursday',
        'next_day_offset': 1,   # Thursday
        'start': 9*3600,        # 9:00AM
        'stop': 16*3600         # 3:00PM
    },
    'Thursday': {
        'next_alarm_day': 'Friday',
        'next_day_offset': 1,   # Friday
        'start': 9*3600,        # 9:00AM
        'stop': 16*3600         # 3:00PM
    },
    'Friday': {
        'next_alarm_day': 'Monday',
        'next_day_offset': 3,   # Monday
        'start': 9*3600,        # 9:00AM
        'stop': 16*3600         # 3:00PM
    },
    'Saturday': {
        'next_alarm_day': 'Monday',
        'next_day_offset': 2,   # Monday
        'start': None,          # No reminder today
        'stop': None            # No reminder today
    }
}


def message_box(title, body, style):
    ## Button styles:
    # 0 : OK
    # 1 : OK | Cancel
    # 2 : Abort | Retry | Ignore
    # 3 : Yes | No | Cancel
    # 4 : Yes | No
    # 5 : Retry | No 
    # 6 : Cancel | Try Again | Continue

    ## To also change icon, add these values to previous number
    # 16 Stop-sign icon
    # 32 Question-mark icon
    # 48 Exclamation-point icon
    # 64 Information-sign icon consisting of an 'i' in a circle
    return ctypes.windll.user32.MessageBoxW(0, body, title, style)


def daily_reminder():
    # Display message box
    #     'OK' == 1
    # 'Cancel' == 2
    reminder_response = message_box('Reminder!', 'This is your reminder!', 1)
    
    if reminder_response == 2:
        # The user selected 'Cancel'... confirm script termination
        # 'Yes' == 6
        #  'No' == 7
        confirmation_response = message_box('Please Confirm', 'Are you sure you want stop getting reminders?', 36)
        
        if confirmation_response == 6:
            # The user selected 'Yes'... end the script
            return
    
    # Compute the next reminder time
    now = datetime.datetime.today()
    weekday = datetime.datetime(now.year, now.month, now.day).strftime("%A")
    
    midnight_next_alarm = datetime.datetime(now.year, now.month, now.day).timestamp() + 86400 * schedule[weekday]['next_day_offset']
    next_alarm_day = schedule[weekday]['next_alarm_day']
    
    schedule_start = midnight_next_alarm + schedule[next_alarm_day]['start']
    schedule_stop = midnight_next_alarm + schedule[next_alarm_day]['stop']

    next_alarm_time = random.randint(schedule_start, schedule_stop)
    # print(next_alarm_time)
    # print('Next alarm scheduled for:', datetime.datetime.fromtimestamp(next_alarm_time).strftime('%A, %B %d, %Y %I:%M:%S'))
    reminder_log(datetime.datetime.fromtimestamp(next_alarm_time).strftime('%A, %B %d, %Y %I:%M:%S'))
    
    t = threading.Timer(next_alarm_time - datetime.datetime.today().timestamp(), daily_reminder)
    t.start()

    return


def reminder_log(s):
    with open('reminder_log.txt', 'a') as f:
        f.write(s)
        f.write('\n')

daily_reminder()