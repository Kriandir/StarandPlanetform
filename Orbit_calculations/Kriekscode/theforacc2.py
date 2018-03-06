from __future__ import division
import initialOrbitals as ic
import numpy as np
import math

# Function used to calculate the force
def calcForce(R, mass,mass2):
    # Here the force is calculated
    # if mass <= 10**28:
    #     if mass <= 10**25 and mass2 <= 10**28:
    #         print 'EARTH CENTERED'
    #     elif mass >= 10**25 and mass2 <= 10**28:
    #         print 'JUPITER CENTERED'
    #     print 'reference mass = ', mass, 'kg'
    #     print 'pulling mass   = ', mass2, 'kg'

    F = ((ic.G*(mass * mass2))/(R**2))
    return F

# Function used to calculate the acceleration
def calcAcc(x,y,F,mass,theta):

    ax = (math.sin(theta)*F)/mass
    ay = (math.cos(theta)*F)/mass

    # flips the acceleration if the object is on the other side of the ellipse
    if x < 0:
        ax = -ax
    if y < 0:
        ay = -ay

    return ax,ay


# Function used to calculate theta
def calcTheta(x,y):
    # sets theta on 90 at the starting position
    if y == 0:
        theta = math.pi/2
    else:
        theta = math.atan(np.sqrt(x**2)/(np.sqrt(y**2)))

    return theta

# Function used to calculate the distance between the planet and the sun
def calcDist(x,y):

    R = np.sqrt(x**2 + y**2)
    return R

def calcKepp(R):
    vkep = np.sqrt(ic.G*(ic.Ms)/R)

    return vkep

def Dragacc(v,vgas,orbital,e):
    return e*(v-vgas)/(ic.tstop*orbital.mass)

def calcDrag(x,y,orbital,vx,vy,dt):
    """Calculate drag Earth experiences"""
    # print orbital.name

    ex = 1
    ey = 1

    rx,ry = orbital.RKCM(dt)
    xcm = rx-x
    ycm = ry-y
    R = calcDist(xcm,ycm)
    theta = calcTheta(x,y)
    vkep = calcKepp(R)
    vhw = ic.gashead * vkep
    vkep = vkep - vhw
    vkepx = math.cos(theta)*vkep
    vkepy = math.sin(theta)*vkep


    if x <0:
        ey = -ey
        if y >0:
            ex = -ex

    if x >0:
        if y>0:
            ex = -ex

    vgasx = (vkepx)*ex

    vgasy = (vkepy)*ey
    #
    # print"##########################################"
    # print "vgasx =" + str(vgasx)
    # print "vgasy =" + str(vgasy)
    # print"##########################################"
    # print "vx = " + str(vx)
    # print "vy = " + str(vy)
    # print "_______________________________________"
    e = -1
    ax = Dragacc(vx,vgasx,orbital,e)
    ay = Dragacc(vy,vgasy,orbital,e)

    return ax,ay
