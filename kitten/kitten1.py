#import appTime
import LL1
import subprocess
import datetime
import atexit
import pickle
import subprocess
import time #used by sleep function

str = 'chrome.exe, Microsoft Word.exe,'


#takes in string of running programs
def tracker(str):

    # app = pickle.load(open("log.p", "rb")) #loads in saved object
    apps = LL1.AppLog()
    apps.init()  # makes sure all apps are starting with a false running status

    prevRun = None  # by default, this is holding running programs list from the previous check


    #def selected_apps(name):
     #   i = 0
      #  while i < appsToTrack.len():  # sees if running application is on the to track list
       #     if name == (appsToTrack(i)):
        #        return True
        #return False

    def findPrevRun(name):
        i=0
        while i < len(prevRun):
            if name == prevRun[i]:
                return True
        return False

    def stopped(name):
        i = 0
        while i < curRun.len():
            if name == curRun(i):
                return False
        return True

    while 1:
        str1 = str.split(',')  # parses input string by commmas
        appsToTrack = str
        sleeptime = 30  # how often it updates (seconds)
        timeStamp = datetime.datetime.now()

        cmd = r'WMIC /OUTPUT:C:\Users\Erin\results.txt PROCESS get Caption'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            print(line)

        filename = r'C:\Users\Erin\results.txt'
        with open(filename, 'r') as f:
            content = f.readlines()
        f = open(filename)
        results = f.readlines()

        curRun = results

        ver = len(str1)
        verr = len(curRun)
        str2 = []
        i = 0
        j = 0
        k = 0
        for i in range(ver):
            for j in range(verr):
                if str1[i] == curRun[j]:
                    str2[k] = str1[i]
                    k += 1

        # curRun #things that are currently running
        timeStamp = datetime.datetime.now()
        # checks for which applications are not running anymore and changes their running
        # bool in apps as well as puts and end timestamp  for the session
        j = 0
        if prevRun != None:
            while j < len(prevRun):  # determines when  a program ended
                if stopped(prevRun(j)):
                    apps.end(prevRun(j), timeStamp, sleeptime)

        i = 0
        while i < len(str2):
            # only update running time
            apps.update(str2[i], timeStamp, sleeptime)

        prevRun = str2
        # pickle.dump(apps, open("log.p","wb")) saves app list object to remember it all
        apps.print()
        time.sleep(sleeptime)


tracker(str)
