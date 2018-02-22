import initialOrbitals as ic
import numpy as np
import math
import theforacc as forc


# Perform the Runge-Kutta calculations for both the star and the planet
# def calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt):
def calcK(instances, dt)

    x = []
    y = []
    vx = []
    vy = []

    cm_x = 0
    cm_y = 0

    for i in range(len(instances)):
        x.append(instances[i].vx)
        y.append(instances[i].vy)
        vx.append(instances[i].ax)
        vy.append(instances[i].ay)
    
    for i in range(len(x)):
        cm_x = instances[i].mass * x[i]
        cm_x += cm_x


    cm_x = cm_x / 

    x2 = []
    y2 = []
    vx2 = []
    vy2 = []

    for i in range(len(instances)):
        x2.append(x[i] + vx[i]*dt*0.5)
        y2.append(y[i] + vy[i]*dt*0.5)
        temp = calcaccx(True, instances[i].x + x[i]*dt*0.5, instances[i].y + y[i]*dt*0.5 ,xs + kx1s*dt*0.5,ys + ky1s*dt*0.5)
        vx2.append(temp[0])
        vy2.append(temp[1])

        # kx1p = vxp
        # kvx1p = axp
        # ky1p = vyp
        # kvy1p = ayp

        # kx1s = vxs
        # kvx1s = axs
        # ky1s = vys
        # kvy1s = ays


    # planet=True
    # kx2p = vxp + kvx1p*dt*0.5
    # ky2p = vyp + kvy1p*dt*0.5
    # kvx2p,kvy2p = calcaccx(planet,xp + kx1p*dt*0.5,yp + ky1p*dt*0.5,xs + kx1s*dt*0.5,ys + ky1s*dt*0.5)

    # planet=False
    # kx2s = vxs + kvx1s*dt*0.5
    # ky2s = vys + kvy1s*dt*0.5
    # kvx2s,kvy2s = calcaccx(planet,xp + kx1p*dt*0.5,yp + ky1p*dt*0.5,xs + kx1s*dt*0.5,ys + ky1s*dt*0.5)


    # planet=True
    # kx3p = vxp + kvx2p*dt*0.5
    # ky3p = vyp + kvy2p*dt*0.5
    # kvx3p,kvy3p = calcaccx(planet,xp + kx2p*dt*0.5,yp+ ky2p*dt*0.5,xs + kx2s*dt*0.5,ys + ky2s*dt*0.5)


    # planet=False
    # kx3s = vxs + kvx2s*dt*0.5
    # ky3s = vys + kvy2s*dt*0.5
    # kvx3s,kvy3s = calcaccx(planet,xp + kx2p*dt*0.5, yp + ky2p*dt*0.5, xs + kx2s*dt*0.5, ys + ky2s*dt*0.5)


    # planet=True
    # kx4p = vxp + kvx3p*dt
    # ky4p = vyp + kvy3p*dt
    # kvx4p,kvy4p = calcaccx(planet,xp + kx3p*dt,yp + ky3p*dt,xs + kx3s*dt,ys + ky3s*dt)

    # planet=False
    # kx4s = vxs + kvx3s*dt
    # ky4s = vys + kvy3s*dt
    # kvx4s,kvy4s = calcaccx(planet,xp + kx3p*dt,yp + ky3p*dt,xs + kx3s*dt,ys + ky3s*dt)


    # kxp = xp + ((float(1)/6)*(kx1p+(2*kx2p)+(2*kx3p)+kx4p))*dt
    # kyp = yp + ((float(1)/6)*(ky1p+(2*ky2p)+(2*ky3p)+ky4p))*dt
    # kvxp = vxp + ((float(1)/6) * (kvx1p+(2*kvx2p)+(2*kvx3p)+kvx4p))*dt
    # kvyp = vyp + ((float(1)/6) * (kvy1p+(2*kvy2p)+(2*kvy3p)+kvy4p))*dt


    # kxs = xs + ((float(1)/6)*(kx1s+(2*kx2s)+(2*kx3s)+kx4s))*dt
    # kys = ys + ((float(1)/6)*(ky1s+(2*ky2s)+(2*ky3s)+ky4s))*dt
    # kvxs = vxs + ((float(1)/6) * (kvx1s+(2*kvx2s)+(2*kvx3s)+kvx4s))*dt
    # kvys = vys + ((float(1)/6) * (kvy1s+(2*kvy2s)+(2*kvy3s)+kvy4s))*dt


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

    # ic.Orbitals.instances[0].x,ic.Orbitals.instances[0].y,ic.Orbitals.instances[0].vx, \
    # ic.Orbitals.instances[0].vy,ic.Orbitals.instances[1].x,ic.Orbitals.instances[1].y, \
    # ic.Orbitals.instances[1].vx,ic.Orbitals.instances[1].vy \
    # = calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt)

    calcK(ic.Orbitals.instances, dt)
