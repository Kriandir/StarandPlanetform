import sys
import initialOrbitals as ic


def asktimesteps():

    askhw = raw_input("Would you like to set the hw y=yes?").lower()
    if askhw == 'y':

        while True:
            try:
                v_hw = raw_input("Please insert a percentage of the Keplerian velocity: ")
                v_hw = float(v_hw) / 100.
                ic.gashead = v_hw
                break

            except(KeyboardInterrupt):
                sys.exit(0)

            except:
                continue


    asktimes = raw_input("Would you like to set timesteps/stepamount? (y/n) ").lower()
    if asktimes == "y":

        while True:
            try:
                dt = raw_input("Please insert a timestep in years:")
                dt = float(dt)*365.25*24*3600           # Convert years to seconds
                ic.dt = int(dt)
                break

            except(KeyboardInterrupt):
                sys.exit(0)

            except:
                continue


    asksteps = raw_input("would you like to insert stepamount?(y/n): ").lower()
    if asksteps =='y':
        while True:
            try:
                steps = raw_input("Please insert integration time in integer years:")
                steps = float(steps)*365.25*24*3600     # Convert years to seconds
                ic.stepamount = int(steps/ic.dt)
                break
            except(KeyboardInterrupt):
                sys.exit(0)
            except:
                continue

    if asksteps =='n':
        ic.calcRK = True
        return 0

    if asktimes == "n":
        ic.calcRK = True
        return 0

    if asktimes != "y" and asktimes !="n":
        asktimesteps()

    ic.calcRK = True