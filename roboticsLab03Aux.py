import math as m
from math import sqrt
from collections import deque
from unittest import TestCase
TestCase.maxDiff = None
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

#print(getCorrectionAngle(135))

def getAngleToDestination(currentPosition, destination):
    currx, curry = currentPosition
    destx, desty = destination
    xDist = destx - currx
    yDist = desty - curry
    try:
        angle = m.atan(xDist/yDist) # is the value returned in degrees or radians
    except:
        if xDist > 0:
            angle = (-m.pi/2)
        else:
            angle = (-(m.pi/2))
    correctAngle = m.degrees(angle)
    if xDist >= 0 and yDist <= 0:
        
        correctAngle += 180
    elif xDist < 0 and yDist < 0:
        
        correctAngle -= 180
    return int(correctAngle)

#print(getAngleToDestination((0,0), (-1,0)))


def checkPositionArrived(currentPosition, destination, threshold):
    x1, y1 = currentPosition
    x2, y2 = destination
    distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
    if distance <= threshold:
        return True
    else:
        return False
    
def createMazeDict(i, j, size):
    dict1 = {}
    for x in range(i):
        for y in range(j):
            dict1[(x,y)] = {'position' : (x * size, y * size), 'neighbors': [], 'visited': False, 'cost': 0}
    return dict1


def addAllNeighbors(mazedict, a, b):
    for key in mazedict:
        x, y = key
        if (x-1, y) in mazedict:
            mazedict[key]['neighbors'] += [(x-1, y)]
        if (x, y+1) in mazedict:
            mazedict[key]['neighbors'] += [(x, y+1)]
        if (x+1, y) in mazedict:
            mazedict[key]['neighbors'] += [(x+1, y)]
        if (x, y-1) in mazedict:
            mazedict[key]['neighbors'] += [(x, y-1)]
        
    return mazedict

def getRobotOrientation(heading):
    heading = heading % 360
    if heading >= 225 and heading < 315:
        return 'S'
    if heading >= 315 and heading < 360 or heading < 45:
        return 'E'
    if heading >= 45 and heading < 135:
        return 'N'
    if heading >= 135 and heading < 225:
        return 'W'

def getPotentialNeighbors(currcell, orientation):
    x,y = currcell
    if orientation == "N":
        potentialNeighbors = [(x-1, y),(x, y + 1 ),(x+1, y),(x, y -1)]
    if orientation == "S":
        potentialNeighbors = [(x + 1, y),(x, y -1),(x-1, y),(x, y + 1)]
    if orientation == "E":
        potentialNeighbors = [(x, y + 1),(x+1, y),(x, y -1),(x-1, y)]
    if orientation == "W":
        potentialNeighbors = [(x, y -1),(x-1, y),(x, y + 1),(x + 1, y)]
    return potentialNeighbors
    

def isValidCell(indices, xmax, ymax):
    x, y = indices
    if x < xmax and x >= 0 and y >= 0 and y < ymax:
        return True
    else:
        return False
print(isValidCell((0,2), 3, 3))
def getWallConfiguration(lsen, fsen, rsen, threshold):
    left = False
    front = False
    right = False
    ldis = 4095 / (lsen + 1)
    fdis = 4095 / (fsen + 1)
    rdis = 4095 / (rsen + 1)
    if ldis < threshold:
        left = True
    if fdis < threshold:
        front = True
    if rdis < threshold:
        right = True
    return [left, front, right]

def getNavigableNeighbors(walls, neighbors, prev, xmax, ymax):
    navneighbor = []
    for index, pos in enumerate(neighbors):
        if index < 3:
            if not walls[index]:
                if isValidCell(pos, xmax, ymax):
                    navneighbor.append(pos)
        else:
            if pos == prev:
                navneighbor.insert(0,pos)
    return navneighbor




def updateMazeNeighbors(mazedict, currcell, navneighbors): #not entirely sure if this actually works
    mazedict[currcell]['neighbors'] = navneighbors
    for key in mazedict:
        if currcell in mazedict[key]['neighbors']:
            if currcell not in navneighbors:
                mazedict[key]['neighbors'].remove(currcell)
    return mazedict
