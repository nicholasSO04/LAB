def turnangle(CURR_CELL, nextcell, orientation):
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
    return angle


print(turnangle((0,0),(1,0), "N"))

print(turnangle((0,0),(0,1), "N"))

print(turnangle((0,0),(-1,0), "E"))

print(turnangle((0,0),(0,-1), "W"))

print(turnangle((0,0),(0,1), "S"))