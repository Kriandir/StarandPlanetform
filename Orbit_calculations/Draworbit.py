import Eulerorbit as k
import Leapfrogorbit as lf
import initialOrbitals as ic
import RungeKutta as u
import AngEnergy as ae
import AskDraw as ad
import DrawAll as da
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import sys





# ask which method to use and if we want to time
try:
    ad.asktimesteps()
except(KeyboardInterrupt):
    sys.exit(0)
timespent = []
# variable used if timing
p = 0
# variable used if using hours days weeks months
h = 0


def Draw(p):

    if ic.calcEuler:
        name = "Euler"
        method = "EU"
    if ic.calcLeap:
        method = "LF"
        name = "Leapfrog"
    if ic.calcRK:
        method = "RK"
        name = "Runge-Kutta"

    # define the figure
    fig = plt.figure("2 body system", figsize=(20,10))
    ax1 = fig.add_subplot(311)
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax2 = fig.add_subplot(312)
    ax2.set_ylabel("Energydifference in %")
    ax3 = fig.add_subplot(313,sharex = ax2,sharey= ax2)
    ax3.set_ylabel("Angularmomentum in  %")
    # ax2.axis([-1,ic.stepamount+1,0.8,1.2])
    # plt.gca().set_position((.1, .3, .8, .6))

    if ic.hourmonth == True:
        ax2.set_xlabel("Steps of %s" % ic.timehdwm)
        ax3.set_xlabel("Steps of %s" % ic.timehdwm)
        plt.suptitle("2 body system using the %s method for a = %0.3e, eccentricity = %0.4f and timestep of %s for a period of 5 years" \
         % (name, ic.a, ic.e,ic.timehdwm),fontsize=20)

    if ic.hourmonth == False:
        ax2.set_xlabel("Steps of %i (s)" % ic.dt)
        ax3.set_xlabel("Steps of %i (s)" % ic.dt)
        years = (ic.dt * ic.stepamount)/31536000.
        plt.suptitle("2 body system using the %s method for a = %0.3e, eccentricity = %0.4f and timestep of %i seconds for a period of %0.2f years" % (name, ic.a, ic.e,ic.dt,years),fontsize=20)



    # check if timer is true.. start clock if true and loop 100 times
    if ic.timer == False:
        p = 99
    while p < 100:
        if ic.timer == True:
            start = time.clock()

        # defining initial values
        ic.Orbitals.instances = []
        Earth = ic.Planet("Earth",ic.a,ic.e,ic.q,ic.Mp)
        Sun = ic.Star("Sun",ic.Ms)
        xplist = []
        yplist = []
        xslist = []
        yslist = []
        englist = []
        angmomlist = []
        i = 0

        # make sure that the initialv if using leapfrog is moved back by 0.5 dt
        initialv = False

        # if live drawing plot a dynamic figure
        if ic.directdraw == True:
            ax1.set_autoscale_on(True)
            plt.ion()


        # Looping over the time steps
        while i < ic.stepamount:

            # determine which calculation we will perform
            if ic.calcEuler:
                k.calcEuler(ic.dt)
            if ic.calcLeap:
                initialv = lf.calcLeap(ic.dt,initialv)
            if ic.calcRK:
                u.calcRK(ic.dt)


            # if not live drawing append to list
            if ic.directdraw == False:

                yplist.append(ic.Orbitals.instances[0].y)
                xplist.append(ic.Orbitals.instances[0].x)
                yslist.append(ic.Orbitals.instances[1].y)
                xslist.append(ic.Orbitals.instances[1].x)

            # calculate energy and angular momentum

            englist.append(ae.eng())
            angmomlist.append(ae.angmom())

            # take initial energy and angular momentum
            if i == 0:
                starteng = ae.eng()
                startangmom = ae.angmom()

            # if live drawing directly draw the planet and the star
            if ic.directdraw == True:
                if ic.dt < 10000 and ic.dt > 0:
                    if i % 100 == 0:
                        for j in range(len(ic.Orbitals.instances)):
                            ax1.scatter(ic.Orbitals.instances[j].x,ic.Orbitals.instances[j].y)

                        ax2.scatter(i,(ae.eng()/starteng))
                        ax3.scatter(i,(ae.angmom()/startangmom))
                        plt.pause(0.0005)
                else:
                    if i % 10 == 0:
                        for j in range(len(ic.Orbitals.instances)):
                            ax1.scatter(ic.Orbitals.instances[j].x,ic.Orbitals.instances[j].y)

                        ax2.scatter(i,(ae.eng()/starteng))
                        ax3.scatter(i,(ae.angmom()/startangmom))
                        plt.pause(0.0005)

            i+=1

    # set the angular momentum and energy as a fraction of its initial value (percentages)
        absenglist = []
        absangmomlist = []
        for i in range(len(englist)):
            absenglist.append(englist[i]/starteng)
            absangmomlist.append(angmomlist[i]/startangmom)

        # print Energydifference error

        dE =(englist[0] - englist[-1])/englist[0]
        print "The error for timesteps of %0.1f = %e" %(ic.dt,dE)

        # clock end time if timer is true
        if ic.timer == True:
            end = time.clock()
            timespent.append(end-start)

        p+=1

    ax1.plot(xplist,yplist,label= "Planet: " + method)
    ax1.plot(xslist,yslist, label = "Star: " + method)
    ax2.plot(range(0,ic.stepamount),absenglist, label = method)
    ax3.plot(range(0,ic.stepamount),absangmomlist, label = method)


    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'upper left')
    ax3.legend(loc = 'upper left')
    plt.legend()

    # take everage median and deviation of time loops if timer is true
    if ic.timer == True:
        average = np.average(timespent)
        median = np.median(timespent)
        deviation = np.std(timespent)
        text = "Time spent (s)\n\naverage = %.4f \nmedian = %.4f \ndeviation %.4f" %(average,median,deviation)
        fig.text(.91,.8,text)

    if ic.hourmonth:
        fig.savefig('2body_%s_a%0.2e_e%0.3f_stepsize_%s.png' %(method,ic.a,ic.e,ic.timehdwm))
    else:
        fig.savefig('2body_%s_a%0.2e_e%0.3f_stepsize%s.png' %(method,ic.a,ic.e,ic.dt))
    plt.show()



