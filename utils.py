import math
import cmath
import numpy as np
import matplotlib.pyplot as plt #temp




# GLOBAL CONSTANTS
# Using Subaru WRX as example car



#Environment Constants
step = 10 # meters
air_dens = 1.225 # kg/m^3



#percent acceleration, amount of acceleration accounting for turns
def perc_acc(steps):
  angle = abs(ang_delta(steps))
  return 1.0 - (angle)

def alt_delta(steps):
  return (sum((float(step[0]) for step in steps))/len(steps))

# average turn angle of visible track ahead
def ang_delta(steps):
  return (sum((float(step[1]) for step in steps))/len(steps))




class WRX(object):
  gears = [3.17, 1.88, 1.3, 0.97, 0.74] # 5 gears
  final_drive = 3.9 # Final Drive Ratio
  tire_diameter = 0.65278 # meters, 25.3 inches: stock 17" wheels
  tire_radius = tire_diameter / 2
  idle_rpm = 750
  redline_rpm = 6300
  weight = 1511.823 #kg = 3333 lbs
  rolling_resistance = 0.02 # average rr constant
  drag_coef = 0.35
  front_area = 2.043866 # 22 * 0.092903 sqare feet converted to square meters
  length = 4.4196 # meters = 174 inches
  tran_efficiency = 0.8 # estimated, but realistic
  braking_dec = -8.0 # meters per sec^2


  CUR_GEAR = 1 # Not starting at 0 because that would be confusing, starting at 1
  RPM = idle_rpm # init to idle
  MPS = 0 # starting from a stop
  
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



  def __init__(self, ALT, ANG):
    self.ALT = ALT
    self.ANG = ANG
  def setVals(self, MPS, RPM, CUR_GEAR):
    self.RPM = RPM
    self.MPS = MPS
    self.CUR_GEAR = CUR_GEAR

  def getRPM(self, MPS, CUR_GEAR):
    #global final_drive, tire_diameter, CUR_GEAR, MPS
    return (MPS/self.tire_radius) * self.gears[CUR_GEAR - 1] * self.final_drive * self.tran_efficiency * 60/(2 * math.pi)
  def getMPS(self, RPM, CUR_GEAR):
    return (RPM*self.tire_radius)/(self.gears[CUR_GEAR-1]*self.final_drive*self.tran_efficiency * 60/(2 * math.pi))
  
  # Useful Utilities
  # 
  def rpm_to_trq(self, rpm):
    return self.fit_trqs[(np.abs(self.fit_rpms-rpm)).argmin()]

  def rpm_to_hp(self, rpm):
    return self.rpm_to_trq(rpm) * rpm / 5252

  def wheel_torque(self, rpm, CUR_GEAR):
    return (self.rpm_to_trq(rpm) * self.gears[CUR_GEAR - 1] * self.final_drive * self.tran_efficiency) / self.tire_radius

  def drag(self, mps = MPS):
    return (0.5 * self.drag_coef * self.front_area * air_dens * (mps * mps)) + (self.rolling_resistance * mps)

  def acceleration(self, RPM, MPS, CUR_GEAR):
    force = self.wheel_torque(RPM, CUR_GEAR) - self.drag(MPS)
    return force / self.weight
  # print wheel_torque(idle_rpm, 2) 
  # print acceleration(idle_rpm, 0, 2)
  def slip_speed(self, steps):
    angle = 90.0 * abs(ang_delta(steps))
    if angle == 0:
      return 9999
    radius = self.length / (math.sin(math.radians(angle)))
    return math.sqrt(radius)


  def slip(self, steps, MPS):
    angle = 90.0 * abs(ang_delta(steps))
    if angle == 0.0: # eliminate divide by 0
      return False
    radius = self.length / (math.sin(math.radians(angle)))
    lat_force = (self.weight * (MPS * MPS)) / radius
    return lat_force >= self.weight

  # print slip([(0, 0.99)], 1)
  # print slip([(0, 0.99)], 2)
  # print slip([(0, 0.99)], 20)

  # def braking(self, MPS):
  #   overall_braking = (self.braking_dec * step) + self.drag(MPS)
  #   return -(overall_braking / self.weight)

  def time_between(self, a, b, c):
    if (b * b) - 4 * a * c < 0:
      discRoot = 1
    else:
      discRoot = math.sqrt((b * b) - 4 * a * c) # first pass
    root1 = (-b + discRoot) / (2 * a) # solving positive
    #root2 = (-b - discRoot) / (2 * a) # solving negative
    pos = "%.2f" % root1
    #neg = "%.2f" % root2
    return pos

  def next_speed(self, time, acc, s):
    return s + acc * float(time)
  # print(getRPM(30, 3))
  # print next_speed([(0, 0)], getRPM(30, 3), 30, 3)
  def peak_trq(self, CUR_GEAR):
    return max((self.wheel_torque(d[0], CUR_GEAR) for d in self.car_data))
  
  def peak_hp(self):
    return max((self.rpm_to_hp(rpm) for rpm in self.fit_rpms))







