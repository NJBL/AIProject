import sys
import csv
import json
import requests
from utils import *
from reward import *
from MDP import *
from simulation import *


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
      #print("usage:\n  CHOOSE (required):\n    either -f average fuel economy\n    or     -s average speed\n  AND      path to track file (required)")
      sys.exit() 
  #sight = 10
  

  # init
  min_consensus = 10
  consensus = []
  lap = ["acc"] * len(track)
  time, record = simulate(track, lap)

  while len(consensus) < min_consensus:
    new_lap = generate_lap(lap, record, car)
    time, record = simulate(track, new_lap)
    
    # The loop is meant to end when the simulation has plateaued, and no improvement is expected
    # The list 'consensus' keeps track of the best time, and keeps duplicate results until the minimum consensus is met
    if time < 0:
      # DNF
      time = -1
    elif not consensus:
      #empty
      consensus.append(time)
    elif time < consensus[0]:
      # new best time
      consensus = [time]
    elif time == consensus[0]:
      # duplicate time, good
      consensus.append(time) 
    elif time > consensus[0]:
      break
    
    lap = new_lap
    #print lap
    print time



  print consensus[0], lap
  #print "Time, Slips, Stalls"

sys.exit("End")