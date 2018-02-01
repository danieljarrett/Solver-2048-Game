import signal

class TimeoutException(Exception):
    pass

def setTimer(interval):
    signal.setitimer(signal.ITIMER_REAL, interval)

def sigHandler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, sigHandler)