#print(updateMazeNeighbors({(0, 0): {'position': (0, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 1): {'position': (0, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 2): {'position': (0, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 3): {'position': (0, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 4): {'position': (0, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 0): {'position': (1, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 1): {'position': (1, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 2): {'position': (1, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 3): {'position': (1, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 4): {'position': (1, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 0): {'position': (2, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 1): {'position': (2, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 2): {'position': (2, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 3): {'position': (2, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 4): {'position': (2, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 0): {'position': (3, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 1): {'position': (3, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 2): {'position': (3, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 3): {'position': (3, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 4): {'position': (3, 4), 'neighbors': [], 'visited': False, 'cost': 0}}, (2, 2), [(1, 2), (3, 2), (2, 1)]))
#print(updateMazeNeighbors({(0, 0): {'position': (0, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 1): {'position': (0, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 2): {'position': (0, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 3): {'position': (0, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 4): {'position': (0, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 0): {'position': (1, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 1): {'position': (1, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 2): {'position': (1, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 3): {'position': (1, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 4): {'position': (1, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 0): {'position': (2, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 1): {'position': (2, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 2): {'position': (2, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 3): {'position': (2, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 4): {'position': (2, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 0): {'position': (3, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 1): {'position': (3, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 2): {'position': (3, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 3): {'position': (3, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 4): {'position': (3, 4), 'neighbors': [], 'visited': False, 'cost': 0}}, (2, 2), [(1, 2), (2, 1)]))
  
def getNextCell(mazedict, currcell):
    mincost = 1000000
    nextmove = None
    for pos in mazedict[currcell]['neighbors']:
        if mazedict[pos]['cost'] < mincost and not mazedict[pos]['visited']:
            mincost = mazedict[pos]['cost']
            nextmove = pos
    if nextmove == None:
        for pos in mazedict[currcell]['neighbors']:
            if mazedict[pos]['cost'] < mincost and not mazedict[pos]['visited']:
                mincost = mazedict[pos]['cost']
                nextmove = pos
    return nextmove

#print(getNextCell({(0, 0): {'position': (0, 0), 'neighbors': [(1, 0)], 'visited': False, 'cost': 1, 'flooded': True}, (0, 1): {'position': (0, 50), 'neighbors': [], 'visited': True, 'cost': 0, 'flooded': False}, (0, 2): {'position': (0, 100), 'neighbors': [(1, 2)], 'visited': False, 'cost': 3, 'flooded': True}, (1, 0): {'position': (50, 0), 'neighbors': [(0, 0), (1, 1), (2, 0)], 'visited': False, 'cost': 0, 'flooded': True}, (1, 1): {'position': (50, 50), 'neighbors': [(1, 2), (2, 1), (1, 0)], 'visited': False, 'cost': 1, 'flooded': True}, (1, 2): {'position': (50, 100), 'neighbors': [(0, 2), (2, 2), (1, 1)], 'visited': False, 'cost': 2, 'flooded': True}, (2, 0): {'position': (100, 0), 'neighbors': [(1, 0), (2, 1)], 'visited': False, 'cost': 1, 'flooded': True}, (2, 1): {'position': (100, 50), 'neighbors': [(1, 1), (2, 2), (2, 0)], 'visited': False, 'cost': 2, 'flooded': True}, (2, 2): {'position': (100, 100), 'neighbors': [(1, 2), (2, 1)], 'visited': False, 'cost': 3, 'flooded': True}}, (0, 1)))

def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False

    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True

    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']

        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)
    return mazeDict
#print(updateMazeCost({(0, 0): {'position': (0, 0), 'neighbors': [(0, 1)], 'visited': True, 'cost': 0}, (0, 1): {'position': (0, 1), 'neighbors': [(0, 0), (1, 1)], 'visited': False, 'cost': 0}, (1, 0): {'position': (1, 0), 'neighbors': [(1, 1)], 'visited': False, 'cost': 0}, (1, 1): {'position': (1, 1), 'neighbors': [(1, 0), (0, 1)], 'visited': True, 'cost': 0}}, (0, 0), (1, 0)))

def checkCellArrived(currcell, destination):
    if currcell == destination:
        return True
    else:
        return False
    