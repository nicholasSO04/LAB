from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

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
def getMinProxApproachAngle():
    pass

def getCorrectionAngle():
    pass


def getAngleToDestination():
    pass

def checkPositionArrived():
    pass

# === REALIGNMENT BEHAVIOR
async def realignRobot():
    pass

# === MOVE TO GOAL
async def moveTowardGoal():
    pass

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
