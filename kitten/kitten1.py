#import appTime
import LL1
import subprocess
import datetime
import atexit
import pickle
import subprocess
import time #used by sleep function


# for blah
#	code in loop
# cide after loop
str = 'chrome.exe, Microsoft Word.exe,'
def tracker():
    [x.strip() for x in str.split(',')]
    appsToTrack = str
    sleeptime = 1
    timeStamp = datetime.datetime.now()

    # cmd = r'WMIC /OUTPUT:C:\Users\Erin\results.txt PROCESS get Caption'
    procStr = ''
    cmd = r'WMIC PROCESS get Caption'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        print(line)
        procStr += line

    curRun = procStr
    print(*curRun)

    # app = pickle.load(open("log.p", "rb")) #loads in saved object
    apps = LL1.AppLog()
    apps.init()  # makes sure all apps are starting with a false running status

    prevRun = None  # by default, this is holding running programs list from the previous check

    def selectedApps(name):
        i = 0
        while i < appsToTrack.len():  # sees if runing application is on the to track list
            if name == (appsToTrack(i)):
                return True
        return False

    def stopped(name):

        i = 0
        while i < curRun.len():
            if name == curRun(i):
                return False
        return True

    while (1):
        # curRun #things that are currently running
        timeStamp = datetime.datetime.now()
        # checks for which applications are not runnign anymore and changes their running
        # bool in apps as well as puts and end timestamp  for the session
        j = 0
        while (j < prevRun.len()):  # determines when  a program ended
            if stopped(prevRun(j)):
                apps.end(prevRun(j), timeStamp, sleeptime)

        i = 0
        while (i < curRun.len()):
            # application was already running
            if apps.find(curRun(i)) & selectedApps(curRun(i)):
                # only update running time
                apps.update(curRun(i), timeStamp, sleeptime)

            else:
                # running app not in app list so add a new node
                if selectedApps(curRun(i)): #only adds new program to list if its selected
                    apps.add(curRun(i), timeStamp)

        prevRun = curRun
        # pickle.dump(apps, open("log.p","wb")) saves app list object to remember it all
        time.sleep(sleeptime)



tracker(str)
