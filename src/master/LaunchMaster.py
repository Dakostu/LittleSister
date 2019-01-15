# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# LaunchMaster.py launches the LittleSister video surveillance routine 
# for the master.

from socket import *
from PictureSettings import *
from DownloadStats import *
import select
import sys
import PictureRecieve

# establish UDP socket
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((NETWORK, IN_PORT))

# because a video surveillance system is a real-time critical system,
# we are being lenient with exceptions
while True:
	try:
		while True:
			ready = select.select([sock],[],[],TIMEOUT)
			if ready[0]:
				data, addr = sock.recvfrom(CHUNKSIZE)
				PictureRecieve.ProcessInputData(data)
	except KeyboardInterrupt:
		print "Interrupted"
		sock.close()
		ResetDLStatistic()
		sys.exit()
	except Exception as e:
		print(e)
		pass

