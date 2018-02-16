import initialOrbitals as ic
import numpy as np
import math
import theforacc as forc



# function for calculating the velocity, we return it twice so we can utilize
# the velocity again for the calculation on the x and y positions
def calcVelo(vx,vy,ax,ay,dt):

    vx = vx + ax*dt
    vy = vy + ay*dt
    return vx,vy,vx,vy


# Leap function
def calcLeap(dt,initialv):

    #  get positional and velocital values from objects
    xp = ic.Orbitals.instances[0].x
    yp = ic.Orbitals.instances[0].y
    vxp = ic.Orbitals.instances[0].vx
    vyp = ic.Orbitals.instances[0].vy
    xs = ic.Orbitals.instances[1].x
    ys = ic.Orbitals.instances[1].y
    vxs = ic.Orbitals.instances[1].vx
    vys = ic.Orbitals.instances[1].vy

    # function calls for both distance and theta
    R = forc.calcDist(xp,yp,xs,ys)
    theta = forc.calcTheta(xp,yp)

    # function call to calc the force on the planet and the star
    Fp = forc.calcForce(R,ic.Orbitals.instances[0].mass)
    Fs = forc.calcForce(R,ic.Orbitals.instances[1].mass)

    # function to calc the acceleration for the planet and the star
    axp,ayp = forc.calcAcc(xp,yp,Fp,ic.Orbitals.instances[0].mass,theta)
    axs,ays = forc.calcAcc(xs,ys,Fs,ic.Orbitals.instances[1].mass,theta)

    # Setting v 0.5 dt back initially
    if initialv == False:

        vxp = vxp -.5 * abs(axp) * dt
        vyp = vyp -.5 * abs(ayp) * dt
        vxs = vxs -.5 * abs(axs) * dt
        vys = vys -.5 * abs(ays) * dt


    # Here the new planet speed and position properties are calculated and stored in the planet object

    ic.Orbitals.instances[0].vx,ic.Orbitals.instances[0].vy,vxp,vyp = calcVelo(vxp,vyp,axp,ayp,dt)
    ic.Orbitals.instances[0].x = xp + vxp * dt
    ic.Orbitals.instances[0].y = yp + vyp * dt


    # Here the new star speed and position properties are calculated and stored in the star object

    ic.Orbitals.instances[1].vx,ic.Orbitals.instances[1].vy,vxs,vys = calcVelo(vxs,vys,axs,ays,dt)
    ic.Orbitals.instances[1].x = xs + vxs * dt
    ic.Orbitals.instances[1].y = ys + vys * dt

    return True
