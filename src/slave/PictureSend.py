# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# PictureSend.py contains all functions regarding 
# to sending picture information in UDP packets.

from socket import *
from PictureSettings import * 
import io
import picamera
import PictureCompare
import StringIO

def Stream(camera):
	IFrame = ""
	numberOfShotFrames = 0
	stream = io.BytesIO()
    
    # a slave takes the frames in the following order:
    # [I] <- [P] <- [P] <- [P] <- [I]
    # (amount of P frames can be set in PictureSettings.py)
    # after taking an I frame, the slave sends the entire picture
    # after taking a P frame, the slave sends differences inbetween frames
	for capture in camera.capture_continuous(stream, FILETYPE,use_video_port=True):		
		stream.seek(0)
		fileStream = stream.read()
		if NUMBER_PFRAMES == 0 or numberOfShotFrames == 0:
			IFrame = fileStream
			PrepareUDPPackage(1,IFrame)
		else:
			IFrameBytes = StringIO.StringIO(IFrame)
			PFrame = StringIO.StringIO(fileStream)
			PictureCompare.CompareIAndPFrames(IFrameBytes, PFrame)
			IFrame = fileStream

		stream.seek(0)
		stream.truncate()
		if NUMBER_PFRAMES != 0:
            numberOfShotFrames = (numberOfShotFrames + 1) % NUMBER_PFRAMES

def GetIPAddress():
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.connect(("8.8.8.8",80))
	return sock.getsockname()[0]

def PrepareUDPPackage(isEntireFile, data):
    # The UDP package structure is as follows
    #
    # If only the entire picture will be sent:
    # [last IP byte | 1 | entire pic byte stream]
    #
    # If a cropped part of the picture will be sent, the following 
    # wwww, hhhh: picture size
    # gggg: granularity of pixel area grids
    # xxxx, yyyy: coordinates of first pixel in pixel area (in PictureCompare.CompareIAndPFrames)
    # [last IP byte | 0 | wwww | hhhh | gggg | xxxx | yyyy | Cropped picture byte stream]
    
	IP_BYTE = ('%03d' % int(GetIPAddress().split(".")[3]))
	DATA_ARRAY = IP_BYTE + str(isEntireFile) 
        if isEntireFile == 0:
                DATA_ARRAY += ('%04d' % IMGWIDTH) + ('%04d' % IMGHEIGHT) + ('%04d' % GRIDFACTOR)
        DATA_ARRAY += data
	SendUDPPackage(DATA_ARRAY)

def SendUDPPackage(DATA_ARRAY):
	sock = socket(AF_INET, SOCK_DGRAM)
	host = gethostname()
	sock.sendto(DATA_ARRAY, (MASTER_IP, PORT))
	sock.close()

