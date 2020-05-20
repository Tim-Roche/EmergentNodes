import math 
import random 
import statistics

black = (0, 0, 0)

class node:
    
    def __init__(self, nSize, pos = [0,0], speed=0, angle=0, color=black):
        self.pos = pos
        self.speed = speed
        self.nSize = nSize
        self.angle = angle
        self.maxAng = 10
        self.atEdge = 0
        self.edgeProtectionComplete = False
        self.color = color
        self.og_color = color
        self.demandedAngles = []
        self.restricted = 0
    
    def updateAngle(self, angle):
        self.angle = angle%360
        return(self.angle)
    
    def addToAngle(self,angle):
        self.angle+= angle
        self.angle = self.angle%360
        return(self.angle)

    def flipAngle(self, inv_angle):
        return(360 - inv_angle)

    def headToPos(self, newPos, invert=False):
        deltaX = newPos[0] - self.pos[0]
        deltaY = newPos[1] - self.pos[1]
        if((deltaX == 0) and (deltaY == 0)):
            return 

        raw_angle = math.degrees(math.atan2(deltaY, deltaX))
        if(invert==True):
            raw_angle = 180 + raw_angle
        angle = self.flipAngle(raw_angle)
        self.requestAngleChange(angle)

    def updatePosistion(self):
        self.addAntiEdge()
        if(self.restricted==0):
            self.requestAngleChange(self.angle, onlyEmpty=True)
            self.updateAngle(self.pickNewAngle())
        else:
            self.clearAngleRequests()
        flipedAng = self.flipAngle(self.angle)
        self.pos[0] = self.pos[0] + self.speed*math.cos(math.radians(flipedAng))
        self.pos[1] = self.pos[1] + self.speed*math.sin(math.radians(flipedAng))
    
    def setRestriction(self, restrictedNum):
        self.restricted = restrictedNum
        if(self.restricted != 0):
            self.color = black
        else:
            self.color = self.og_color
        #print("Restriction: "+str(self.restricted))

    def addAntiEdge(self):
        if((self.atEdge > 0)):
            velX = self.speed*math.cos(math.radians(self.angle))
            velY = self.speed*math.sin(math.radians(self.angle))
            if(self.atEdge >= 3):
                velY = -1*velY
            if((self.atEdge > 0) and (self.atEdge <= 2)):
                velX = -1*velX
            self.updateAngle(math.floor(math.degrees((math.atan2(velY, velX)))))
            return(True)
        return(False)

    def requestAngleChange(self, angle, onlyEmpty=False):
        if((onlyEmpty == False) or (not self.demandedAngles)):
            self.demandedAngles.append(angle)

    def clearAngleRequests(self):
        self.demandedAngles = []

    def capAngleChange(self, newAngle):
        if(self.maxAng >= 360):
            return(newAngle)
        delta = newAngle - self.angle
        addAngle = min([abs(delta), self.maxAng])
        s = math.copysign(1, delta)
        newAngle = self.angle + s*addAngle
        return(newAngle)

    def pickNewAngle(self):
        if(len(self.demandedAngles) > 0):
            avg = statistics.median(self.demandedAngles)
            self.demandedAngles = []
            return(self.capAngleChange(avg))
        return(self.angle)

    def nodeState(self):
        print("Posistion: " + str(self.pos))
        print("Speed: " + str(self.speed))
        print("Angle: "+ str(self.angle))
        print("At Edge: " + str(self.atEdge))
        print("Used Edge Protect: " + str(self.edgeProtectionComplete))
