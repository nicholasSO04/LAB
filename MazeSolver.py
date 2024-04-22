from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
name = 'MARVIN'
robot = Create3(Bluetooth(name))  # Will connect to the first robot found.

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === MAZE DICTIONARY
N_X_CELLS = 3 # Size of maze (x dimension)
N_Y_CELLS = 3 # Size of maze (y dimension)
CELL_DIM = 50


# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (0,2)
CURR_CELL = START
DESTINATION = (2,0)



# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 90

# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True

# ==========================================================
# Helper Functions

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
        potentialNeighbors = [(x + 1, y),(x, y - 1),(x-1, y),(x, y + 1)]
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

def getWallConfiguration(lsen, fsen, rsen, threshold):
    left = False
    front = False
    right = False
    ldis = 4095 / (lsen + 1)
    fdis = 4095 / (fsen + 1)
    rdis = 4095 / (rsen + 1)
    if ldis <= threshold:
        left = True
    if fdis <= threshold:
        front = True
    if rdis <= threshold:
        right = True
    return [left, front, right]

def getNavigableNeighbors(walls, neighbors, prev, xmax, ymax):
    navneighbor = []
    # for index, pos in enumerate(neighbors):
    #     if pos == prev:
    #         navneighbor.append(pos)
    #     try:
    #         if not walls[index]: 
    #             if isValidCell(pos, xmax, ymax): 
    #                 navneighbor.append(pos)
            
    #     except:
    #         pass
    if prev:
        navneighbor.append(prev)
    for index, wall in enumerate(walls):
        if not wall:
            if isValidCell(neighbors[index], xmax, ymax): 
                    navneighbor.append(neighbors[index])

    return navneighbor

def updateMazeNeighbors(mazedict, currcell, navneighbors):
    for key in mazedict:
        if currcell in mazedict[key]['neighbors']:
            if key not in navneighbors:
                mazedict[key]['neighbors'].remove(currcell)
    mazedict[currcell]['neighbors'] = navneighbors
    return mazedict
    
def getNextCell(mazedict, currcell):
    mincost = 1000000
    nextmove = None
    for pos in mazedict[currcell]['neighbors']:
        if mazedict[pos]['cost'] < mincost and not mazedict[pos]['visited']:
            mincost = mazedict[pos]['cost']
            nextmove = pos
    if nextmove == None:
        for pos in mazedict[currcell]['neighbors']:
            if mazedict[pos]['cost'] < mincost:
                mincost = mazedict[pos]['cost']
                nextmove = pos
    return nextmove

def checkCellArrived(currcell, destination):
    if currcell == destination:
        return True
    else:
        return False
    

def printMazeGrid(mazeDict, nXCells, nYCells, attribute):
    for y in range(nYCells - 1, -1, -1):
        row = '| '
        for x in range(nXCells):
            cell_value = mazeDict[(x, y)][attribute]
            row += '{} | '.format(cell_value)
        print(row[:-1])

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

# === BUILD MAZE DICTIONARY

MAZE_DICT = createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = addAllNeighbors(MAZE_DICT, N_X_CELLS, N_Y_CELLS)


MAZE_DICT[CURR_CELL]["visited"] = True
# ==========================================================
# EXPLORATION AND NAVIGATION

# === EXPLORE MAZE
async def navigateToNextCell(robot, nextcell, orientation):
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM
    # get the orientation of the cells given the current heading of the object
    # check which direction there are walls in
    # check for the cell with the lowest cost and which was not visited, find the change of angle necessary (90degrees right, 90degrees left, 180degrees)
    # set robot movement to equal to one cell dimension

    # getRobotOrientation()
    # getPotentialNeighbors()
    # isValidCell() # check if the neighbor is within the bounds of the region
    # getWallConfiguration() # check in which direction there are walls in
    # getNavigableNeighbors() # based on the location of walls, the whether the cell is within the bounds
    # updateMazeCost() # function for updating the cost of going to each cell
    # updateMazeNeighbors() # this function updates the neighbors the robot can navigate to in the dictionary
    # getNextMove() # implement this function to get the next best possible cell
    # fucntion to get angle:
    angle = 0
    direc = 0
    orient = 0
    x1, y1 = CURR_CELL
    x2, y2 = nextcell
    if x2 - x1 != 0:
        if x2-x1 >0:
            direc = 0 #right
        else:
            direc = -180 #left
    if y2-y1 != 0:
        if y2-y1 >0:
            direc = -90 #up
        else:
            direc = -270 #down
    if orientation == "N":
        orient = 90
    elif orientation == "E":
        orient = 0
    elif orientation == "S":
        orient = 270
    else:
        orient = 180
        
    angle = orient + direc
    PREV_CELL = CURR_CELL
    
    CURR_CELL = nextcell
    MAZE_DICT[CURR_CELL]['visted'] = True
    
    await robot.turn_right(angle)

    await robot.move(CELL_DIM)


@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    while not (HAS_ARRIVED or HAS_COLLIDED):
        #GET READINGS
        current_position = await robot.get_position()
        heading = current_position.heading
        orient = getRobotOrientation(heading)
        potneighbors = getPotentialNeighbors(CURR_CELL, orient)
        readings = (await robot.get_ir_proximity()).sensors
        lsen, fsen, rsen = readings[0], readings[3], readings[6]
        walls = getWallConfiguration(lsen, fsen, rsen, WALL_THRESHOLD)
        print(walls)
        navigable = getNavigableNeighbors(walls, potneighbors, PREV_CELL, N_X_CELLS, N_Y_CELLS)
        
        #UPDATE MAZE DICT
        
        MAZE_DICT = updateMazeNeighbors(MAZE_DICT, CURR_CELL, navigable)
        MAZE_DICT = updateMazeCost(MAZE_DICT, START, DESTINATION)
        
        #MOVE TO NEXT CELL
        
        next = getNextCell(MAZE_DICT, CURR_CELL)
        print(next)
        if next == (1,2):
            print(MAZE_DICT)
        await navigateToNextCell(robot, next, orient)

        if checkCellArrived(CURR_CELL, DESTINATION):
            HAS_ARRIVED = True
            print('arrived')
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(0, 255 ,0)
        if HAS_COLLIDED:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,0)



robot.play()
