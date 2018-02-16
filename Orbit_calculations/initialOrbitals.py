
import numpy as np


# parent class for orbitals
class Orbitals:

    instances = []
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
        self.y = 0
        self.vx = 0
        Orbitals.instances.append(self)

# inherit Orbital parent qualities and define a planet
class Planet(Orbitals):
    def __init__(self,name,a,q,e,mass):
        self.a = a
        self.e = e
        self.vy = (1/(1+q))*np.sqrt(((1+e)/(1-e))) * np.sqrt((G*(Mp + Ms))/a)
        self.x =((1-e)/(1+q))*a
        Orbitals.__init__(self,name,mass)

# inherit Orbital parent qualities and define a star
class Star(Orbitals):
    def __init__(self,name,mass):
        self.vy = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].vy
        self.vx = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].vx
        self.x = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].x
        self.y = -Orbitals.instances[0].mass / mass * Orbitals.instances[0].y
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
