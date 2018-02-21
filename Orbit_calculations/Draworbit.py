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

def Draw():

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


    ic.Orbitals.instances = []
    Earth = ic.Planet("Planet",ic.a,ic.e,ic.q,ic.Mp)


    Sun = ic.Star("Star",ic.Ms)
    for i in ic.Orbitals.instances:
        i.CM()
    for i in ic.Orbitals.instances:
        i.InitialSpeed()


    ##############TODO FIX THIS INTO CLASS
    xplist = []
    yplist = []
    xslist = []
    yslist = []
    ################################
    # this calculates our energy and angularmomentum
    englist = []
    angmomlist = []
    i = 0

    # make sure that the initialv if using leapfrog is moved back by 0.5 dt
    initialv = False

    # Looping over the time steps
    while i < ic.stepamount:

        # determine which calculation we will perform
        if ic.calcEuler:
            k.calcEuler(ic.dt)
        if ic.calcLeap:
            initialv = lf.calcLeap(ic.dt,initialv)
        if ic.calcRK:
            u.calcRK(ic.dt)

        ############after TODO not necessary###########################
        # if not live drawing append to list
        if ic.directdraw == False:

            yplist.append(ic.Orbitals.instances[0].y)
            xplist.append(ic.Orbitals.instances[0].x)
            yslist.append(ic.Orbitals.instances[1].y)
            xslist.append(ic.Orbitals.instances[1].x)

        ###############################################################

        # calculate energy and angular momentum

        englist.append(ae.eng())
        angmomlist.append(ae.angmom())

        # take initial energy and angular momentum
        if i == 0:
            starteng = ae.eng()
            startangmom = ae.angmom()


        i+=1

# set the angular momentum and energy as a fraction of its initial value (percentages)
    absenglist = []
    absangmomlist = []
    for i in range(len(englist)):
        absenglist.append(englist[i]/starteng)
        absangmomlist.append(angmomlist[i]/startangmom)

    # print Energydifference error

    dE =(englist[0] - englist[-1])/englist[0]
    print "The error for timesteps of %0.1f = %.2e" %(ic.dt,dE)


    ax1.plot(xplist,yplist,label= "Planet: " + method)
    ax1.plot(xslist,yslist, label = "Star: " + method)
    ax2.plot(range(0,ic.stepamount),absenglist, label = method)
    ax3.plot(range(0,ic.stepamount),absangmomlist, label = method)


    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'upper left')
    ax3.legend(loc = 'upper left')
    plt.legend()

    plt.show()

Draw()
