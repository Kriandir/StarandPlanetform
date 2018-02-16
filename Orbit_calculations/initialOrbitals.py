
import numpy as np


# parent class for orbitals
class Orbitals(object):

    instances = []
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
        # self.y = 0
        # self.vx = 0
        # self.x = 0
        # self.vy = 0
        Orbitals.instances.append(self)

    def CM(self):
        # calculate center of mass based on amount of objects
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


    def InitialSpeed(self):

# If object is a planet calculate its velocity
        if self.name == 'Planet':
            self.vy = (1/(1+q))*np.sqrt(G*(Ms+self.mass)/self.x)



#  IF object is a star calculate its velocity
        if self.name == "Star":
            massvsum = 0

            for i in Orbitals.instances:
                if i.name == 'Planet':
                    massvsum +=i.mass * i.vy

            self.vy = -1/self.mass * massvsum







# inherit Orbital parent qualities and define a planet
class Planet(Orbitals):

    def __init__(self,name,a,q,e,mass):
        self.x = a
        self.e = e
        self.vy = 0
        self.y = 0
        self.vx = 0
        # self.vy = (1/(1+q))*np.sqrt(((1+e)/(1-e))) * np.sqrt((G*(Mp + Ms))/a)
        # self.x =((1-e)/(1+q))*a

        Orbitals.__init__(self,name,mass)


# inherit Orbital parent qualities and define a star
class Star(Orbitals):
    def __init__(self,name,mass):
        self.x = 0
        self.y = 0
        self.vy = 0
        self.vx = 0
        # self.vy = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].vy
        # self.vx = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].vx
        # self.x = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].x
        # self.y = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].y
        # Star.instances.append(self)
        Orbitals.__init__(self,name,mass)


# default values
Mp = 5.972e24
Ms = 1.989e30
q = Mp/Ms
dt = 3600*24*3
stepamount = int(1e8/dt)
a =1.496e11
e =0.0167
G = 6.67408e-11

directdraw  = False
calcEuler = False
calcLeap = False
calcRK = False
calcAll = False
timer = False
hourmonth = False
timehdwm = ""

x = ((1-e)/(1+q))*a
v =  (1/(1+q))*np.sqrt(((1+e)/(1-e))) * np.sqrt((G*(Mp + Ms))/a)
