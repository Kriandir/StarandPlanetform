import initialOrbitals as ic
import numpy as np
import math

# function used to calculate the force
def calcForce(R, mass):
    # Here the force is calculated
    F = ((ic.G*(ic.Orbitals.instances[0].mass*ic.Orbitals.instances[1].mass))/(R**2))
    return F

# function used to calculate the acceleration
def calcAcc(x,y,F,mass,theta):

    ax = (math.sin(theta)*F)/mass
    ay = (math.cos(theta)*F)/mass

    # flips the acceleration if the object is on the other side of the ellipse
    if x > 0:
        ax = -ax
    if y > 0:
        ay = -ay

    return ax,ay
    

#function used to calculate theta
def calcTheta(x,y):
    # sets theta on 90 at the starting position
    if y == 0:
        theta = math.pi/2
    else:
        theta = math.atan(np.sqrt(x**2)/(np.sqrt(y**2)))

    return theta

# Function used to calculate the distance between the planet and the sun
def calcDist(x,y,xx,yy):

    R = np.sqrt(x**2 + y**2) + np.sqrt(xx**2 + yy**2)
    return R
