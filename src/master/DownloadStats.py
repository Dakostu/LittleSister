# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# DownloadStats.py is a Python module that calculates the amount of downloaded KB/s
# for the master.

import time
from PictureSettings import * 

# totalDLSize is a module-local variable that gets cleared every second 
# (calculated using Unix time).
# Upon being cleared, the last value gets persisted to a file in the current running directory.
totalDLSize = 0
lastAvrgDLCalculationDate = int(time.time())

def AddToDLStatistic(amount):
	global totalDLSize
	totalDLSize = totalDLSize + amount
	PersistDLSizeAmount()

def PersistDLSizeAmount():
	global totalDLSize
	global lastAvrgDLCalculationDate
	currentTime = int(time.time())
	
	# reset value every Unix second
	if (currentTime == lastAvrgDLCalculationDate):
		return
	lastAvrgDLCalculationDate = currentTime
	DLSizeFile = open(DLSIZEFILELOC, "w")
	DLSizeFile.write('% .2f' % (totalDLSize/1000.0))
	DLSizeFile.close()
	totalDLSize = 0

def ResetDLStatistic():
	DLSizeFile = open(DLSIZEFILELOC, "w")
	DLSizeFile.write('0')
	DLSizeFile.close()

