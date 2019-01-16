# LITTLE SISTER
# Daniel Kostuj, 2019
# Refer to LICENSE file for license information.

# PictureSettings.py contains all settings for the slave.

# camera settings
IMGHEIGHT       = 240
IMGWIDTH        = (IMGHEIGHT/4)*3
FRAMERATE       = 24
FILETYPE        = "jpeg"

# difference calculation settings
GRIDFACTOR      = 30  # granularity of pixel area that will be sent as diffs
PIXELDIFF       = 20  # threshold value of pixel color difference calculation
r               = 0
g               = 1
b               = 2
NUMBER_PFRAMES  = 10  # set this value to 0 to shoot I frames only and disable difference calculation

# network settings
MASTER_IP       = "200.200.200.1"
PORT            = 8001
