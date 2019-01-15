# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# PictureCompare.py contains all functions regarding to image processing.

from PIL import Image, ImageChops
from PictureSettings import *
import os
import PictureSend
import StringIO
import io
import numpy

# pixel marking algorithm
def IsPixelDifferent(p1, p2):
	return abs(p1[r] - p2[r]) > PIXELDIFF or abs(p1[g] - p2[g]) > PIXELDIFF or abs(p1[b] - p1[b]) > PIXELDIFF

def CompareIAndPFrames(IFrameStream, PFrameStream):
	IFrameMatrix = ImageStreamToMatrix(IFrameStream)
	PFrameMatrix = ImageStreamToMatrix(PFrameStream)

	x = 0
	y = 0
	while x < IMGWIDTH:
		while y < IMGHEIGHT:
			IFramePixel = IFrameMatrix.getpixel((y,x))
			PFramePixel = PFrameMatrix.getpixel((y,x))
			if IsPixelDifferent(IFramePixel, PFramePixel):
				SendChunk(PFrameMatrix,x,y)
			y = y + GRIDFACTOR
		x = x + GRIDFACTOR
		y = 0


def SendChunk(PFrameMatrix,x,y):
	data = ('%04d' % x) + ('%04d' % y)
	cropped = PFrameMatrix.crop((x,y,x+GRIDFACTOR,y+GRIDFACTOR))
	cropBuffer = StringIO.StringIO()
	cropped.save(cropBuffer,'jpeg')
	data += cropBuffer.getvalue()

	PictureSend.PrepareUDPPackage(0, data)


def ImageStreamToMatrix (stream):
	return Image.open(stream)
