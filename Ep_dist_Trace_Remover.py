#!/usr/bin/env python

## Thsi will ask for an epicentral distance, then more/less
## from this information, it will move the traces which meet the criteria of the above

##E.g. dist 85, below would move all traces which have a distance of less than 85 to a new directory.

import obspy
import os
import shutil
from glob import *

import argparse

parser = argparse.ArgumentParser(description='Move unwanted distance SAC files to a separate directory.')

parser.add_argument("-d","--distance", help="Enter the epicentral distance in degrees.", type=str, nargs=1, required=True, action="store")

parser.add_argument("-c","--above_or_below", help="Move traces which are either above(a) or below(b) the distance.", type=str, nargs=1, required=True, action="store")

parser.add_argument("-v", "--verbose", help="Increase verbosity of output, just --verbose is enough to turn on.",action="store_true")

args = parser.parse_args()

distance = args.distance[0]
more_less = args.above_or_below[0]


move_dir = "Traces_Removed_by_Epdist"

if not os.path.exists(move_dir):
    os.makedirs(move_dir)

for sac_file in glob('*SAC'):
	st = obspy.read(sac_file)
	tr = st[0]
	dist=tr.stats.sac.gcarc
	
	if more_less == "a":
		if dist > float(distance):
			shutil.move(sac_file,move_dir)
	elif more_less == "b":
		if dist < float(distance):
			shutil.move(sac_file,move_dir)
	else:
		print("you messed up")




