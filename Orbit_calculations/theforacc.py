import initialOrbitals as ic
import numpy as np
import math

# function used to calculate the force
def calcForce(R, body_1, body_2):
    # Here the force is calculated
    F = ((ic.G*(ic.body_1.mass*body_2.mass))/(R**2))
    return F

# function used to calculate the acceleration
def calcAcc(x, y, F, mass, theta):

    ax = (math.cos(theta)*F)/mass
    ay = (math.sin(theta)*F)/mass

    # flips the acceleration if the object is on the other side of the ellipse
    # if x > 0:
    #     ax = -ax
    # if y > 0:
    #     ay = -ay

    return ax,ay
    

#function used to calculate theta
def calcTheta(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    
    # sets theta on 0 at the starting position
    if y == 0:
        theta = 0
    else:
        theta = math.atan(np.sqrt(x**2)/(np.sqrt(y**2)))

    return theta

# Function used to calculate the distance between the planet and the sun
def calcDist(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    R = np.sqrt(x**2 + y**2)

    return R
