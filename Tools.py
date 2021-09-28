import time

def get_date(timestamp):
    t = timestamp/1000
    humantime= time.ctime(t)
    return humantime


 