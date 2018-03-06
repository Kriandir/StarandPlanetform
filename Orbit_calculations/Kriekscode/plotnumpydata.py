import numpy as np
import matplotlib.pyplot as plt
import os
import sys


if len(sys.argv)!=2:
    print "Please enter directory of numpy data to plot"
else:
    # load in data
    directory = sys.argv[1]
    os.chdir(directory)
    Orbitals = np.load("Orbitals.npy")
    absenglist = np.load("englist.npy")
    absangmomlist = np.load('anglist.npy')
    stepamount = np.load('stepamount.npy')

    # define the figure
    fig = plt.figure("2 body system", figsize=(20,10))
    ax1 = fig.add_subplot(311)
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax2 = fig.add_subplot(312)
    ax2.set_ylabel("Energydifference in %")
    ax3 = fig.add_subplot(313,sharex = ax2,sharey= ax2)
    ax3.set_ylabel("Angularmomentum in  %")

    #plot the data
    for i in Orbitals:
        ax1.plot(i.xlist,i.ylist,label = i.name)

    ax2.plot(range(0,stepamount),absenglist)
    ax3.plot(range(0,stepamount),absangmomlist)
    plt.show()
