from __future__ import division
import initialOrbitals as ic
import numpy as np
import math

# function used to calculate the force
def calcForce(R, mass,mass2):
    # Here the force is calculated
    print mass
    print mass2
    F = ((ic.G*(mass * mass2))/(R**2))
    return F

# function used to calculate the acceleration
def calcAcc(x,y,F,mass,theta):

    ax = (math.sin(theta)*F)/mass
    # print '########################'
    # print theta
    # print ax
    # print '#############################'
    ay = (math.cos(theta)*F)/mass

    # print '########################'
    # print "y = woop woop: %.f" %y
    # print "ay = derp derp: %.f" %ay
    # print '#############################'

    # flips the acceleration if the object is on the other side of the ellipse
    if x < 0:
        ax = -ax
    if y < 0:
        ay = -ay

    return ax,ay


#function used to calculate theta
def calcTheta(x,y):
    # sets theta on 90 at the starting position
    if y == 0:
        theta = math.pi/2
    else:
        # print "##############"
        # print "x = %.f" %x
        # print "y = %.f" % y
        # print '###############'
        theta = math.atan(np.sqrt(x**2)/(np.sqrt(y**2)))
        # print theta/math.pi
        # print '$$$$$$$$$$$$$$$$$'

    return theta

# Function used to calculate the distance between the planet and the sun
def calcDist(x,y):

    R = np.sqrt(x**2 + y**2)
    return R
