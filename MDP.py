from utils import *
from reward import *
from MDP import *
from simulation import *



def reward(spd, rpm, pk_rpm, gr, hp, err):
  if err:
    return -9999
  return gr*(spd + hp + ((rpm - pk_rpm)/1000))


def generate_lap(prev, record, car):
  new_lap = prev
  for i,step in enumerate(record):
    c_rpm, c_sp, c_gr, slip, stall = step
    err = slip or stall
    c_hp = car.rpm_to_hp(c_rpm)
    c_trq = car.wheel_torque(c_rpm, c_gr)
    pk_trq = car.peak_trq(c_gr)
    #print c_sp, c_rpm, c_gr
    c_rwd = reward(c_sp, c_rpm, car.pk_rpm, c_gr, c_hp, err)
    
    # Compare actions
    # Shift up
    u_g, u_s, u_rpm, u_hp = car.est_shift_up(c_sp, c_gr)
    u_rwd = reward(u_s, u_rpm, car.pk_rpm, u_g, u_hp, (u_rpm <= car.idle_rpm))

    # Shfit down
    d_g, d_s, d_rpm, d_hp = car.est_shift_down(c_sp, c_gr)
    d_rwd = reward(d_s, d_rpm, car.pk_rpm, d_g, d_hp, (d_rpm <= car.idle_rpm))
    #print c_rwd, u_rwd, d_rwd
    if u_rwd > c_rwd or d_rwd > c_rwd:
      if d_rwd > u_rwd:
        if not prev[i] == "down":
          prev[i] = "down"
        else:
          continue
      else:
        if not prev[i] == "up":
          prev[i] = "up"
        else:
          continue
      break

    
  
  return prev
  
  
  # ASSISTED
  # n_lap = prev
  # for i, step in enumerate(prev):
  #   if i < (len(record) - 1):
  #     car = record[i]
  #     c_rpm = car.RPM
  #     c_s = car.MPS
  #     c_g = car.CUR_GEAR
      
  #     try :
  #       if car.rpm_to_hp(c_rpm) > car.peak_hp():
  #         # shift up
  #         print "SHIFT UP"
  #         n_lap[i] = "up"
        
  #       elif (car.wheel_torque(c_rpm, c_g) < car.peak_trq(c_g)) and (c_s >= record[i + 1].MPS):
  #         # shfit down
  #         print "SHIFT DOWN"
  #         n_lap[i] = "down" 
  #     except IndexError:
  #       break
  #   #else:
  #     # DNF
  #     # if record[-1][0] == "SLIP":
  #     #   # too fast
  #     #   # Need to brake earlier
  #     #   0
  #     # elif record[-1][0] == "STALL":
  #     #   # too slow for this gear, need to downshift
  #     #   0