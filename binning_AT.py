"""
Python backend for Machine Learning project 1
Binning into days, weeks, and time of day

@author: Adam Terwilliger
"""

import sys
import os
import numpy as np


np.set_printoptions(threshold='nan')

file = "downloads.txt"

fileLines = []

with open(file) as fh:
	for i, line in enumerate(fh):
		line = line.strip()
		lineParts = line.split(',')
		downloads = lineParts[1]
		if downloads != "nan":
			downloads = int(downloads)
		else:
			downloads = 0
		fileLines.append(downloads)
		
#print fileLines

downloadArray = np.empty([len(fileLines),2]).astype(int)

def binning(mod, mod2, mod3):
	for hour, downloads in enumerate(fileLines):
		downloadArray[hour] = int(hour % mod / mod2 % mod3), downloads
		#print downloadArray[hour]

	binCountArray = np.bincount(downloadArray[:,0])
	binnedArray = np.bincount(downloadArray[:,0],weights=downloadArray[:,1])
	
	#print binCountArray
	#print binnedArray
	
	return np.array(binnedArray / binCountArray)

timeOfDay = binning(24, 1, len(fileLines))
dayOfMonth = binning(len(fileLines), 24, len(fileLines))
dayOfWeek = binning(len(fileLines), 24, 7)

#for i in range(len(timeOfDay)):
#	print i, timeOfDay[i]

def printValues(name, array):
	dataSet = "var " + name + " = [\n"
        for i in range(len(array)):
        	dataSet += "[{}, {}],\n".format(str(i+1), str(array[i]))
	# trim off the last comma
	dataSet = dataSet[:-2]
	dataSet += "\n];"
	with open(name+"Data.js", "w") as fh:
		fh.write(dataSet)

def printValues2():
	dataSet = "var dayOfWeek = [\n"
        for i in range(len(dayOfWeek)):
        	dataSet += "[{}, {}],\n".format(str(i+1), str(dayOfWeek[i]))
	# trim off the last comma
	dataSet = dataSet[:-2]
	dataSet += "\n];"
	with open("dayOfWeek.js", "w") as fh:
		fh.write(dataSet)

def printValues3():
	dataSet = "var dayOfMonth = [\n"
        for i in range(len(dayOfMonth)):
        	dataSet += "[{}, {}],\n".format(str(i+1), str(dayOfMonth[i]))
	# trim off the last comma
	dataSet = dataSet[:-2]
	dataSet += "\n];"
	with open("dayOfMonth.js", "w") as fh:
		fh.write(dataSet)

printValues('timeOfDay',timeOfDay)
printValues('dayOfWeek',dayOfWeek)
printValues('dayOfMonth',dayOfMonth)
