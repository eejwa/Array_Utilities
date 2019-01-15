#!/usr/bin/env python

### code to replace the real data with a ricker wave or a sine wave
### at a predicted arrival time based on a given phase

import obspy
import numpy as np
import argparse
from scipy import signal

parser = argparse.ArgumentParser(description='Preprocessing script for data retrieved from obspy DMT')

parser.add_argument("-file","--file_wildcard", help="Enter the file to be normalised (e.g. *BHR*)", type=str, required=True, action="store", default = "*NORM*")
parser.add_argument("-freq","--frequency", help="Enter the frequency for the wavelet", type=float, required=True, action="store", default = "0.4")

parser.add_argument("-p","--phase", help="Enter the you want to be targetted (e.g. SKS)", type=str, required=True, action="store", default = "SKS")

parser.add_argument("-t","--wavelet_type", help="Enter the type of wave you want sine(s) or ricker(r).", type=str, required=True, action="store", default = "s")

parser.add_argument("-v", "--verbose", help="Increase verbosity of output, just --verbose is enough to turn on.",action="store_true")

args = parser.parse_args()

file_names = args.file_wildcard
phase = args.phase
wave_type = args.wavelet_type
labels = ["kt1", "kt2", "kt3", "kt4", "kt5", "kt6", "kt7", "kt8", "kt9"]

stream = obspy.read(file_names)

sampling_interval = stream[0].stats.delta
sampling_rate = stream[0].stats.sampling_rate
freq=args.frequency
amp=5

time = len(stream[0].data)*sampling_interval

for i,tr in enumerate(stream):
	data = tr.data
	new_data = np.full_like(data,0)
	print(tr.stats.station)
	##get the travel time prediction for the requested phase
	for K in labels:
		try:
			phase_label = getattr(tr.stats.sac, K)
		except:
			pass
			## check to see if it is the same as the phase:
		if phase_label == phase:
			print(phase_label)
			print(phase)
			Target_time_header = K.replace("k","")
			pred_time = getattr(tr.stats.sac, Target_time_header)

	## make a synthetic wave
	if wave_type == "s":
		t = np.arange(0,(1/freq)+sampling_interval,sampling_interval)
		wavelet = np.sin(2*np.pi*freq*t)*amp
	elif wave_type == "r":
		t = np.arange(-1*((1/freq)+sampling_interval),(1/freq)+sampling_interval,sampling_interval)
#		wavelet = signal.ricker(1000, 1)*amp
		wavelet = (1.0 - 2.0*(np.pi**2)*(freq**2)*(t**2)) * np.exp(-(np.pi**2)*(freq**2)*(t**2))*amp
		## add the synthetic wave at the predicted time
	synth_wave = np.insert(new_data,(pred_time*sampling_rate) - ((1/freq))*sampling_rate,wavelet)

	tr.data = synth_wave

	tr.write("%s.%s.SAC" %(tr.stats.station,tr.stats.channel),format="SAC")
