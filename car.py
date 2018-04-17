import sys
import csv
from utils import *
from reward import *

# System Arguments
# reward, path to track file
if len(sys.argv) != 2:
  print("usage:\n        path to track file (required)")
  sys.exit()
# CHOOSE (required):\n    either -f average fuel economy\n    or     -s average speed\n  AND
else:
  #reward = 'fuel' if ((sys.argv[1] == '-f') or (sys.argv[1] == '-F')) else 'speed'
  track = []
  try:
    with open(sys.argv[1]) as csvfile:
      t = csv.reader(csvfile)
      for row in t:
        track.append(row)
  except IOError:
      print("COULD NOT FIND FILE")
      print("usage:\n  CHOOSE (required):\n    either -f average fuel economy\n    or     -s average speed\n  AND      path to track file (required)")
      sys.exit() 
  sight = 10
  print simulate(track, sight)
  #print car.MPS, car.RPM
  # speed = 0
  # rpm = idle_rpm
  # print speed, rpm
  # try:
  #   for i in range(len(track)):
  #     visible = track[i:i+sight-1]
  #     speed = next_speed(visible, rpm, speed)
  #     rpm = getRPM(speed)
  #     print speed, rpm
      
  # except IOError, e:
  #   print e
sys.exit("End")










# track = [
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0],
  #   [0.0,0.0]
  # ]