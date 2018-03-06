import Eulerorbit as k
import Leapfrogorbit as lf
import initialOrbitals as ic
import RungeKutta2 as u
import AngEnergy as ae
import AskDraw as ad
import DrawAll as da
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import sys
import matplotlib.cm as cm


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
    q = ic.Ms/1.898e27
    Earth = ic.Planet("Planet",ic.a,ic.e,q,1.898e27)
    # Earth2 = ic.Planet("Planet",ic.a, ic.e,ic.q,ic.Mp)
    Earth2 = ic.Planet("Earth",ic.a *2, ic.e,ic.q,ic.Mp)
    print '\n'
    print 'Radius orbit 1 = ', ic.a * 2, 'm'
    print 'Radius orbit 2 = ', ic.a, 'm'
    print 'Stepsize dt    = ', ic.dt, 's'
    print 'Stepamount     = ', ic.stepamount, '\n'
    Sun = ic.Star("Star",ic.Ms)
    for i in ic.Orbitals.instances:
        i.CM()
    for i in ic.Orbitals.instances:
        i.InitialSpeed()
    for i in ic.Orbitals.instances:
        print 'Initial x position %s = %.4e m' % (i.name, i.x)
        print 'Initial y velocity %s = %.4e m/s' % (i.name, i.vy)


################
    # this calculates our energy and angularmomentum
    englist = []
    angmomlist = []
    i = 0

    # make sure that the initialv if using leapfrog is moved back by 0.5 dt
    initialv = False
    # Looping over the time steps
    while i < ic.stepamount:
        # print '\n\nHERE COMES TIMESTEP %i' % i
        # if i == 10:
        #     break

        # determine which calculation we will perform
        if ic.calcEuler:
            k.calcEuler(ic.dt)
        if ic.calcLeap:
            initialv = lf.calcLeap(ic.dt,initialv)
        if ic.calcRK:
            u.calcRK(ic.dt)


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

    x10list=[]
    y10list = []
    xs10list=[]
    ys10list = []
    for i in ic.Orbitals.instances:
        # if i.name == "Earth":
        #     for j in range(len(i.xlist)):
        #         if j %10 ==0:
        #             x10list.append(i.xlist[j])
        #             y10list.append(i.ylist[j])
        # if i.name == "Star":
        #     for j in range(len(i.xlist)):
        #         if j %10 ==0:
        #             xs10list.append(i.xlist[j])
        #             ys10list.append(i.ylist[j])


        ax1.plot(i.xlist,i.ylist,label = i.name)
        # ax2.scatter(i.xlist,i.ylist,label=i.name)
    # colors = iter(cm.rainbow(np.linspace(0, 1, len(x10list))))
    # for i in range(len(x10list)):
    #     colorz = next(colors)
    #     ax2.scatter(x10list[i],y10list[i],color=colorz,label= str(i*10) +"th step")
    #     ax2.scatter(xs10list[i],ys10list[i],color=colorz)
    ax2.plot(range(0,ic.stepamount),absenglist, label = method)
    ax3.plot(range(0,ic.stepamount),absangmomlist, label = method)


    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'upper left')
    ax3.legend(loc = 'upper left')
    plt.legend()

    plt.savefig("plot_with_dt_"+str(ic.dt) +"and_years_"+str(ic.stepamount*ic.dt/(365.25*25*3600))+".png")

Draw()
