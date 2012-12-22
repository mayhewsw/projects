# Image stuff
# What I want to do in this file:
# - find a way to extract features from an image, in the form of vectors
# - train an SVM on those features
# - use that trained SVM to classify other images.

#from opencv.cv import *
#from opencv.highgui import *
import cv
import numpy
import os, sys
from shogun.Features import *
from shogun.Classifier import *
from shogun.Kernel import *
import math

wndname = "Classification Test"

# Chunk the image using a grid this high and long
chunkGridSize = 7

#########################################
# !! IMPORTANT !!
# Red images are: 0
# Blue images are: 1
# Yellow images are: 2
red_label = 0
blue_label = 1
yellow_label = 2
########################################


def getFeatures(imglist):
    # This will be the matrix that holds every feature vector
    features = []

    for imgname in imglist:
        #print imgname
        
        img = cv.LoadImage(imgname)

        size = cv.GetSize(img);
        depth = img.depth;
        ch1 = cv.CreateImage(size, depth, 1)
        ch2 = cv.CreateImage(size, depth, 1)
        ch3 = cv.CreateImage(size, depth, 1)
        
        # Convert to LUV (Do I want to do this?)
        #cv.CvtColor(img, img, cv.CV_RGB2Luv)

        # Split into channels
        cv.Split(img,ch1,ch2,ch3, None)

        # This will hold all of the features (this should be 294 long at the end)
        imgvector = []
    
        for channel in [ch1, ch2, ch3]:

            # Get the block height and width
            blockHeight = channel.height / chunkGridSize
            blockWidth = channel.width / chunkGridSize

            # Because of integer truncation, and the loops below, it will be
            # nice to have these numbers be exact
            newHeight = blockHeight * chunkGridSize
            newWidth = blockWidth * chunkGridSize

            # range(start, stop, step). Duh.
            for i in range(0, newWidth, blockWidth):
                for j in range(0, newHeight, blockHeight):

                    #print
                    #print i, j
                    #print blockWidth, blockHeight
                    #print newHeight, newWidth
                    #print channel.height, channel.width
                    rect = (i, j, blockWidth, blockHeight)
                    cv.SetImageROI(channel, rect)

                    # TODO: make sure AvgSdv only works on the ROI
                    (mean, stdDev) = cv.AvgSdv(channel)
                    variance = stdDev[0] # * stdDev[0]
                    imgvector.append(mean[0])
                    imgvector.append(variance)

                    # Just in case.
                    cv.ResetImageROI(channel)

        features.append(imgvector)
        
    return features





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


# Taken from: http://peternixon.net/news/2009/07/28/natural-text-sorting-in-python/
def naturallysorted(L, reverse=False): 
    """ Similar functionality to sorted() except it does a natural text sort 
    which is what humans expect when they see a filename list. 
    """
    import re
    convert = lambda text: ('', int(text)) if text.isdigit() else (text, 0) 
    alphanum = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(L, key=alphanum, reverse=reverse) 


def normalizeFeatures(f):
    ''' Normalizes features to all be
    between 0 and 1'''
    # The important thing is to normalize each component (mean, variance) of each band separately.
    
    pass

def rgb2lst(img):
    ''' Not sure if this is necessary '''
    size = cv.GetSize(img);
    depth = img.depth;
    R = cv.CreateImage(size, depth, 1)
    G = cv.CreateImage(size, depth, 1)
    B = cv.CreateImage(size, depth, 1)
    L = cv.CreateImage(size, depth, 1)
    S = cv.CreateImage(size, depth, 1)
    T = cv.CreateImage(size, depth, 1)
    
    cv.Split(img,R,G,B, None)

    # L = (R + G + B) / sqrt(3)
    cv.Add(R, G, L)
    cv.Add(L, B, L)
    cv.ConvertScale(L, L, scale=1/math.sqrt(3))

    # S = R - B / sqrt(2)
    cv.Sub(R, B, S)
    cv.ConvertScale(S, S, scale=1/math.sqrt(2))

    # T = (R - 2*G + B)/sqrt(6)
    cv.ConvertScale(G, G, scale=2)
    cv.Sub(R, G, T)
    cv.Add(T, B, T)
    cv.ConvertScale(T, T, scale=1/math.sqrt(6))

    cv.Merge(L, S, T, None, img)

    return img
    

