from __future__ import division
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
import os
AU = 1.5e11 
Mj = 1.898e27

# ask which method to use and if we want to time
try:
    ad.asktimesteps()
except(KeyboardInterrupt):
    sys.exit(0)

def calc_resonance_orbits(P_fraction):
    r = P_fraction**(2. / 3) * ic.a
    x = []
    y = []
    for theta in np.linspace(0, (2*np.pi), num=1000):
        x.append(r * np.cos(theta))
        y.append(r * np.sin(theta))
    return x, y

def Draw(headwind_var):
    ic.gashead = headwind_var

    # decide if save or plot figure
    save = False
    colorplot = False

    if ic.calcRK:
        method = "RK"
        name = "Runge-Kutta"

    # define the figure
    fig = plt.figure("2 body system", figsize=(10,20))
    # ax1 = fig.add_subplot(311)
    # ax1 = fig.add_subplot(111)
    # ax1.set_xlabel("x (AU)")
    # ax1.set_ylabel("y (AU)")
    # ax1.set_title('hw = %.1f percent , runtime = %.f yrs' % (ic.gashead * 100, ic.stepamount / 100. ))

    ax2 = fig.add_subplot(111)
    ax2.set_xlabel('Time (yrs)')
    ax2.set_ylabel('Distance to sun (AU)')     
    # ax2.set_ylabel("Energydifference in %")
    # ax3 = fig.add_subplot(313,sharex = ax2,sharey= ax2)
    # ax3.set_ylabel("Angularmomentum in  %")

    ic.Orbitals.instances = []
    q = ic.Ms/Mj			# Mass ratio sun / jup
    Earth = ic.Planet("Planet", "Jupiter", ic.a, ic.e, q, Mj, 'red')
    Earth2 = ic.Planet("Earth", "Earth", ic.a * 2, ic.e, ic.q, ic.Mp, 'blue')

    print 'Working on body no. %s'%str(master_index+1)
    # print 'Radius orbit 1 = ', ic.a * 2/ AU, 'AU'
    # print 'Radius orbit 2 = ', ic.a/ AU, 'AU'
    # print 'Stepsize dt    = ', ic.dt, 's'
    # print 'Stepamount     = ', ic.stepamount, '\n'

    Sun = ic.Star("Star", "Sun", ic.Ms, 'black')

    for i in ic.Orbitals.instances:
        if 'HW' in i.name:
            continue
        else:    
            i.CM()

    for i in ic.Orbitals.instances:
        i.InitialSpeed()
    # for i in ic.Orbitals.instances:
    #     print 'Initial x position %s = %.4e AU' % (i.name, i.x/AU)
    #     print 'Initial y velocity %s = %.4e m/s' % (i.name, i.vy)


################
    # this calculates our energy and angularmomentum
    englist = []
    angmomlist = []
    i = 0

    # make sure that the initialv if using leapfrog is moved back by 0.5 dt
    # Looping over the time steps
    while i < ic.stepamount:
        # determine which calculation we will perform
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

    x10list=[]
    y10list = []
    xs10list=[]
    ys10list = []

    res_colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']

    k = 0
    testMassNum = 0
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


        # ax1.plot(np.array(i.xlist) / ic.a, np.array(i.ylist) / ic.a, label = i.expl_name, c=i.color)


        if i.name == "Earth":
            dist_sun = np.sqrt(np.array(i.xlist)**2 + np.array(i.ylist)**2) / ic.a
            ax2.plot(np.arange(len(dist_sun)) / 100., dist_sun, label='HW = '+str(ic.gashead * 100)+'%'+' of v_k', c=res_colors[master_index])

        k += 1

    
    # colors = iter(cm.rainbow(np.linspace(0, 1, len(x10list))))
    # for i in range(len(x10list)):
    #     colorz = next(colors)
    #     ax2.scatter(x10list[i],y10list[i],color=colorz,label= str(i*10) +"th step")
    #     ax2.scatter(xs10list[i],ys10list[i],color=colorz)
    # ax2.plot(range(0,ic.stepamount),absenglist, label = method)
    # ax3.plot(range(0,ic.stepamount),absangmomlist, label = method)
    cwd = os.getcwd()
    newdir = cwd+"/"+"dt_of_"+str(int(ic.dt))+"years_of"+str(int(ic.stepamount*ic.dt/(365.25*25*3600)))
    try:
        os.mkdir(newdir)
    except:
        pass

    os.chdir(newdir)
    # ax1.legend(loc = 'upper left')
    # ax2.legend(loc = 'upper left')
    # ax3.legend(loc = 'upper left')

    # add resonance orbits
    resonances = [1/2, 2/3, 3/4, 2, 3/2, 4/3]
    resonances_labels = ['1/2', '2/3', '3/4', '2', '3/2', '4/3']

    res_colors = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']
    col = 0

    if master_index == lenHWs - 1:
        for frac in resonances:
            x, y = calc_resonance_orbits(frac)
            if frac < 1:
                # ax1.plot(np.array(x) / ic.a, np.array(y) / ic.a, c=res_colors[col], ls='dotted', lw=2, label='Pe/Pj = %s'%resonances_labels[col])
                ax2.axhline(np.sqrt(np.array(x[0])**2 + np.array(y[0])**2) / ic.a, c=res_colors[col], ls='dotted', label='Pe/Pj = %s'%resonances_labels[col])
            else:
                # ax1.plot(np.array(x) / ic.a, np.array(y) / ic.a, c=res_colors[col], ls='dashed', lw=2, label='Pe/Pj = %s'%resonances_labels[col])
                ax2.axhline(np.sqrt(np.array(x[0])**2 + np.array(y[0])**2) / ic.a, c=res_colors[col], ls='dashed', label='Pe/Pj = %s'%resonances_labels[col])

            col += 1

        ax2.axhline(1, c='red', label="Jupiter's orbit")
        # ax2.axhline(1.06815, c='red', label="Jupiter's Hillsphere", alpha=0.6)
        ax2.fill_between(np.arange(-100, 1000), 1, 1.06815, label="Jupiter's Hillsphere", alpha=0.3, color='red')

        # plt.savefig('plot_with_hw_'+str(ic.gashead * 100)+'percent_and_runtime_'+str(ic.stepamount / 100.)+'yrs.png')
        ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=5)

    if save:
        np.save("Orbitals.npy",ic.Orbitals.instances)
        np.save("englist.npy",absenglist)
        np.save("anglist.npy",absangmomlist)
        np.save("stepamount.npy",ic.stepamount)
        print 'saving under:' + str(newdir)
        plt.savefig("plot_with_dt_"+str(ic.dt) +"and_years_"+str(ic.stepamount*ic.dt/(365.25*25*3600))+".png")



# headwinds = np.arange(3.05, 3.56, 0.1)
headwinds = [2.9, 3.05, 3.25]
lenHWs = len(headwinds)
master_index = 0
for i in range(len(headwinds)):
    Draw(headwinds[i] / 100)
    master_index += 1

plt.show()
