import initialOrbitals as ic
import numpy as np
import math
import theforacc as forc


# Eulers function
def calcEuler(dt):

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

    # Here the new planet properties are calculated and stored in the planet object
    ic.Orbitals.instances[0].x = xp + vxp * dt
    ic.Orbitals.instances[0].y = yp + vyp * dt
    ic.Orbitals.instances[0].vx =vxp + axp * dt
    ic.Orbitals.instances[0].vy =vyp + ayp * dt

    # Here the new star properties are calculated stored in the star object
    ic.Orbitals.instances[1].x = xs + vxs * dt
    ic.Orbitals.instances[1].y = ys + vys * dt
    ic.Orbitals.instances[1].vx =vxs + axs * dt
    ic.Orbitals.instances[1].vy =vys + ays * dt
