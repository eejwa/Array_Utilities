#!/usr/bin/env python

### code to pick a time window of a bunch of traces:
import obspy
import numpy as np
import matplotlib.pyplot as plt
### import code to add information to a results file.
import os

import argparse

parser = argparse.ArgumentParser(description='Preprocessing script for data retrieved from obspy DMT')

parser.add_argument("-f","--file_wildcard", help="Enter the file to be normalised (e.g. *BHR*)", type=str, required=True, action="store", default = "*BHR*")

parser.add_argument("-p","--phase", help="Enter the you want to be targetted (e.g. SKS)", type=str, required=True, action="store", default = "SKS")


args = parser.parse_args()

file_names = args.file_wildcard
phase = args.phase

#---------- Load the data ----------#
# read in all the normalised sac files in the directory
stream = obspy.read(file_names)
stream.normalize()
## define a window
window = []

labels = ["kt1", "kt2", "kt3", "kt4", "kt5", "kt6", "kt7", "kt8", "kt9"]

## list for average of SKS times
Target_phase_times = []

def get_window(event):
	ix = event.xdata
	print("ix = %f" %ix)
	window.append(ix)
	print(len(window))
	if len(window) == 2:
		fig.canvas.mpl_disconnect(cid)
		plt.close()

	return window


#~~~~~~ I've changed the code so it can now read in sac files without this coordinates nonesense ~~~~~~#

# make list of list of all the phase predicted times.
time_header_times = [[] for i in range(9)]

Target_time_header = None
# Get all predicted SKS times
for x,trace in enumerate(stream):
#### find out which time header holds the predicted time
### for the phase you want.
	ep_dist = trace.stats.sac.gcarc

### not all the traces will have the same phases arriving due to epicentral
### distance changes
	phases_tn = []
	phases = []
	for K in labels:
		try:
			phase_label = getattr(trace.stats.sac, K)
			phases_tn.append([str(phase_label), str(K.replace("k",""))])
			phases.append(str(phase_label))
		except:
			pass
			## check to see if it is the same as the phase:
		if phase_label == phase:
			print(phase_label)
			print(phase)
			if Target_time_header == None:
				Target_time_header = K.replace("k","")

			print(Target_time_header)
	Target_phase_times.append(getattr(trace.stats.sac, "t1") - trace.stats.sac.b)
	print(phases_tn)
	for c in range(len(phases_tn)):
		timeheader=phases_tn[c][1]
		time_header_times[c].append([float(getattr(trace.stats.sac,timeheader) - trace.stats.sac.b), float(ep_dist), phases_tn[c][0]])

avg_target_time = np.mean(Target_phase_times)
min_target_time = int(np.min(Target_phase_times))
max_target_time = int(np.max(Target_phase_times))


## Window for plotting record section
win_st = float(min_target_time - 100)
win_end = float(max_target_time + 150)

fig = plt.figure()
ax = fig.add_subplot(111)

distances = []
geometry = []
for i,tr in enumerate(stream):

	dist = tr.stats.sac.gcarc

	stla = tr.stats.sac.stla
	stlo = tr.stats.sac.stlo
	stel = tr.stats.sac.stel
	geometry.append([stlo, stla, stel])

	window_length = win_end - win_st

	## get the number of data points in the window
	pts_in_wind = window_length*tr.stats.sampling_rate

	# define start and end data point
	start_sample = int((win_st) * tr.stats.sampling_rate + .5)

	tr_plot = tr.copy()
	## get the data points for the window only
	dat_plot = tr_plot.data[int(start_sample):(int(start_sample) + int(pts_in_wind))]
	## Add the epicentral distance value to the data to make the record section.
	#print(dist)
	dat_plot +=dist
	#print(dat_plot)
	print(tr.stats.sac.t1)
	time = np.arange(win_st, win_end, 1/tr.stats.sampling_rate)
	distances.append(dist)
	ax.plot(time,dat_plot,color='black')

plt.xlim(win_st,win_end)

