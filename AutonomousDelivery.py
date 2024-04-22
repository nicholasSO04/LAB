

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m
from math import sqrt
# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
name = "EVE"
robot = Create3(Bluetooth(name))  # Will connect to the first robot found.


HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
SENSOR2CHECK = 0
HAS_ARRIVED = False
DESTINATION = (0, 20)
ARRIVAL_THRESHOLD = 5
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
ROTATION_DIR = 0
SPEED = 10

# Implementation for fail-safe robots
# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255,0,0)
    

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255,0,0)

# ==========================================================

# Helper Functions
def getMinProxApproachAngle(readingsList):
    global IR_ANGLES
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
    
def movementDirection(readings):
    max = 0
    sensorIndex = -1
    direc = "clockwise"
    for i in range(len(readings)):
        if readings[i] >= 20:
            if readings[i] > max:
                max = readings[i]
                sensorIndex = i
    if sensorIndex in [0, 1, 2]: 
        direc = "clockwise"                            
            
    elif sensorIndex in [4,5,6]:  
        direc = "counterclockwise" 
    return direc   

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    
    global HAS_REALIGNED, DESTINATION
    await robot.set_wheel_speeds(0,0)
    current_position = await robot.get_position()
    headings = current_position.heading
    pos = current_position.x, current_position.y
    theta = getCorrectionAngle(headings)
    await robot.turn_right(theta)
    destAngle = getAngleToDestination(pos, DESTINATION)
    print(theta, destAngle)
    await robot.turn_right(destAngle)
    HAS_REALIGNED = True
    await robot.set_wheel_speeds(SPEED, SPEED)

    

# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global HAS_FOUND_OBSTACLE, SENSOR2CHECK, SPEED, HAS_REALIGNED, HAS_ARRIVED
    await robot.set_wheel_speeds(SPEED, SPEED)
    readings = (await robot.get_ir_proximity()).sensors
    dist, angle =  getMinProxApproachAngle(readings)
    current_position = await robot.get_position()
    pos = current_position.x, current_position.y
    if checkPositionArrived(pos, DESTINATION, ARRIVAL_THRESHOLD):
            HAS_ARRIVED = True
            print('arrived')
    print(current_position.x, current_position.y)
    if dist < 20:
        await robot.set_wheel_speeds(0,0)
        await robot.turn_right(angle)
        HAS_FOUND_OBSTACLE = True
        HAS_REALIGNED = False
        ROTATION_DIR = movementDirection(readings)
        if ROTATION_DIR == "clockwise":
            SENSOR2CHECK = 0
        else:
            SENSOR2CHECK = 6


# === FOLLOW OBSTACLE
async def followObstacle(robot):
    global ROTATION_DIR, SPEED, HAS_FOUND_OBSTACLE, HAS_REALIGNED
    await robot.set_wheel_speeds(SPEED,SPEED)
    readings = (await robot.get_ir_proximity()).sensors
    sidesens = readings[SENSOR2CHECK]
    sidedist = 4095 / (sidesens + 1)
    if sidedist > 100:
        HAS_FOUND_OBSTACLE = False
        HAS_REALIGNED = False
        await robot.move(5) # figure out this distance
    elif sidedist <= 5 or sidedist > 10:
        await robot.set_wheel_speeds(0,0)
        if ROTATION_DIR == "clockwise":
            if sidedist <= 5:
                await robot.turn_right(3)
            if sidedist > 10:
                await robot.turn_left(3)
        else:
            if sidedist <= 5:
                await robot.turn_left(3)
            if sidedist > 10:
                await robot.turn_right(3)
        await robot.set_wheel_speeds(SPEED, SPEED)

# ==========================================================

# Main function

@event(robot.when_play)
async def makeDelivery(robot):
    global ROTATION_DIR, SPEED, HAS_FOUND_OBSTACLE, SENSOR2CHECK
    global HAS_ARRIVED, HAS_COLLIDED, HAS_REALIGNED
    global DESTINATION

    while not HAS_ARRIVED and not HAS_COLLIDED:
        print('hi')
        while not HAS_REALIGNED and not HAS_COLLIDED:
            await realignRobot(robot)
            while not HAS_FOUND_OBSTACLE and not HAS_COLLIDED and not HAS_ARRIVED:
                await moveTowardGoal(robot)
            while HAS_FOUND_OBSTACLE and not HAS_COLLIDED and not HAS_ARRIVED:
                await followObstacle(robot)

        current_position = await robot.get_position()
        pos = current_position.x, current_position.y
        if checkPositionArrived(pos, DESTINATION, ARRIVAL_THRESHOLD):
            HAS_ARRIVED = True
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(0,255,0)
            print('arrived')


# start the robot
robot.play()


