from node import node
from timer import timer
import statistics
import random
import math 

black = (0, 0, 0)

class keeper:
    def __init__(self, bounds, safetyBounds=0.1):
        self.nodes = []
        self.bounds = bounds
        self.c_dis = 0
        self.a_dis = 0
        self.ang_dis = 0
        self.safetyBounds = safetyBounds

    #Debugging #################
    def debugHerd(self):
        print("Number of Nodes: " + len(self.nodes))
        print("Clustering: " + str(c_dis > 0))

    #Generation and Updating #################
    def updateHerd(self):
        for nodeNum in range(0, len(self.nodes)):
            node = self.nodes[nodeNum]
            listing = self.sortByDistance(node)
            if(self.c_dis > 0):
                self.clusterNode(node, listing)
            if(self.a_dis > 0):
                self.avoidNode(node, listing)                      
            if(self.ang_dis > 0):
                self.matchNode(node, listing)   

        for nodeNum in range(0, len(self.nodes)):
            node = self.nodes[nodeNum]
            node.updatePosistion()
            node = self.handleEdges(node)
        return(self.nodes)

    def addRandomizedNodes(self, nodeSize, num, speed=10, color=black):
        for i in range(0, num):
            locX = random.randint(0, self.bounds[0])
            locY = random.randint(0, self.bounds[1])
            angle = random.randint(0, 359)
            self.generateNode(nodeSize, [locX, locY], speed=speed, angle=angle,color=color)

    def generateNode(self, nodeSize, pos, speed = 0, angle = 0, color=black):
        newNode = node(nodeSize, pos = pos, speed = speed, angle = angle,  color=color)
        self.nodes.append(newNode)
        return(newNode)
    
    def handleEdges(self, node):
        #Behavor: when we come to an edge we stop the node
        xBound = self.bounds[0]
        yBound = self.bounds[1]
        xPos = node.pos[0]
        yPos = node.pos[1]
        radius = node.nSize/2

        safteyX = xBound*self.safetyBounds
        safteyY = yBound*self.safetyBounds

        if(xPos < 0):
            node.atEdge = 1
            node.pos[0] = 0
            node.setRestriction(1)
        elif(xPos > xBound - radius):
            node.atEdge = 2
            node.pos[0] = xBound - radius
            node.setRestriction(2)
        elif(yPos < 0):
            node.atEdge = 3
            node.pos[1] = 0
            node.setRestriction(3)
        elif(yPos > yBound - radius):
            node.atEdge = 4
            node.pos[1] = yBound - radius 
            node.setRestriction(4)
        else:
            node.atEdge = 0
            rNum = node.restricted
            if((rNum == 1) or (rNum == 2)):
                if((xPos > safteyX) and (xPos < xBound - radius - safteyX)):
                    node.setRestriction(0)
            if((rNum == 3) or (rNum == 4)):
                 if((yPos > safteyY) and (yPos < yBound - radius - safteyY)):
                     node.setRestriction(0)  
        return(node)

    ## DISTANCE #################
    def getNumClose(self, distance, listing):
        details = []
        i = 0
        while((i < len(listing)) and (listing[i][0] <= distance)):
            details.append([listing[i][1], listing[i][2], listing[i][3]]) 
            i+=1
        return(details)
        
    def sortByDistance(self, iNode):
        listing = []
        initX = iNode.pos[0]
        initY = iNode.pos[1]

        for node in self.nodes:
            if(node is not iNode):
                finalX = node.pos[0]
                finalY = node.pos[1]
                angle = node.angle
                d_calc = math.sqrt((finalX - initX)**2 + (finalY - initY)**2)
                listing.append([d_calc, finalX, finalY, angle])
        listing = sorted(listing)
        return(listing)

    ## CLUSTERING #################
    def enableClustering(self, distance):
        if(distance < 0):
            distance = 0

        self.c_dis = distance

    def clusterNode(self, node, listing):
        nodeX = node.pos[0]
        nodeY = node.pos[1]
        avgLoc = self.findLocalMean(self.c_dis, listing)
        if(avgLoc is not None):
            node.headToPos(avgLoc)

    def findLocalMean(self, distance, listing):
        listing = self.getNumClose(distance, listing)
        if(len(listing) == 0):
            return None
        xAvg = 0
        yAvg = 0
        for l in listing:
            xAvg += l[0]
            yAvg += l[1]
        xAvg = xAvg/len(listing)
        yAvg = yAvg/len(listing)
        return([xAvg, yAvg])

    ## AVOIDANCE 
    def enableAvoidance(self, distance):
        if(distance < 0):
            distance = 0

        self.a_dis = distance

    def avoidNode(self, node, listing):
        avgLoc = self.findLocalMean(self.a_dis, listing)
        if(avgLoc is not None):
            node.headToPos(avgLoc, invert=True)

    ## Angle Matching
    def enableAngleMatching(self, distance):
        if(distance < 0):
            distance = 0
        
        self.ang_dis = distance

    def matchNode(self, node, listing):
        angles = [node.angle]
        listing = self.getNumClose(self.ang_dis,listing)
        if(len(listing) > 1):
            for i in range(0,len(listing)):
                angles.append(listing[i][2])
            node.requestAngleChange(statistics.median(angles))