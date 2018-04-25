from utils import *
from reward import *
from MDP import *
from simulation import *
from state_est import *

BOGUS = 9999

def reward(spd, rpm, pk_rpm, gr, hp, slip_s, err):
  reward = 0
  if err:
    return -99999999999999
  reward += spd
  reward += hp
  reward += (rpm - pk_rpm)/1000
  if not slip_s == BOGUS: # no angle strait track
    reward -= 10 * (spd - slip_s)
  return gr * reward 


def generate_lap(track, prev, record, car, sight):
  new_lap = prev
  update = False
  kill = False
  for i,step in enumerate(record):
    visible = track[i:i+sight-1]
    if prev[i] == "brake":
      continue
    c_rpm, c_sp, c_gr, slip, stall = step
    err = slip or stall
    # if err:
    #   print slip, stall
    c_hp = car.rpm_to_hp(c_rpm)
    c_trq = car.wheel_torque(c_rpm, c_gr)
    pk_trq = car.peak_trq(c_gr)
    slip_s = car.slip_speed(visible)
    if not slip_s:
      slip_s = BOGUS # no angle, just making it irrelevant
    c_stall = c_rpm <= car.idle_rpm
    c_slip = c_sp > slip_s
    c_rwd = reward(c_sp, c_rpm, car.pk_rpm, c_gr, c_hp, slip_s, (c_stall or c_slip))
    # Compare actions

    # Brake
    b_g, b_s, b_rpm, b_hp = est_braking(c_sp, c_gr, visible)
    b_stall = b_rpm <= car.idle_rpm
    b_slip = b_s > slip_s
    b_rwd = reward(b_s, b_rpm, car.pk_rpm, b_g, b_hp, slip_s, (b_stall or b_slip))
    
    # Shift up
    u_g, u_s, u_rpm, u_hp = est_shift_up(c_sp, c_gr)
    u_stall = u_rpm <= car.idle_rpm
    u_slip = u_s > slip_s
    u_rwd = reward(u_s, u_rpm, car.pk_rpm, u_g, u_hp, slip_s, (u_stall or u_slip))

    # Shfit down
    d_g, d_s, d_rpm, d_hp = est_shift_down(c_sp, c_gr)
    d_stall = d_rpm <= car.idle_rpm
    d_slip = d_s > slip_s
    d_rwd = reward(d_s, d_rpm, car.pk_rpm, d_g, d_hp, slip_s, (d_stall or d_slip))
    #print c_rwd, u_rwd, d_rwd, b_rwd

    


    if u_rwd > c_rwd or d_rwd > c_rwd or b_rwd > c_rwd:
      if d_rwd > u_rwd and d_rwd > b_rwd:
        if not prev[i] == "down":
          prev[i] = "down"
          update = True
          print "down"
        else:
          continue
      elif u_rwd >= d_rwd and u_rwd >= b_rwd:
        if not prev[i] == "up":
          prev[i] = "up"
          update = True
          print "up"
        else:
          continue
      elif b_rwd >= u_rwd and b_rwd >= d_rwd:
        if not prev[i] == "brake":
          prev[i] = "brake"
          update = True
          print "brake"
        else:
          continue
      break
  if not update:
    # Enforce extra braking if there are lingering slips
    for i,step in enumerate(record):
      c_rpm, c_sp, c_gr, slip, stall = step
      if slip:
        try:
          for j in range(i, 0, -1):
            if not (prev[j] == "brake" or prev[j] == "down"):
              prev[j] = "brake"
              update = True
              break
        except IndexError:
          kill = True
  if not update:
    kill = True
  
  return prev, kill
  
  
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