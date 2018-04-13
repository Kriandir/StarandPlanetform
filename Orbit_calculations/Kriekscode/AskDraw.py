import sys
import initialOrbitals as ic


def asktimesteps():

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

    ic.calcRK = True