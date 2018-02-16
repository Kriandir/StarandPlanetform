import Eulerorbit as k
import Leapfrogorbit as lf
import initialOrbitals as ic
import RungeKutta as u
import AngEnergy as ae
import AskDraw as ad
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import sys

timespent = []
# function for plotting all the functions in a single plot
def plotAll(dt,stepamount,p):

    # make sure that the initialv of leapfrog is moved back by 0.5 dt
    initialv = False

    # define the figure
    fig = plt.figure("2 body system", figsize=(20,10))
    ax1 = fig.add_subplot(311)
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax2 = fig.add_subplot(312)
    ax2.set_ylabel("Energydifference in %")
    ax3 = fig.add_subplot(313,sharex = ax2,sharey= ax2)
    ax3.set_ylabel("Angularmomentum in  %")
    # ax2.axis([-1,ic.stepamount+1,0.8,1.02])
    if ic.hourmonth == True:
        ax2.set_xlabel("Steps of %s" % ic.timehdwm)
        ax3.set_xlabel("Steps of %s" % ic.timehdwm)
        plt.suptitle("2 body system using all the methods for a = %0.3e, eccentricity = %0.4f and timestep of %s for a period of 5 years" \
         % (ic.a, ic.e,ic.timehdwm),fontsize=16)

    if ic.hourmonth == False:
        ax2.set_xlabel("Steps of %i (s)" % ic.dt)
        ax3.set_xlabel("Steps of %i (s)" % ic.dt)
        years = (ic.dt * ic.stepamount)/157680000.
        plt.suptitle("2 body system using all the methods for a = %0.3e, eccentricity = %0.4f and timestep of %i seconds for a period of %0.3f years" % (ic.a, ic.e,ic.dt,years),fontsize=16)


    while p < 100:
        if ic.timer == True:
            start = time.clock()

            # loop through the calculations
            for j in range(0,3):

            #   set initial values for each calculation

                xplist = []
                yplist = []
                xslist = []
                yslist = []
                englist = []
                angmomlist = []
                i = 0
                ic.Orbitals.instances = []
                Earth = ic.Planet("Earth",ic.a,ic.e,ic.q,ic.Mp)
                Sun = ic.Star("Sun",ic.Ms)

                while i < stepamount:

                    # determine which calculation we will perform
                    if j == 0:


                        k.calcEuler(dt)
                    if j == 1:
                        legendname = "LF"

                        initialv = lf.calcLeap(dt,initialv)
                    if j == 2:
                        legendname = "RK"
    
                        u.calcRK(dt)


                    # append data to list

                    yplist.append(ic.Orbitals.instances[0].y)
                    xplist.append(ic.Orbitals.instances[0].x)
                    yslist.append(ic.Orbitals.instances[1].y)
                    xslist.append(ic.Orbitals.instances[1].x)

                    #  calculate energy and angular momentum
                    englist.append(ae.eng())
                    angmomlist.append(ae.angmom())

                    # take initial energy and angular momentum
                    if i == 0:
                        starteng = ae.eng()
                        startangmom = ae.angmom()

                    i+=1


                # calculate the normalized energy and angulermomentum

                absenglist = []
                absangmomlist = []
                for i in range(len(englist)):
                    absenglist.append(englist[i]/starteng)
                    absangmomlist.append(angmomlist[i]/startangmom)

                if p == 99:
                    # plot the figure and the star and the planet and the energy and the angular momentum if not timing
                        ax1.plot(xplist,yplist,label= "Planet: " + legendname)
                        ax1.plot(xslist,yslist, label = "Star: " + legendname)
                        ax2.plot(range(-1,stepamount+1),absenglist, label = legendname)
                        ax3.plot(range(-1,stepamount+1),absangmomlist, label = legendname)

            if p == 99:
                ax1.legend(loc = 'upper left')
                ax2.legend(loc = 'upper left')
                ax3.legend(loc = 'upper left')

                if ic.timer == True:
                    average = np.average(timespent)
                    median = np.median(timespent)
                    deviation = np.std(timespent)
                    text = "Time spent (s)\n\naverage = %.4f \nmedian = %.4f \ndeviation %.4f" %(average,median,deviation)
                    fig.text(.91,.8,text)

                if ic.hourmonth:
                    fig.savefig('2body_all_a%0.2e_e%0.3f_stepsize_%s.png' %(ic.a,ic.e,ic.timehdwm))
                else:
                    fig.savefig('2body_all_a%0.2e_e%0.3f_stepsize%s.png' %(ic.a,ic.e,ic.dt))
                # plt.show()
            # clock end time if timer is true
            if ic.timer == True:
                end = time.clock()
                timespent.append(end-start)
            p+=1
