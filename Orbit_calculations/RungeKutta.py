from __future__ import division
import initialOrbitals as ic
import numpy as np
import math
import theforacc as forc


# Perform the Runge-Kutta calculations for both the star and the planet
# def calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt):
def calcK(instances, dt):

    # for i in range(len(instances)):
    print 'i = %i, x = %.4f AU, v = %.4f, a = %.4f' % (0, instances[0].x / 150000000000., instances[0].vx, instances[0].ax)
    print 'i = %i, y = %.4f AU, v = %.4f, a = %.4f' % (0, instances[0].y / 150000000000., instances[0].vy, instances[0].ay)


    x = []
    y = []
    vx = []
    vy = []

    cm_x = 0
    cm_y = 0
    mass_tot = 0

    for i in range(len(instances)):
        x.append(instances[i].vx)
        y.append(instances[i].vy)
        vx.append(instances[i].ax)
        vy.append(instances[i].ay)


    for i in range(len(x)):
        cm_x = instances[i].mass * x[i]
        cm_x += cm_x
        cm_y = instances[i].mass * y[i]
        cm_y += cm_y
        mass_tot += instances[i].mass

    cm_x = cm_x / mass_tot
    cm_y = cm_y / mass_tot

    for i in range(len(x)):
        x[i] = x[i] - cm_x
        y[i] = y[i] - cm_y

## SECOND RK STEP
    x2 = []
    y2 = []
    vx2 = []
    vy2 = []

    for i in range(len(instances)):
        x2.append(x[i] + vx[i]*dt*0.5)
        y2.append(y[i] + vy[i]*dt*0.5)
        ax_list = []
        ay_list = []
        for j in range(len(instances)):
            if i != j:
                temp = calcacc(instances[i], instances[i].x + x[i]*dt*0.5, instances[i].y + y[i]*dt*0.5, instances[j], instances[j].x + x[j]*dt*0.5, instances[j].y + y[j]*dt*0.5)
                ax_list.append(temp[0])
                ay_list.append(temp[1])

        vx2.append(sum(ax_list))
        vy2.append(sum(ay_list))

## THIRD RK STEP
    x3 = []
    y3 = []
    vx3 = []
    vy3 = []

    for i in range(len(instances)):
        x3.append(x[i] + vx2[i]*dt*0.5)
        y3.append(y[i] + vy2[i]*dt*0.5)
        ax_list = []
        ay_list = []
        for j in range(len(instances)):
            if i != j:
                temp = calcacc(instances[i], instances[i].x + x2[i]*dt*0.5, instances[i].y + y2[i]*dt*0.5, instances[j], instances[j].x + x2[j]*dt*0.5, instances[j].y + y2[j]*dt*0.5)
                ax_list.append(temp[0])
                ay_list.append(temp[1])

        vx3.append(sum(ax_list))
        vy3.append(sum(ay_list))


## FOURTH RK STEP
    x4 = []
    y4 = []
    vx4 = []
    vy4 = []

    for i in range(len(instances)):
        x4.append(x[i] + vx3[i]*dt)
        y4.append(y[i] + vy3[i]*dt)
        ax_list = []
        ay_list = []
        for j in range(len(instances)):
            if i != j:
                temp = calcacc(instances[i], instances[i].x + x3[i]*dt, instances[i].y + y3[i]*dt, instances[j], instances[j].x + x3[j]*dt, instances[j].y + y3[j]*dt)
                ax_list.append(temp[0])
                ay_list.append(temp[1])

        vx4.append(sum(ax_list))
        vy4.append(sum(ay_list))

    # planet=True
    # kx3p = vxp + kvx2p*dt*0.5
    # ky3p = vyp + kvy2p*dt*0.5
    # kvx3p,kvy3p = calcaccx(planet,xp + kx2p*dt*0.5,yp+ ky2p*dt*0.5,xs + kx2s*dt*0.5,ys + ky2s*dt*0.5)

    # planet=True
    # kx4p = vxp + kvx3p*dt
    # ky4p = vyp + kvy3p*dt
    # kvx4p,kvy4p = calcaccx(planet,xp + kx3p*dt,yp + ky3p*dt,xs + kx3s*dt,ys + ky3s*dt)

    x_final = []
    y_final = []
    vx_final = []
    vy_final = []

    for i in range(len(x)):
        x_final.append(instances[i].x + ((float(1)/6)*(x[i]+(2*x2[i])+(2*x3[i])+x4[i]))*dt)
        y_final.append(instances[i].y + ((float(1)/6)*(y[i]+(2*y2[i])+(2*y3[i])+y4[i]))*dt)
        vx_final.append(instances[i].vx + ((float(1)/6) * (vx[i]+(2*vx2[i])+(2*vx3[i])+vx4[i]))*dt)
        vy_final.append(instances[i].vy + ((float(1)/6) * (vy[i]+(2*vy2[i])+(2*vy3[i])+vy4[i]))*dt)

    for i in range(len(x)):
        instances[i].x = x_final[i]
        instances[i].y = y_final[i]
        instances[i].vx = vx_final[i]
        instances[i].vy = vy_final[i]

    return x_final, y_final, vx_final, vy_final
    # return kxp,kyp,kvxp,kvyp,kxs,kys,kvxs,kvys