# Variables, current attributes of the car
ALT = 0 # assumes starting at 0 alt
ANG = 0.0 # always starting strait

car = WRX(ALT, ANG)
def simulate(track, sight, lap):
  #print "Peak Torque", car.peak_trq()
  total_time = 0.0 #s
  stalls = 0
  slips = 0
  for i in range(len(track)):
    try:
      action = lap[i]
      section = [track[i]]
      # current values 
      c_rpm = car.RPM
      c_s = car.MPS
      c_g = car.CUR_GEAR
      print c_s, c_rpm, c_g

      if car.slip(section, c_s):
        slips += 1
      if c_rpm < car.idle_rpm:
        stalls += 1

      acc = car.acceleration(car.RPM, c_s, c_g)
      time = car.time_between(acc / 2, c_s, -(step))
      total_time += float(time)

      # new values
      if action == "up":
        n_g = min(len(car.gears), c_g + 1)
      elif action == "down":
        n_g = max(1, c_g - 1)
      else:
        n_g = c_g
      n_s = car.next_speed(time, acc, c_s)
      n_rpm = car.getRPM(n_s, n_g)
      if n_rpm > car.redline_rpm:
        car.setVals(car.getMPS(car.redline_rpm, n_g), car.redline_rpm, n_g)
        continue
      car.setVals(n_s, n_rpm, n_g)
    except IOError:
      pass # I know...I know

  return total_time, slips, stalls



# def simulate(track, sight):
#   #print "Peak Torque", car.peak_trq()
#   total_time = 0.0 #s
#   slips = 0
#   for i in range(len(track)):
#     try:
#       #print car.CUR_GEAR, car.MPS, car.RPM
#       visible = track[i:i+sight-1]
#       # current values 
#       c_rpm = car.RPM
#       c_s = car.MPS
      
#       print c_s, car.CUR_GEAR#, car.slip_speed(visible) 
#       if car.slip(visible, c_s):
#         slips += 1
#       if c_s >= car.slip_speed(visible):
#         #need to brake
#         b_acc = car.braking_dec
#         b_time = car.time_between(b_acc / 2, c_s, -(step))
        
#         b_s = car.next_speed(b_time, b_acc, c_s)
#         b_rpm = car.getRPM(b_s, car.CUR_GEAR)
#         b_g = car.CUR_GEAR
#         if car.wheel_torque(b_rpm, b_g) < car.peak_trq(b_g):
#           print "Shift Down"
#           b_g = max(1, b_g - 1) # at least 1st gear
#         car.setVals(b_s, b_rpm, b_g)
#         total_time += float(b_time)
#         print "Braking", b_s, car.slip_speed(visible)#, car.slip(visible, c_s)
#         continue

      
#       acc = car.acceleration(car.RPM, c_s, car.CUR_GEAR)# * perc_acc(visible)
#       time = car.time_between(acc / 2, c_s, -(step))
#       total_time += float(time)

#       if car.rpm_to_hp(c_rpm) > car.peak_hp():
#         #shift up
#         if len(car.gears) > car.CUR_GEAR:
#           print "Shift UP"#, car.rpm_to_hp(c_rpm)
#           car.setVals(c_s, car.getRPM(c_s, car.CUR_GEAR + 1), car.CUR_GEAR + 1)
#           continue
#         else:
#           # already highest gear
#           continue
      

      
#       # new calculated values
#       n_s = car.next_speed(time, acc, c_s)
#       n_rpm = car.getRPM(n_s, car.CUR_GEAR)
#       #print car.wheel_torque(n_rpm, car.CUR_GEAR) < car.peak_trq(car.CUR_GEAR), c_s >= n_s
#       if (car.wheel_torque(n_rpm, car.CUR_GEAR) < car.peak_trq(car.CUR_GEAR)) and (c_s >= n_s):
#         #shift down
#         if car.CUR_GEAR > 1:
#           print "Shift DOWN"#, car.wheel_torque(n_rpm)
#           car.setVals(c_s, car.getRPM(c_s, car.CUR_GEAR - 1), car.CUR_GEAR - 1)
#           continue

      

