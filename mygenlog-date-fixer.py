
import os
import sys
import time
import re


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()


        cr = func(*args, **kwargs)                                                                                      [0/749]
        cr.next()
        return cr
    return start

def follow(log_file, target):
    while True:
        line = log_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)

@coroutine
def date_grabber():
    DATE_PATTERN = r'^(?P<date>\d+)\s+(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)'
    date_line_re = re.compile(DATE_PATTERN)
    
    date = None
    hours = None
    minutes = None
    seconds = None
 
    while True:
        line = (yield)
        match = date_line_re.match(line)
        if match is not None:
            date = match.group('date')
            hours = match.group('hours')
            minutes = match.group('minutes')
            seconds = match.group('seconds')
            print line,
        else:
            print '%s   %s:%s:%s %s' % (date, hours, minutes, seconds, line)
        
if __name__ == '__main__':
    file_name = sys.argv[1]
    f = open(file_name)
    follow(f, date_grabber())
