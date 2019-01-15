# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# PictureRecieve.py is the Python module that parses the incoming UDP package 
# from a slave and modifies the according webcam picture.

from PictureSettings import *
from DownloadStats import *
from PIL import Image
import io
import imghdr
import os
import sys

def ProcessInputData(data):
        AddToDLStatistic(len(data))

        SLAVE_IP_BYTE = data[:3]
        isEntirePicture = int(data[3])
        pictureData = data[4:]

        # either save entire pic or insert cropped picture, according to isEntirePicture byte
        if (isEntirePicture):
                SavePicture(SLAVE_IP_BYTE, pictureData)
        else:
                DrawNewChunks(SLAVE_IP_BYTE, pictureData)

def DrawNewChunks(ByteIP, data):    
        # refer to PictureSend.py in the slave source code folder
        # for UDP package structure
        IMGWIDTH = int(data[:4])
        IMGHEIGHT = int(data[4:8])
        GRIDFACTOR = int(data[8:12])
        chunkX = int(data[12:16])
        chunkY = int(data[16:20])
        pictureData = data[20:]
        picturePath = (FILELOC + ByteIP + FILETYPE)

        # check validity of recieved picture data
        if imghdr.what("",pictureData) is not 'jpeg':
            return

        # if picture on master is corrupt: create new picture
        if os.path.exists(picturePath) and imghdr.what(picturePath) == 'jpeg':
                savedImage = Image.open(picturePath)
        else:
                savedImage = Image.new('RGB',((IMGHEIGHT, IMGWIDTH)), color='black').save(picturePath)

        tempCroppedPic = Image.open(io.BytesIO(pictureData))
        savedImage.paste(tempCroppedPic,(chunkX,chunkY, chunkX+GRIDFACTOR, chunkY+GRIDFACTOR))
        savedImage.save(picturePath)

def SavePicture(ByteIP, picData):
	if imghdr.what("",picData) is not 'jpeg':
		return

    file = open (FILELOC + ByteIP + FILETYPE, "w")
    file.write(picData)
    file.close()

