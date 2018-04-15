
class Node(object):
 
    def __init__(self, app_name, timeLog, curStart, curEnd, totalTime, prev, next, running):
        self.app_name = app_name # .exe name as seen by computer
        self.timeLog = timeLog
        self.curStart = curStart
        self.curEnd = curEnd
        self.totalTime = totalTime
        self.prev = prev
        self.next = next
        self.running = running
        #self.formalName = formalName
 
 
class AppLog(object):
 
    head = None
    tail = None
 
    def add(self, app_name, timeLog):
        #need to get the appname
        new_node = Node(app_name, timeLog[3][1000], -1, 0, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node
        new_node.running = False

    def remove(self, app_name):
        current_node = self.head
 
        while current_node is not None:
            if current_node.appName == app_name:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    self.current_node.next.prev = None
 
            current_node = current_node.next
 
    def show(self):
        print("Show list appName:")
        current_node = self.head
        while current_node is not None:
            print(current_node.prev.app_name) if hasattr(current_node.prev, "app_name") else None,
            print(current_node.app_name),
            print(current_node.totalTime),
            print(current_node.next.app_name) if hasattr(current_node.next, "app_name") else None
 
            current_node = current_node.next
        print("*"*50)

    def get_node(self, app_name):
        current_node = self.head
        while current_node is not None:
            if app_name == current_node.app_name:
                return current_node
            else:
                current_node = current_node.next

    def get_time(self, app_name):
        current_node = self.get_node(app_name)
        return current_node.totalTime

    def update(self, app_name,time, unitSleep, curStart):
        current_node = self.get_node(app_name)
        if self.find(app_name) is not True:
            self.add(app_name, None)
        if current_node.running is not True:
            current_node.timeLog[0][curStart+1] = time
            current_node.totalTime = current_node.totalTime+unitSleep
        else:
            current_node.running = True
            current_node.timeLog[2][curStart+1] += unitSleep
            current_node.totalTime = current_node.totalTime + unitSleep

    def end(self, app_name, time,unitSleep, curStart):
        current_node = self.get_node(app_name)
        #adds unitsleep time to duration
        current_node.timeLog[0][curStart+1] += unitSleep
        current_node.totalTime += unitSleep
        #adds time stamp for when application was stopped
        current_node.timeLog[2][curStart+1] = time
        current_node.curStart+=1 #correct way to increment?
        current_node.running = False


    #initilizes running status of applications to false for extra precautions (save data in case of crash)
    def init(self):
        current_node = self.head
        while current_node is not None:
            current_node.running = False
            current_node = current_node.next

    def find(self, name):
        current_node = self.head
        while current_node is not None:
            if current_node.app_name == name:
                return True
        return False

    def print(self):
        current_node = self.head
        while current_node is not None:
            #if current_node.appName == name:
            print(current_node.totalTime)
            print(current_node.app_name)


# d = AppLog()
 
# d.add(5)
# d.add(6)
# d.add(50)
# d.add(30)
 
# d.show()
 
# d.remove(50)
# d.remove(5)
 
# d.show()