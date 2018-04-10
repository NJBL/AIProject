import math
import numpy as np
import matplotlib.pyplot as plt #temp

# GLOBAL CONSTANTS
# Using Subaru WRX as example car
gears = [3.17, 1.88, 1.3, 0.97, 0.74] # 5 gears
final_drive = 3.9 # Final Drive Ratio
tire_diameter = 25.3 # stock 17" wheels, in inches
idle_rpm = 750
weight = 3333 # lbs
rolling_resistance = 0.02 # average rr constant
drag_coef = 0.35
tran_efficiency = 0.8
car_data = np.array([
  (1013, 117.2),
  (1496, 136.1),
  (2019, 174.3),
  (2525, 235.8),
  (3015, 259.6),
  (3510, 280.0),
  (3815, 275.4),
  (4008, 273.2),
  (4213, 271.1),
  (4513, 265.4),
  (5015, 261.3),
  (5523, 245.8),
  (5812, 240.7),
  (6014, 225.6),
  (6211, 210.7),
])
rpms = car_data[:,0]
trqs = car_data[:,1]
z = np.polyfit(rpms, trqs, 3)
dfunc = np.poly1d(z)
fit_rpms = np.linspace(rpms[0], rpms[-1], 1000)
fit_trqs = dfunc(fit_rpms)

torque_curve = 0
#Environment Constants
step = 52.8 # feet, (1 mile / 100)


# Variables, current attributes of the car
CUR_GEAR = 1 # Not starting at 0 because that would be confusing, starting at 1
RPM = idle_rpm # init to idle
MPH = 0 # init to stopped
ACC = 1.0 # init to stopped
ALT = 0 # assumes starting at 0 alt
ANG = 0

# Useful Utilities
# 
def rpm_to_trq(rpm):
  return fit_trqs[(np.abs(fit_rpms-rpm)).argmin()]

def rpm_to_hp(rpm):
  return rpm_to_trq(rpm) * rpm / 5252

def acceleration(trq, MPH = MPH, drag_coef = drag_coef, rolling_resistance = rolling_resistance, weight = weight):
  return (trq - (drag_coef * MPH) - (rolling_resistance * MPH)) / weight

print rpm_to_trq(3000)
print rpm_to_hp(3000)
print acceleration(rpm_to_trq(3000),20)


# Car Physics

# 
# def acceleration(RPM = RPM, CUR_GEAR = CUR_GEAR, final_drive = final_drive, tran_efficiency = tran_efficiency, tire_diameter = tire_diameter):
#   wheel_torque = rpm_to_trq(RPM) * gears[CUR_GEAR] * final_drive * tran_efficiency / (tire_diameter / 2)  
#   return wheel_torque
# print acceleration(3000)

# def acceleration(steps):
#   f_trac = 1.0 - abs(ang_delta(steps))
#   f_drag = drag_coef * velocity()
#   f_rr = rolling_resistance * velocity()
#   return (f_trac - f_drag + f_rr) / weight





# "Driver" functions

# percent acceleration, amount of acceleration accounting for turns
def perc_acc(steps):
  return 1.0 - abs(ang_delta(steps))

# average turn angle of visible track ahead
def ang_delta(steps):
  return ANG - (reduce(lambda step, next: step[1] + next[1], steps)/len(steps))

def alt_delta(steps):
  return ALT - (reduce(lambda step, next: step[0] + next[0], steps)/len(steps))

def slip():
  return 0

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
