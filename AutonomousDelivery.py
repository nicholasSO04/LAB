

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m
from math import sqrt
# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Create3(Bluetooth())  # Will connect to the first robot found.


HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
SENSOR2CHECK = 0
HAS_ARRIVED = False
DESTINATION = (0, 120)
ARRIVAL_THRESHOLD = 5
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

# Implementation for fail-safe robots
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

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    headings = [] # add headings to thing
    theta = getCorrectionAngle(headings)
    robot.turn_right(theta)
    destAngle = getAngleToDestination()
    robot.turn_right(destAngle)
    

# === MOVE TO GOAL
async def moveTowardGoal(robot):
    while HAS_FOUND_OBSTACLE == False:
        robot.set_wheel_speeds(5,5) # must define this function properly


# === FOLLOW OBSTACLE
async def followObstacle():
    pass

# ==========================================================

# Main function

@event(robot.when_play)
async def makeDelivery(robot):
    pass


# start the robot
robot.play()