#       car.setVals(n_s, n_rpm, car.CUR_GEAR)
#     except IOError:
#       pass # I know...I know

#   return total_time, slips
  






  # Basic Shifting functions
  # def shift_up(self):
  #   if len(self.gears) > self.CUR_GEAR:
  #     #print self.getRPM(self.MPS, self.CUR_GEAR)
  #     self.setVals(self.MPS, self.getRPM(self.MPS, self.CUR_GEAR + 1), self.CUR_GEAR + 1)
  #     print self.getRPM(self.MPS, self.CUR_GEAR)
  #     print self.CUR_GEAR 
  #     return True
  #   else:
  #     return False

  # def shift_down(self):
  #   if self.CUR_GEAR > 1:
  #     #print self.getRPM(self.MPS, self.CUR_GEAR)
  #     self.setVals(self.MPS, self.getRPM(self.MPS, self.CUR_GEAR - 1), self.CUR_GEAR - 1)
  #     #print self.getRPM(self.MPS, self.CUR_GEAR)
  #     print self.CUR_GEAR 
  #     return True
  #   else:
  #     return False





# Car Physics




# # def getMPS(RPM = RPM, CUR_GEAR = self.CUR_GEAR):
# #   #global gears, final_drive, tire_diameter, CUR_GEAR, RPM
# #   return (RPM*tire_diameter)/(gears[CUR_GEAR]*final_drive*336)

# def getRPM(MPS = self.MPS, CUR_GEAR = self.CUR_GEAR):
#   #global final_drive, tire_diameter, CUR_GEAR, MPS
#   return ((MPS/self.tire_radius) * self.gears[CUR_GEAR - 1] * self.final_drive * 60/(2 * math.pi)) 
# # Useful Utilities
# # 
# def rpm_to_trq(rpm):
#   return fit_trqs[(np.abs(fit_rpms-rpm)).argmin()]

# def rpm_to_hp(rpm):
#   return rpm_to_trq(rpm) * rpm / 5252

# def wheel_torque(rpm = self.RPM, CUR_GEAR = self.CUR_GEAR):
#   return (rpm_to_trq(rpm) * self.gears[CUR_GEAR - 1] * self.final_drive * self.tran_efficiency) / self.tire_diameter

# def drag(mps = self.MPS):
#   return (0.5 * self.drag_coef * self.front_area * air_dens * (mps * mps)) + (self.rolling_resistance * mps)

# def acceleration(RPM = self.RPM, MPS = self.MPS, CUR_GEAR = self.CUR_GEAR):
#   return (wheel_torque(RPM, CUR_GEAR) - drag(MPS)) / self.weight
# # print wheel_torque(idle_rpm, 2) 
# # print acceleration(idle_rpm, 0, 2)

# def slip(steps, MPS = MPS):
#   angle = 90.0 * abs(ang_delta(steps))
#   radius = length / (math.sin(math.radians(angle)))
#   lat_force = (weight * (MPS * MPS)) / radius
#   #print radius, lat_force, weight
#   return lat_force >= weight

# # print slip([(0, 0.99)], 1)
# # print slip([(0, 0.99)], 2)
# # print slip([(0, 0.99)], 20)

# dp = "%.2f"
# def next_speed(steps, RPM = RPM, MPS = self.MPS, CUR_GEAR = CUR_GEAR):
#   acc = acceleration(RPM, MPS, CUR_GEAR) * perc_acc(steps)
#   a = acc / 2
#   b = MPS
#   c = -(step)
#   discRoot = math.sqrt((b * b) - 4 * a * c) # first pass
#   root1 = (-b + discRoot) / (2 * a) # solving positive
#   #root2 = (-b - discRoot) / (2 * a) # solving negative
#   pos = dp % root1
#   #neg = dp % root2
#   time = pos
#   return MPS + acc * float(time)
# # print(getRPM(30, 3))
# # print next_speed([(0, 0)], getRPM(30, 3), 30, 3)


# # Basic Shifting functions
# def shift_up():
#   global CUR_GEAR, RPM
#   if len(self.gears) > CUR_GEAR:
#     CUR_GEAR += 1
#     RPM = getRPM() 
#     return True
#   else:
#     return False

# def shift_down():
#   global CUR_GEAR, RPM
#   if CUR_GEAR > 1:
#     CUR_GEAR -= 1
#     RPM = getRPM()
#     return True
#   else:
#     return False



