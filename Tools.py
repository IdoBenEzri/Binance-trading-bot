import time

def get_date(timestamp):
    t = timestamp/1000
    humantime= time.ctime(t)
    return humantime


def getPercant(x,y):
    if x and y:
        return (x/y)*100
    return None    