avg_dist = np.mean(np.array(distances))

geometry = np.array(geometry)

### Now I'll plot the predictions for SKS etc.

## Make into arrays to make life easier
t1_arr = np.array(time_header_times[0])
t2_arr = np.array(time_header_times[1])
t3_arr = np.array(time_header_times[2])
t4_arr = np.array(time_header_times[3])
t5_arr = np.array(time_header_times[4])
t6_arr = np.array(time_header_times[5])
t7_arr = np.array(time_header_times[6])
t8_arr = np.array(time_header_times[7])
t9_arr = np.array(time_header_times[8])

## Try and except loops for plotting the predicted arrivals
try:
	ax.plot(t1_arr[:,0], t1_arr[:,1], color='C0', label=t1_arr[0,2])
except:
	print("nuts, NO ARRIVAL ")

try:
	ax.plot(t2_arr[:,0], t2_arr[:,1], color='C1', label=t2_arr[0,2])
except:
	print("G-Bus, NO ARRIVAL ")

try:
	ax.plot(t3_arr[:,0], t3_arr[:,1], color='C2', label=t3_arr[0,2])
except:
	print("this sucks, NO ARRIVAL ")

try:
	ax.plot(t4_arr[:,0], t4_arr[:,1], color='C3', label=t4_arr[0,2])
except:
	print("what the duck, NO ARRIVAL ")

try:
	ax.plot(t5_arr[:,0], t5_arr[:,1], color='C4', label=t5_arr[0,2])
except:
	print("god damn it, NO ARRIVAL ")

try:
	ax.plot(t6_arr[:,0], t6_arr[:,1], color='C5', label=t6_arr[0,2])
except:
	print("balls, NO ARRIVAL ")

try:
	ax.plot(t7_arr[:,0], t7_arr[:,1], color='C6', label=t7_arr[0,2])
except:
	print("sigh, NO ARRIVAL ")

try:
	ax.plot(t8_arr[:,0], t8_arr[:,1], color='C7', label=t8_arr[0,2])
except:
	print(":( NO ARRIVAL ")

try:
	ax.plot(t9_arr[:,0], t9_arr[:,1], color='C8', label=t9_arr[0,2])
except:
	print("... NO ARRIVAL ")


deg = u"\u00b0"

#plt.title('Record Section Picking Window | Depth: %s Mag: %s' %(stream[0].stats.sac.evdp, stream[0].stats.sac.mag))
plt.ylabel('Epicentral Distance (%s)' %deg)
plt.xlabel('Time (s)')
plt.legend(loc='best')

cid = fig.canvas.mpl_connect('button_press_event', get_window)

print("BEFORE YOU PICK!!")
print("The first click of your mouse will the the start of the window")
print("The second click will the the end of the window")
plt.show()
## Luckily, the traces have already had the instrument response removed - Well Done Ward ##


stime = stream[0].stats.starttime + window[0]
etime = stream[0].stats.starttime + window[1]
times_t1 = t1_arr[:,0].astype(float)
#print(times_t1)
print(window[0], window[1])
print(window[0] + stream[0].stats.sac.b)
print(window[1] + stream[0].stats.sac.b)

## both of these values are relative to the start of the trace
## So I dont need to add the beginning value.

rel_window_start_bot = window[0] - times_t1.min()
rel_window_start_top = window[0] - times_t1.max()
rel_window_end_bot = window[1] - times_t1.min()
rel_window_end_top = window[1] - times_t1.max()

print(rel_window_start_bot,rel_window_start_top)
print(rel_window_end_bot,rel_window_end_top)


with open("window_start_end.txt", 'w') as window_file:
	window_file.write("window_start_rel_t1 | window_end_rel_t1 | abs_pick \n")
	window_file.write("%s | %s | %s \n" %(str(rel_window_start_bot),str(rel_window_start_top), str(window[0])))
	window_file.write("%s | %s | %s \n" %(str(rel_window_end_bot),str(rel_window_end_top), str(window[1])))
