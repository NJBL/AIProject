import sys
import csv
from utils import *

# System Arguments
# reward, path to track file
if len(sys.argv) != 3:
  print("usage:\n  CHOOSE (required):\n    either -f average fuel economy\n    or     -s average speed\n  AND      path to track file (required)")
  sys.exit()
else:
  reward = 'fuel' if ((sys.argv[1] == '-f') or (sys.argv[1] == '-F')) else 'speed'
  print(reward)
  try:
    with open(sys.argv[2]) as csvfile:
      track = csv.reader(csvfile)
      for row in track:
        print(row)
    
  except IOError:
      print("COULD NOT FIND FILE")
      print("usage:\n  CHOOSE (required):\n    either -f average fuel economy\n    or     -s average speed\n  AND      path to track file (required)")
      sys.exit() 

  #print(getRPM())
  #print(getMPH())
sys.exit("End")