# Calculate R,theta,F and acceleration and return the acceleration
def calcacc(body_1, body_1_x, body_1_y, body_2, body_2_x, body_2_y):

    force_list = []

    R = forc.calcDist(body_1_x, body_1_y, body_2_x, body_2_y)
    force = forc.calcForce(R, body_1, body_2)

    theta, x_dir, y_dir = forc.calcTheta(body_1_x, body_1_y, body_2_x, body_2_y)
    axp,ayp = forc.calcAcc(body_1_x, body_1_y, force, body_1.mass, theta, x_dir, y_dir)

    return axp, ayp


# Runge-kutta function
def calcRK(dt):

    instances = ic.Orbitals.instances
    # x = []
    # y = []
    # vx = []
    # vy = []

    #  get positional and velocital values from objects
    # xp = ic.Orbitals.instances[0].x
    # yp = ic.Orbitals.instances[0].y
    # vxp = ic.Orbitals.instances[0].vx
    # vyp = ic.Orbitals.instances[0].vy
    # xs = ic.Orbitals.instances[1].x
    # ys = ic.Orbitals.instances[1].y
    # vxs = ic.Orbitals.instances[1].vx
    # vys = ic.Orbitals.instances[1].vy

    # for i in range(len(instances)):
    #     x.append(instances[i].x)
    #     y.append(instances[i].y)
    #     vx.append(instances[i].vx)
    #     vy.append(instances[i].vy)

    # # function calls for both distance and theta
    # R = forc.calcDist(xp,yp,xs,ys)
    # theta = forc.calcTheta(xp,yp)

    # # function call to calc the force on the planet and the star
    # Fp = forc.calcForce(R,ic.Orbitals.instances[0].mass)
    # Fs = forc.calcForce(R,ic.Orbitals.instances[1].mass)

    # # function to calc the acceleration for the planet and the star
    # axp,ayp = forc.calcAcc(xp,yp,Fp,ic.Orbitals.instances[0].mass,theta)
    # axs,ays = forc.calcAcc(xs,ys,Fs,ic.Orbitals.instances[1].mass,theta)

    for i in range(len(instances)):
        for j in range(len(instances)):
            ax_list = []
            ay_list = []
            if i != j:
                temp = calcacc(instances[i], instances[i].x, instances[i].y, instances[j], instances[j].x, instances[j].y)
                ax_list.append(temp[0])
                ay_list.append(temp[1])

        instances[i].ax = sum(ax_list)
        instances[i].ay = sum(ay_list)



    # calculate and store the position and velocity of the orbitals using RK

    # ic.Orbitals.instances[0].x,ic.Orbitals.instances[0].y,ic.Orbitals.instances[0].vx, \
    # ic.Orbitals.instances[0].vy,ic.Orbitals.instances[1].x,ic.Orbitals.instances[1].y, \
    # ic.Orbitals.instances[1].vx,ic.Orbitals.instances[1].vy \
    # = calcK(xp,yp,vxp,vyp,axp,ayp,xs,ys,vxs,vys,axs,ays,dt)

    calcK(ic.Orbitals.instances, dt)
