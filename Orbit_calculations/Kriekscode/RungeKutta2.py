import initialOrbitals as ic
import numpy as np
import math
import theforacc2 as forc


# Perform the Runge-Kutta calculations for both the star and the planet
# def calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt):

def RKiter(dx,dy,x,y,dt,kuttax,kuttay,kuttadx,kuttady,j,i,instances):
    """
    Calculate the Runge-Kutta terms for the RK4-Method
    """
#  if at the first kutta term do this:
    if kuttax ==0 and kuttay ==0:
        kx = dx
        ky = dy
        kdx,kdy = calcaccx(x + kuttax*dt,y+kuttay*dt,j,i,instances,dt)
# if at any other kutta term do this:
    else:
        kx = dx + kuttadx*dt
        ky = dy + kuttady*dt
        kdx,kdy = calcaccx(x + kuttax*dt,y+kuttay*dt,j,i,instances,dt)

    return kx,ky,kdx,kdy


def calcK(instances,dt):
    """Here we call on all the RK functions"""
    # Reset the rungevalues atributes for each object
    for j in instances:
        j.rungevalues = []
        j.rungevalues.append([0,0,0,0])

# loop through the runge kutta terms
    for i in np.arange(1,5):
        # loop through the objects
        for j in instances:
            # as long as we haven't reached the final runge kutta term do this:
            if i != 4:
                kuttax,kuttay,kuttadx,kuttady = RKiter(j.vx,j.vy,j.x,j.y,dt*0.5,j.rungevalues[i-1][0],j.rungevalues[i-1][1],j.rungevalues[i-1][2],j.rungevalues[i-1][3],j,i,instances)
                j.rungevalues.append([kuttax,kuttay,kuttadx,kuttady])

            if i == 4:
                kuttax,kuttay,kuttadx,kuttady = RKiter(j.vx,j.vy,j.x,j.y,dt,j.rungevalues[i-1][0],j.rungevalues[i-1][1],j.rungevalues[i-1][2],j.rungevalues[i-1][3],j,i,instances)
                j.rungevalues.append([kuttax,kuttay,kuttadx,kuttady])

# loop through all the instances and then change coordinates and list
    for j in instances:

        # if j.name == "Planet":
        print "kx1 = %.e en kx2 = %.e en kx3 = %.e en kx4 = %.e" %(j.rungevalues[1][2],j.rungevalues[2][2],j.rungevalues[3][2],j.rungevalues[4][2])
        j.x = j.x + ((1./6)*(j.rungevalues[1][0]+(2*j.rungevalues[2][0])+(2*j.rungevalues[3][0])+j.rungevalues[4][0]))*dt
        j.y= j.y + ((1./6)*(j.rungevalues[1][1]+(2*j.rungevalues[2][1])+(2*j.rungevalues[3][1])+j.rungevalues[4][1]))*dt
        j.vx = j.vx + ((1./6)*(j.rungevalues[1][2]+(2*j.rungevalues[2][2])+(2*j.rungevalues[3][2])+j.rungevalues[4][2]))*dt
        j.vy = j.vy + ((1./6)*(j.rungevalues[1][3]+(2*j.rungevalues[2][3])+(2*j.rungevalues[3][3])+j.rungevalues[4][3]))*dt
        j.xlist.append(j.x)
        j.ylist.append(j.y)



# Calculate R,theta,F and acceleration and return the acceleration
def calcaccx(x,y,j,i,instances,dt):
# """Function call for calculating acceleration"""
    axlist = []
    aylist = []
    # loop through the instances that are not the instance which we called this object
    # and calculate the Force ,R theta and acceleration from having put the instance at the coordinate (0,0)
    for g in instances:
        if g != j:

            x = g.x + g.rungevalues[i-1][0]*dt - x
            y = g.y + g.rungevalues[i-1][1]*dt - y
            R = forc.calcDist(x,y)
            theta = forc.calcTheta(x,y)
            F = forc.calcForce(R,j.mass,g.mass)



            ax,ay = forc.calcAcc(x,y,F,j.mass,theta)
            if j.name == "Planet" and g.name == "Planet":
                print R
                print "g.x = %.f" %x
                print "and acc = %.e " %ax
                print "######"
            axlist.append(ax)
            aylist.append(ay)
            # if g.name == "Planet" and j.name == "Star":
            #
            #     print axlist
            #     print '-------------'

    axlist = np.array(axlist)
    aylist = np.array(aylist)
    if j.name == "Star":
        print axlist
        print np.sum(axlist)
        print '------'

    return np.sum(axlist),np.sum(aylist)

# Runge-kutta function
def calcRK(dt):
    """stupid function please ignore"""
    calcK(ic.Orbitals.instances,dt)
