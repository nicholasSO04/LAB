import math as m
from math import sqrt

def getMinProxApproachAngle(readingsList):
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
    max = 0 
    closest = 0
    for index, i in enumerate(readingsList):
        if i > max:
            max = i
            closest = IR_ANGLES[index]
    max = 4095 / (max + 1)
    max = round(max, 3)
    return max, closest

def getCorrectionAngle(heading):
    correction = 90
    if heading < 0:
        correction = 90 - heading
        if heading < -90:
            correction -= 360
    elif correction > 0:
        correction = 90 - heading
    return int(-1 * correction)

print(getCorrectionAngle(135.6))

print(getCorrectionAngle(-116))

print(getCorrectionAngle(-89))


def getAngleToDestination(currentPosition, destination):
    currx, curry = currentPosition
    destx, desty = destination
    xDist = destx - currx
    yDist = desty - curry
    angle = m.atan(xDist/yDist) # is the value returned in degrees or radians
    correctAngle = m.degrees(angle)
    if xDist > 0 and yDist < 0:
        correctAngle += 180
    elif xDist < 0 and yDist < 0:
        correctAngle -= 180
    return int(correctAngle)




def checkPositionArrived(currentPosition, destination, threshold):
    x1, y1 = currentPosition
    x2, y2 = destination
    distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
    if distance <= threshold:
        return True
    else:
        return False
    
def createMazeDict():
    pass

def addAllNeighbors():
    pass

def getRobotOrientation():
    pass

def getPotentialNeighbors():
    pass

def isValidCell():
    pass

def getWallConfiguration():
    pass

def getNavigableNeighbors():
    pass

def updateMazeNeighbors():
    pass
    
def getNextCell():
    pass

def checkCellArrived():
    pass