# if plotting hour week and month simultaneously set proper time steps and dt
def Checkhourmonthday(h,p):
    if ic.hourmonth == True:
        while h < 4:
            if h == 0:
                ic.dt = 3600
                ic.stepamount = 43800
                ic.timehdwm = "hours"

            if h == 1:
                ic.dt = 86400
                ic.stepamount = 1825
                ic.timehdwm = "days"

            if h == 2:
                ic.dt = 604800
                ic.stepamount =261
                ic.timehdwm = "weeks"

            if h == 3:
                ic.dt = 2419200
                ic.stepamount = 65
                ic.timehdwm = "months"
            ic.Orbitals.instances = []
            Earth = ic.Planet("Earth",ic.a,ic.e,ic.q,ic.Mp)
            Sun = ic.Star("Sun",ic.Ms)
            Drawwhat(p)
            h+=1

    if ic.hourmonth == False:
        ic.Orbitals.instances = []
        Earth = ic.Planet("Earth",ic.a,ic.e,ic.q,ic.Mp)
        Sun = ic.Star("Sun",ic.Ms)
        Drawwhat(p)



# check whether use all methods or just one
def Drawwhat(p):
    if ic.calcAll == True:
        if ic.timer == True:
                da.plotAll(ic.dt,ic.stepamount,p)
        if ic.timer == False:
            p = 99
            da.plotAll(ic.dt,ic.stepamount,p)
    else:
        Draw(p)
Checkhourmonthday(h,p)
