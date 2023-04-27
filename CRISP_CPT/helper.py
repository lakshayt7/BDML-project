import datetime
import time

def parse_time(time_string):
    t = 0
    year = time_string.split('-')[0]
    month = time_string.split('-')[1]
    day = time_string.split('-')[2]
    day, stamp = day.split('T')[0], day.split('T')[1]
    hour, minute, left = stamp.split(':')
    seconds = left[:-1]
    dt = datetime.datetime(int(year), int(month), int(day))
    t+=time.mktime(dt.timetuple())
    t+=float(hour)*3600 + float(minute)*60 + float(seconds)
    return t