#cvShowImage(wndname, img)
#cvWaitKey(0)

def main():
    # Do you have stored data?
    data = True

    if data:
        features_train = numpy.loadtxt("features_train.txt")
        features_test = numpy.loadtxt("features_test.txt")

        train_labs_arr = numpy.loadtxt("labs_train.txt")
        test_labs_arr = numpy.loadtxt("labs_test.txt", dtype = int)

    else:
        # Red
        path = "images/red/"
        imglist_red = os.listdir(path)
        imglist_red = naturallysorted(map(lambda s: path + s, imglist_red))
        
        test_red = imglist_red[-5:]
        test_labs_red = [red_label]*len(test_red)
        imglist_red = imglist_red[0:-5]
        
        labs_red = [red_label]*len(imglist_red)
        
        # Blue
        path = "images/blue/"
        imglist_blue = os.listdir(path)
        imglist_blue = naturallysorted(map(lambda s: path + s, imglist_blue))
        
        test_blue = imglist_blue[-5:]
        test_labs_blue = [blue_label]*len(test_blue)
        imglist_blue = imglist_blue[0:-5]
        
        labs_blue = [blue_label]*len(imglist_blue)
        
        # Yellow
        path = "images/yellow/"
        imglist_yellow = os.listdir(path)
        imglist_yellow = naturallysorted(map(lambda s: path + s, imglist_yellow))
        
        test_yellow = imglist_yellow[-5:]
        test_labs_yellow = [yellow_label]*len(test_yellow)
        imglist_yellow = imglist_yellow[0:-5]
        
        labs_yellow = [yellow_label]*len(imglist_yellow)
        
    
        # Put them together again.
        train_imglist = imglist_red + imglist_blue + imglist_yellow
        train_labs = map(float, labs_red + labs_blue + labs_yellow)
        
        test_imglist = test_red + test_blue + test_yellow
        test_labs = map(float, test_labs_red + test_labs_blue + test_labs_yellow)
        
        # Get Features
        # TODO: this is the bottleneck. May want to save this stuff out to file. Good practice anyway.
        print "Getting features..."
        features_train = getFeatures(train_imglist)
        features_test = getFeatures(test_imglist)

        # Convert the list to an array, and get the transpose (probably not the best way to do it, but hey.)
        features_train = numpy.array(features_train).T
        features_test = numpy.array(features_test).T

        numpy.savetxt("features_train.txt", features_train)
        numpy.savetxt("features_test.txt", features_test)

        train_labs_arr = numpy.array(train_labs)
        test_labs_arr = numpy.array(test_labs)

        numpy.savetxt("labs_train.txt", train_labs_arr)
        numpy.savetxt("labs_test.txt", test_labs_arr)


    #print features_train
    #print features_train.shape, train_labs_arr.shape
    #print features_test.shape, test_labs_arr.shape
    
    # Begin LibSVM stuff.
    print 'LibSVMMultiClass'

    # orig parameters are:
    #C=1
    #epsilon=1e-5

    C = 10
    epsilon = 0.001

    #for C in range(49, 50):
    #for epsilon in [6]:

    feats_train=RealFeatures(features_train)
    feats_test=RealFeatures(features_test)
    #width=2.1
    width = 2.1
    kernel=GaussianKernel(feats_train, feats_train, width)
    
    labels=Labels(train_labs_arr)
    
    svm=LibSVMMultiClass(C, kernel, labels)
    svm.set_epsilon(epsilon)
    svm.train()
    
    kernel.init(feats_train, feats_test)
    out = svm.classify().get_labels()
    
    #if (out >= 1).any():
    print 
    print "============================"
    print C, epsilon 
    print numpy.vstack((out.T, test_labs_arr)).T
    
    

if __name__ == "__main__":
   main()
   #s = ["t100","t34","t2","t1445","t90","t45","t455","t4"]
   #print naturallysorted(s)
   #img = cv.LoadImage("images/yellow/yellow4.jpg")
   #img = rgb2lst(img)
   #cv.ShowImage(wndname, img)
   #cv.WaitKey(0)
