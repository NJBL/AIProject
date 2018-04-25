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

  
  sight = 10
  

  # init
  min_consensus = 10
  consensus = []
  lap = ["acc"] * len(track)
  time, record = simulate(track, lap)
  best = 0
  all_lap_times = []
  while len(consensus) < min_consensus:
    new_lap, kill = generate_lap(track, lap, record, car, sight)
    time, record = simulate(track, new_lap)
    all_lap_times.append(time)
    # The loop is meant to end when the simulation has plateaued, and no improvement is expected
    # The list 'consensus' keeps track of the best time, and keeps duplicate results until the minimum consensus is met
    if time < 0:
      # DNF
      time = -1
      continue
    elif len(consensus) == 0:
      #empty
      consensus.append(time)
      best = new_lap
    elif time < consensus[0]:
      # new best time
      consensus = [time]
      best = new_lap
    elif time == consensus[0]:
      # duplicate time, consistent
      consensus.append(time) 
    
    lap = new_lap
    if kill:
      break


  print "Best time:\n", consensus, "\nBest lap:\n", best, "\nAll lap times:\n", all_lap_times

sys.exit("End")