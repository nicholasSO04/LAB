

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
    minDist = 10000000000
    angleInd = 0
    for num in range(len(readingsList)):
        if readingsList[num] < minDist:
            minDist = readingsList[num]
            angleInd = num
    return (minDist, IR_READINGS[num])
    pass

def getCorrectionAngle(heading):
    if heading != 90:
        correctingAngle = int(heading - 90)
    pass


def getAngleToDestination(currentPosition, destination):
    xDist = destination[0] - currentPosition[0]
    yDist = destination[1] - currentPosition[1]
    angle = m.arctan(yDist/xDist) # is the value returned in degrees or radians
    correctAngle = 90-angle
    return correctAngle
    pass

def checkPositionArrived(currentPosition, destination, threshold):
    xDist = destination[0] - currentPosition[0]
    yDist = destination[1] - currentPosition[1]
    distanceDest = sqrt((xDist)**2+(yDist)**2)
    if distanceDest < threshold:
        return True
    else:
        return False
    pass

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    theta = getCorrectionAngle()
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


