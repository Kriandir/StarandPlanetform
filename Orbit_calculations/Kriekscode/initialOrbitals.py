
import numpy as np
import inspect


# parent class for orbitals
class Orbitals(object):
    """Initiation mainclass for all orbitals"""

    instances = []
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
        self.ax = 0
        self.ay = 0
        self.rungevalues = []
        self.xlist = []
        self.ylist = []
        Orbitals.instances.append(self)

    def CM(self):
        # calculate center of mass based on amount of objects
        # and reset the coordinate system to the center of mass
        masses = 0
        xpositions = 0
        ypositions = 0
        for i in Orbitals.instances:
            masses += i.mass
            xpositions += i.mass * i.x
            ypositions += i.mass * i.y

        rx = xpositions/masses
        ry = ypositions/masses

        self.x = self.x - rx
        self.y = self.y -ry

    def RKCM(self,dt):
        # calculate center of mass based on amount of objects
        # and reset the coordinate system to the center of mass
        masses = 0
        xpositions = 0
        ypositions = 0
        for i in Orbitals.instances:
            masses += i.mass
            xpositions += i.mass * (i.x + i.rungevalues[-1][0]*dt)
            ypositions += i.mass * (i.y + i.rungevalues[-1][1]*dt)

        rx = xpositions/masses
        ry = ypositions/masses

        return rx,ry

    def InitialSpeed(self):

# If object is a planet calculate its velocity
        if isinstance(self,Planet):
            self.vy = (1/(1+q))*np.sqrt(G*(Ms+self.mass)/self.x)



#  IF object is a star calculate its velocity
        if isinstance(self,Star):
            massvsum = 0

            for i in Orbitals.instances:
                if i.name == 'Planet':
                    massvsum +=i.mass * i.vy

            self.vy = -1/self.mass * massvsum



# inherit Orbital parent qualities and define a planet
class Planet(Orbitals):
    """Initiazion planet subclasses"""

    def __init__(self,name,a,q,e,mass):
        self.x = a
        self.e = e
        self.vy = 0
        self.y = 0
        self.vx = 0
        self.q = q


        Orbitals.__init__(self,name,mass)


# inherit Orbital parent qualities and define a star
class Star(Orbitals):
    """Initization star subclasses"""
    def __init__(self,name,mass):
        self.x = 0
        self.y = 0
        self.vy = 0
        self.vx = 0
        Orbitals.__init__(self,name,mass)


# default values
Mp = 5.972e24
Ms = 1.989e30
q = Mp/Ms
dt = 3600*24*365.25*0.01
stepamount = int((10*365.25*3600*24)/dt)
a =1.496e11
e =0.0167
G = 6.67408e-11
tstop = 10.*(365.25*24*3600)
directdraw  = False
calcEuler = False
calcLeap = False
calcRK = False
gashead = 0.1
calcAll = False
timer = False
hourmonth = False
timehdwm = ""

# x = ((1-e)/(1+q))*a
# v =  (1/(1+q))*np.sqrt(((1+e)/(1-e))) * np.sqrt((G*(Mp + Ms))/a)
