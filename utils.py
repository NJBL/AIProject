import math

# GLOBAL CONSTANTS
# Using Subaru WRX as example car
gears = [3.17, 1.88, 1.3, 0.97, 0.74] # 5 gears
final_drive = 3.9 # Final Drive Ratio
tire_diameter = 25.3 # stock 17" wheels, in inches

#Environment Constants
step = 52.8 # feet, (1 mile / 100)


# Variables, current attributes of the car
CUR_GEAR = 1 # Not starting at 0 because that would be confusing, starting at 1
RPM = 0 # init to idle
MPH = 0 # init to stopped

def getMPH(gears = gears, final_drive = final_drive, tire_diameter = tire_diameter, CUR_GEAR = CUR_GEAR, RPM = RPM):
  #global gears, final_drive, tire_diameter, CUR_GEAR, RPM
  return (RPM*tire_diameter)/(gears[CUR_GEAR]*final_drive*336)
def getRPM(gears = gears, final_drive = final_drive, tire_diameter = tire_diameter, CUR_GEAR = CUR_GEAR, MPH = MPH):
  #global gears, final_drive, tire_diameter, CUR_GEAR, MPH
  return (MPH*gears[CUR_GEAR]*final_drive*336)/(tire_diameter)



# Basic Shifting functions
def shift_up():
  global CUR_GEAR
  if len(gears) > CUR_GEAR:
    CUR_GEAR += 1
    return True
  else:
    return False

def shift_down():
  global CUR_GEAR
  if CUR_GEAR > 1:
    CUR_GEAR -= 1
    return True
  else:
    return False
