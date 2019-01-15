# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# LaunchMaster.py launches the LittleSister video surveillance routine 
# for the slave.

from picamera import PiCamera
from PictureSettings import IMGHEIGHT, IMGWIDTH, FRAMERATE
import PictureSend

# set up camera
camera = PiCamera()
camera.resolution = (IMGHEIGHT, IMGWIDTH)
camera.framerate = FRAMERATE

while True:
	PictureSend.Stream(camera)
