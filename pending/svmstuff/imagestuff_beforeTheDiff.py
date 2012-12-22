# Image stuff
# What I want to do in this file:
# - find a way to extract features from an image, in the form of vectors
# - train an SVM on those features
# - use that trained SVM to classify other images.

from opencv.cv import *
from opencv.highgui import *
import cv

wndname = "Classification Test"

# Chunk the image using a grid this high and long
chunkGridSize = 7


# TODO: populate this
imglist = ["images/yellow/yellow1.jpg"]

# This will be the matrix that holds every feature vector
#TODO: convert to vector/matrix form?
features = []

for imgname in imglist:
    img = cvLoadImage(imgname)
    
    size = cvGetSize(img);
    depth = img.depth;
    ch1 = cvCreateImage(size, depth, 1)
    ch2 = cvCreateImage(size, depth, 1)
    ch3 = cvCreateImage(size, depth, 1)

    # Convert to LUV (Do I want to do this?)
    cvCvtColor(img, img, CV_RGB2Luv)

    # Split into channels
    cvSplit(img,ch1,ch2,ch3,0)

    # This will hold all of the features (this should be 294 long at the end)
    # TODO: convert this to vector/matrix form?
    imgvector = []
    
    for channel in [ch1, ch2, ch3]:

        # Get the block height and width
        blockHeight = channel.height / chunkGridSize
        blockWidth = channel.width / chunkGridSize

        # Because of integer truncation, and the loops below, it will be
        # nice to have these numbers be exact
        newHeight = blockHeight * chunkGridSize
        newWidth = blockWidth * chunkGridSize
        
        for i in range(0, blockHeight, newHeight):
            for j in range(0, blockWidth, newWidth):

                rect = cvRect(i, j, blockWidth, blockHeight)
                cv.SetImageROI(channel, rect)

                # TODO: make sure AvgSdv only works on the ROI
                (mean, stdDev) = cvAvgSdv(c)
                variance = stdDev * stdDev
                imgvector += [mean, variance]
                
                # Just in case.
                cvResetImageRoi(channel)

    features.append(imgvector)

print features

# Basically, each vector needs to be a column. Create it as a row and transpose the matrix. Easiest, probably. 
# somehow convert features to a matrix, and take the transform, so it looks like:
#[img1_band1_mean_00, img2...
#[img1_band1_variance_00, img2...

#[img1_band1_mean_01, img2...
#[img1_band1_variance_01, img2...    

#[img1_band1_mean_02, img2...
#[img1_band1_variance_02, img2...

#[Repeat for band2, img2...
#[And band3, img2...


# What I need to do:
# Get image data in the right format:
# Split up each image into some chunks (49 blocks?)
# get features from each chunk
# Let's start with mean and variance of each band of LUV image. (Why??)
# This means that each vector will be of length: 49 chunks * 2 calcs * 3 bands = 294




#cvShowImage(wndname, img)
#cvWaitKey(0)
