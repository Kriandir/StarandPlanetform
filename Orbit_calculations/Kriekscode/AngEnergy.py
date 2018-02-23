import initialOrbitals as ic
import numpy as np
import theforacc2 as forc
import math

# calculate the angular momentum using the different Orbitals and then return it
def angmom():
    angmom = 0
    for i in range(len(ic.Orbitals.instances)):
        xdir = ic.Orbitals.instances[i].mass * ic.Orbitals.instances[i].vy * ic.Orbitals.instances[i].x
        ydir = ic.Orbitals.instances[i].mass * ic.Orbitals.instances[i].vx * ic.Orbitals.instances[i].y
        angmom = angmom +(xdir-ydir)
        return angmom

def eng():

# small formula for calculating the m1*m2
    Mass = 1
    for i in range (len(ic.Orbitals.instances)):

        Mass *= ic.Orbitals.instances[i].mass

# calculating the potential and kinetic energy of the system
    # Epot = (ic.G*Mass)/forc.calcDist(ic.Orbitals.instances[0].x,ic.Orbitals.instances[0].y, \
    # ic.Orbitals.instances[1].x,ic.Orbitals.instances[1].y)
    Epot = 1
    Ekinp = 0.5*(np.sqrt(ic.Orbitals.instances[0].vx**2 + ic.Orbitals.instances[0].vy**2)**2)* \
    ic.Orbitals.instances[0].mass
    Ekins = 0.5*(np.sqrt(ic.Orbitals.instances[1].vx**2 + ic.Orbitals.instances[1].vy**2)**2)* \
    ic.Orbitals.instances[1].mass

    Etot = Ekinp + Ekins - Epot

    return Etot
