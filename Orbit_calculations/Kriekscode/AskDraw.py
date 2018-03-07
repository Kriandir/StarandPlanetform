import sys
import initialOrbitals as ic



# def askdefaults():
#     default = raw_input("Would you like to use the default settings? (y/n) ").lower()
#     if default == "n":
#
#         while True:
#             try:
#                 a = raw_input("Please insert a semi-major axis in m:").lower()
#                 ic.a = float(a)
#                 break
#             except(KeyboardInterrupt):
#                 sys.exit(0)
#             except:
#                 continue
#
#         while True:
#             try:
#                 e = raw_input("Please insert an eccentricity between or equal to 0 and 1:").lower()
#                 e = float(e)
#
#                 if 0<=e<=1:
#                     ic.e =e
#                     break
#             except(KeyboardInterrupt):
#                 sys.exit(0)
#             except:
#                 continue
#         asktimesteps()
#
#
#     if default == "y":
#         asktimesteps()
#     if default != "y" and default !="n":
#         askdefaults()

def asktimesteps():

        # hourmonth = raw_input("Would you like to plot for hours, days, months and years? (y/n) ").lower()
        # if hourmonth == "y":
        #     ic.hourmonth = True
        #     asktime()
        #
        # if hourmonth =="n":

    asktimes = raw_input("Would you like to set timesteps/stepamount? (y/n) ").lower()
    if asktimes == "y":

        while True:
            try:
                dt = raw_input("Please insert a timestep in years:")
                dt = float(dt)*365.25*24*3600
                stepamount = 1e8/dt
                ic.stepamount = int(stepamount)
                ic.dt = int(dt)
                break
            except(KeyboardInterrupt):
                sys.exit(0)

            except:
                continue



    asksteps = raw_input("would you like to insert stepamount?(y/n): ").lower()
    # if asksteps =='y' or asksteps =='n':
    #     break
# except(KeyboardInterrupt):
#     sys.exit(0)
# except:
#     continue


    if asksteps =='y':
        while True:
            try:
                print 'yo'
                steps = raw_input("Please insert integration time in integer years:")
                # set the timestop on 10 years and see this is most likely faulty
                ic.tstop = 10./(365.25*24*3600)
                print ic.tstop
                steps = float(steps)*365.25*24*3600
                ic.stepamount = int(steps/dt)
                print ic.stepamount
                break
            except(KeyboardInterrupt):
                sys.exit(0)
            except:
                continue

    if asksteps =='n':
        ic.calcRK = True
        return 0


    if asktimes == "n":
        # asktime()
        ic.calcRK = True
        return 0
    if asktimes != "y" and asktimes !="n":
        asktimesteps()
    # asktime()
    ic.calcRK = True
        # if hourmonth !="n" and hourmonth !="y":
        #     asktimesteps()

# def asktimesteps():
#         hourmonth = raw_input("Would you like to plot for hours, days, months and years? (y/n) ").lower()
#         if hourmonth == "y":
#             ic.hourmonth = True
#             asktime()
#
#         if hourmonth =="n":
#             while True:
#                 try:
#                     dt = raw_input("Please insert a timestep in integer seconds:").lower()
#                     ic.dt = int(dt)
#                     break
#                 except:
#                     continue
#             while True:
#                 try:
#                     steps = raw_input("Please insert amount of timesteps in integer:").lower()
#                     ic.stepamount = int(steps)
#                     break
#                 except:
#                     continue
#             asktime()
#         if hourmonth !="n" and hourmonth !="y":
#             asktimesteps()

# def asktime():
#     timer = raw_input("Would you like to time your code? (y/n) ").lower()
#     if timer == "y":
#         ic.timer= True
#         askall()
#     if timer == "n":
#         asklive()
#     if timer != "y" and timer !="n":
#         asktime()

#
# def asklive():
#     draw = raw_input("Would you like to plot a live image? (y/n) ").lower()
#     if draw == "y":
#         ic.directdraw = True
#         askeuler()
#     if draw != "y" and draw !="n":
#         asklive()
#     if draw == "n":
#         askall()
#
# def askall():
#     plotall =  raw_input("Would you like to run all the calculations? (y/n) ").lower()
#     if plotall == "y":
#         ic.calcAll = True
#         return 0
#     if plotall != "y" and plotall !="n":
#         askall()
#     if plotall =="n":
#         askeuler()

def askeuler():
    euler = raw_input("Would you like to run Euler? (y/n) ").lower()
    if euler == "y":
        ic.calcEuler = True
        return 0
    if euler != "y" and euler !="n":
        askeuler()
    if euler =="n":
        askleap()

def askleap():
    leap = raw_input("Would you like to run Leapfrog? (y/n) ").lower()

    if leap == "y":
        ic.calcLeap = True
        return 0
    if leap != "y" and leap !="n":
        askleap()
    if leap == "n":
        askRK()

def askRK():
    RK = raw_input("Would you like to run Runge-Kutta? (y/n) ").lower()
    if RK == "y":
        ic.calcRK = True
        return 0
    if RK != "y" and RK !="n":
        askRK()
    if RK == "n":
        sys.exit("Error message: YOLO")
