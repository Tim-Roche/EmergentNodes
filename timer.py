class timer:
    def __init__(self, alarm):
        self.ticks = 0
        
        self.alarm = alarm

    def tick(self):
        self.ticks += 1

    def setAlarm(self, alarm, isRinging):
        self.alarm = alarm
        if(isRinging):
            self.ticks = self.alarm
        else:
            self.ticks = 0

    def clear(self):
        self.ticks = 0

    def tickOrClear(self):
        if(self.isRinging()):
            self.clear()
        else:
            self.tick()

    def isRinging(self):
        if(self.ticks >= self.alarm):
            return(True)
        return(False)