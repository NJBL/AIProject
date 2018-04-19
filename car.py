import sys
import csv
import json
import requests
from utils import *
from reward import *


# API_key = "AIzaSyByKr1JYD0yYLdK7BG0aKYci2uoegcaPGk" #yes, I know...I know
# response = requests.get("https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=" + API_key)
# print json.loads(response.text)['results']

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
  lap = ["up"] * len(track)
  print simulate(track, sight, lap)
  print "Time, Slips, Stalls"
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