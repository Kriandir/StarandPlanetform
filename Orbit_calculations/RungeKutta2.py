import initialOrbitals as ic
import numpy as np
import math
import theforacc as forc


# Perform the Runge-Kutta calculations for both the star and the planet
# def calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt):

def RKiter(dx,dy,x,y,dt,kuttax,kuttay,kuttadx,kuttady):
    """
    Calculate the Runge-Kutta terms for the RK4-Method
    """

    if kuttax ==0 and kuttay ==0:
        kx = dx
        ky = dy
        kdx,kdy = calcaccx(x + kuttax*dt,y+kuttay*dt)

    else:
        kx = dx + kuttadx*dt
        ky = dy + kuttady*dt
        kdx,kdy = calcaccx(x + kuttax*dt,y+kuttay*dt)
    return kx,ky,kdx,kdy

########### TODO IMPLEMENT CM FOR vx etc in ACCX and MAKE EVERYTHING PROPERLY RUNNABLE####
def calcK(instances,dt):
    for j in instances:
        j.rungevalues = []
        j.rungevalues.append([0,0,0,0])

    for i in np.arange(1,5):
        for j in instances:
            if i != 4:
                kuttax,kuttay,kuttadx,kuttady = RKiter(dx,dy,x,y,dt*0.5,j.rungevalues[i-1][0],j.rungevalues[i-1][1],j.rungevalues[i-1][2],j.rungevalues[i-1][3])
                j.rungevalues.append([kuttax,kuttay,kuttadx,kuttady])

            if i == 4:
                kuttax,kuttay,kuttadx,kuttady = RKiter(dx,dy,x,y,dt,j.rungevalues[i-1][0],j.rungevalues[i-1][1],j.rungevalues[i-1][2],j.rungevalues[i-1][3])
                j.rungevalues.append([kuttax,kuttay,kuttadx,kuttady])

    for j in instances:
        j.x = j.x + ((1/6)*(j.rungevalues[1][0]+(2*j.rungevalues[2][0])+(2*j.rungevalues[3][0])+j.rungevalues[4][0]))*dt
        j.y= j.y + ((1/6)*(j.rungevalues[1][1]+(2*j.rungevalues[2][1])+(2*j.rungevalues[3][1])+j.rungevalues[4][1]))*dt
        j.vx = j.vx + ((1/6)*(j.rungevalues[1][2]+(2*j.rungevalues[2][2])+(2*j.rungevalues[3][2])+j.rungevalues[4][2]))*dt
        j.vy = j.vy + ((1/6)*(j.rungevalues[1][3]+(2*j.rungevalues[2][3])+(2*j.rungevalues[3][3])+j.rungevalues[4][3]))*dt
    #
    #
    # return kxp,kyp,kvxp,kvyp,kxs,kys,kvxs,kvys



# Calculate R,theta,F and acceleration and return the acceleration
def calcaccx(planet,xp,yp,xs,ys):

    R = forc.calcDist(xp,yp,xs,ys)
    theta = forc.calcTheta(xp,yp)

    # check whether planet or star
    if planet == True:

        Fp = forc.calcForce(R,ic.Orbitals.instances[0].mass)
        axp,ayp = forc.calcAcc(xp,yp,Fp,ic.Orbitals.instances[0].mass,theta)

        return axp,ayp

    if planet == False:

        Fs = forc.calcForce(R,ic.Orbitals.instances[1].mass)
        axs,ays = forc.calcAcc(xs,ys,Fs,ic.Orbitals.instances[1].mass,theta)

        return axs,ays

# Runge-kutta function
def calcRK(dt):

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


    # calculate and store the position and velocity of the orbitals using RK

    ic.Orbitals.instances[0].x,ic.Orbitals.instances[0].y,ic.Orbitals.instances[0].vx, \
    ic.Orbitals.instances[0].vy,ic.Orbitals.instances[1].x,ic.Orbitals.instances[1].y, \
    ic.Orbitals.instances[1].vx,ic.Orbitals.instances[1].vy \
    = calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt)
