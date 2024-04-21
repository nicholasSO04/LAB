from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Create3(Bluetooth())  # Will connect to the first robot found.

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === MAZE DICTIONARY
N_X_CELLS = 3 # Size of maze (x dimension)
N_Y_CELLS = 3 # Size of maze (y dimension)
CELL_DIM = 50


# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (0,1)
CURR_CELL = START
DESTINATION = (1,0)
MAZE_DICT[CURR_CELL]["visited"] = True


# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80

# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    pass

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    pass

# ==========================================================
# Helper Functions

def createMazeDict(nXCells, nYCells, cellDim):
    
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

# ==========================================================
# EXPLORATION AND NAVIGATION

# === EXPLORE MAZE
async def navigateToNextCell():
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM
    pass

@event(robot.when_play)
async def navigateMaze():
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    pass


robot.play()
