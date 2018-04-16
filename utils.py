import math
import cmath
import numpy as np
import matplotlib.pyplot as plt #temp

# GLOBAL CONSTANTS
# Using Subaru WRX as example car
gears = [3.17, 1.88, 1.3, 0.97, 0.74] # 5 gears
final_drive = 3.9 # Final Drive Ratio
tire_diameter = 0.65278 # meters, 25.3 inches: stock 17" wheels
idle_rpm = 750
redline_rpm = 6300
weight = 1511.823 #kg = 3333 lbs
rolling_resistance = 0.02 # average rr constant
drag_coef = 0.35
front_area = 2.043866 # 22 * 0.092903 sqare feet converted to square meters
length = 4.4196 # meters = 174 inches
tran_efficiency = 0.8
# RPM, Newtons of Torque
car_data = np.array([
  (1013, 159),
  (1496, 185),
  (2019, 236),
  (2525, 320),
  (3015, 352),
  (3510, 380),
  (3815, 373),
  (4008, 370),
  (4213, 368),
  (4513, 360),
  (5015, 354),
  (5523, 333),
  (5812, 326),
  (6014, 306),
  (6211, 286),
])
rpms = car_data[:,0]
trqs = car_data[:,1]
z = np.polyfit(rpms, trqs, 3)
dfunc = np.poly1d(z)
fit_rpms = np.linspace(rpms[0], rpms[-1], 1000)
fit_trqs = dfunc(fit_rpms)
# plt.plot(rpms, trqs, 'o', fit_rpms, fit_trqs)
# plt.show()

#Environment Constants
step = 100 # meters
air_dens = 1.225 # kg/m^3


# Variables, current attributes of the car
CUR_GEAR = 1 # Not starting at 0 because that would be confusing, starting at 1
RPM = idle_rpm # init to idle
MPS = 0 
#ACC = 0.0 # init to stopped
ALT = 0 # assumes starting at 0 alt
ANG = 0.0


# Car Physics





# "Driver" functions

# percent acceleration, amount of acceleration accounting for turns
def perc_acc(steps):
  return 1.0 - abs(ang_delta(steps))

def alt_delta(steps):
  return ALT - (sum((step[0] for step in steps))/len(steps))

# average turn angle of visible track ahead
def ang_delta(steps):
  return ANG - (sum((step[1] for step in steps))/len(steps))




# def getMPS(RPM = RPM, CUR_GEAR = CUR_GEAR, gears = gears, final_drive = final_drive, tire_diameter = tire_diameter):
#   #global gears, final_drive, tire_diameter, CUR_GEAR, RPM
#   return (RPM*tire_diameter)/(gears[CUR_GEAR]*final_drive*336)

def getRPM(MPS = MPS, CUR_GEAR = CUR_GEAR, gears = gears, final_drive = final_drive, tire_diameter = tire_diameter):
  #global gears, final_drive, tire_diameter, CUR_GEAR, MPS
  return (MPS*gears[CUR_GEAR]*final_drive*336)/(tire_diameter)

# Useful Utilities
# 
def rpm_to_trq(rpm):
  return fit_trqs[(np.abs(fit_rpms-rpm)).argmin()]

def rpm_to_hp(rpm):
  return rpm_to_trq(rpm) * rpm / 5252

def wheel_torque(rpm = RPM, CUR_GEAR = CUR_GEAR):
  return (rpm_to_trq(rpm) * gears[CUR_GEAR - 1] * final_drive * tran_efficiency) / tire_diameter

def drag(mps = MPS, drag_coef = drag_coef, front_area = front_area):
  return (0.5 * drag_coef * front_area * air_dens * (mps * mps)) + (rolling_resistance * mps)

def acceleration(RPM = RPM, MPS = MPS, CUR_GEAR = CUR_GEAR, rolling_resistance = rolling_resistance, weight = weight):
  return (wheel_torque(RPM, CUR_GEAR) - drag(MPS, drag_coef)) / weight
print wheel_torque(3500, 3) 
print acceleration(3500, 30, 3)

def slip(steps, MPS = MPS):
  angle = 90.0 * abs(ang_delta(steps))
  radius = length / (math.sin(math.radians(angle)))
  lat_force = (weight * (MPS * MPS)) / radius
  #print radius, lat_force, weight
  return lat_force >= weight

print slip([(0, 0.99)], 1)
print slip([(0, 0.99)], 2)
print slip([(0, 0.99)], 20)

def next_speed(RPM = RPM, MPS = MPS, CUR_GEAR = CUR_GEAR):
  acc = acceleration(RPM, MPS, CUR_GEAR)
  # a = acc / 2
  # b = MPS
  # c = 100

  # #The Discriminant
  # d = (b**2) - (4*a*c)

  # #The Solutions
  # solution1 = (-b-cmath.sqrt(d))/(2*a)
  # solution2 = (-b+cmath.sqrt(d))/(2*a)
  # print (solution1)
  # print (solution2)
  return 0
#next_speed(3500, 30, 3)


# Basic Shifting functions
def shift_up():
  global CUR_GEAR, RPM
  if len(gears) > CUR_GEAR:
    CUR_GEAR += 1
    RPM = getRPM() 
    return True
  else:
    return False

def shift_down():
  global CUR_GEAR, RPM
  if CUR_GEAR > 1:
    CUR_GEAR -= 1
    RPM = getRPM()
    return True
  else:
    return False

peak_trq = max(fit_trqs)
peak_hp = max(rpm_to_hp(rpm) for rpm in fit_rpms)


# def estimate_visible(steps):
#   global RPM, MPH, ACC
#   rpm = RPM
#   mph = MPH
#   acc = ACC
#   for i in range(len(steps)):
#     acc = acceleration(rpm, mph) * perc_acc(steps[i:])
#     mph = mph + (step/5280) * 
#     rpm = getRPM(mph)
#   RPM = rpm
#   MPH = mph
#   ACC = acc
#   return acc, mph, rpm
