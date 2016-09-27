"""                           InterlaceSimple.py
Created on Tue Sep 20 15:08:56 2016

A simple image interlacing program. Should be suitable for use with parallax barriers and lenticular lenses
that perfectly overlap an integer number of screen pixels.
For lenticular lens screens where the lenses do not overlap exactly with the screen pixels, use InterlaceUpsampled.py
to improve image quality.

@author: dmcauslan
"""

#Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.transform import resize

## Define interlacing parameters.
nViews = 5                      # Number of interlaced images
screenRes = (1080, 1920)        # Screen dimensions [height width] (pixels)
imageRes = (screenRes[0], screenRes[1]//nViews)     # Resolution of each interlaced image

# Define filename etc.
imType         = 'calibration'           # type of image to be interlaced (e.g., 'calibration', 'general', etc.)
generalBase    = 'ferrari'           # base file name (for 'general' case)
generalDir     = 'H:/David/Google Drive/Lenticular Sheet/images/{}/'.format(generalBase) # base directory (for 'general' case)
generalExt     = 'jpg'               # file format    (for 'general' case)


## Loads/creates the images to be interlaced.
def imageLoader(imageRes, nViews, imType, generalDir, generalBase, generalExt):    
    print('> Loading the images to be interlaced...')
    # Loop over the number of views
    for i in range(nViews):
        print('  - Loading frame {} of {}...'.format(i+1, nViews))
        # Choose which set of images to create/load
        # Calibration image - all images are black, except the centre image which is white        
        if imType == 'calibration':
            # On first iteration create array lfImage to hold all images            
            if i==0:
                nImages = np.zeros(np.hstack((imageRes,3,nViews)), dtype = np.uint8)
            nImages[:,:,:,i] = 255*(i==round((nViews)/2))*np.ones(np.hstack((imageRes,3)), dtype = np.uint8)
        # Image used for alignment - alternating red, green, blue images.
        elif imType == 'redgreenblue':
            # On first iteration create array lfImage to hold all images            
            if i==0:
                nImages = np.zeros(np.hstack((imageRes,3,nViews)), dtype = np.uint8)
            if i%3 == 0:
                nImages[:,:,0,i] = 255*np.ones(imageRes)
            elif i%3 == 1:
                nImages[:,:,2,i] = 255*np.ones(imageRes)
            elif i%3 == 2:
                nImages[:,:,1,i] = 255*np.ones(imageRes)
        # Image used for measuring crosstalk between views
        elif imType == 'numbersCrosstalk':
            # How the numbers will be arranged, need to change this as we change nViews            
            nRow = 2
            nCol = 3
            # Load the numbers crosstalk images
            im1 = 255*mpimg.imread('H:/David/Google Drive/Lenticular Sheet/images/numbers crosstalk/numbers crosstalk 0{}.png'.format(i+1))
            sz = np.shape(im1)
            # Rearrange them so the different images are arranged in a grid
            im2 = np.zeros(np.hstack((nRow*sz[0], nCol*sz[1], 3)), dtype = np.uint8)
            rows = ((i%nRow)*sz[0]+np.arange(sz[0])).astype(int)
            cols = (np.floor(i/nRow)*sz[1]+np.arange(sz[1])).astype(int)
            im2[rows[:, np.newaxis], cols, :] = im1
            # On first iteration create array lfImage to hold all images
            if i == 0:
                nImages = np.zeros(np.hstack((np.shape(im2),nViews)),dtype = np.uint8)
            nImages[:,:,:,i] = im2
        # General image interlacing - for example ferrari images
        elif imType == 'general':
            # On first iteration create array lfImage to hold all images            
            if i == 0:
                tmp = mpimg.imread('{}{}-{:02d}.{}'.format(generalDir, generalBase, i+1, generalExt))
                nImages = np.zeros(np.hstack([np.shape(tmp),nViews]), dtype = np.uint8)
            nImages[:,:,:,i] = mpimg.imread('{}{}-{:02d}.{}'.format(generalDir, generalBase, i+1, generalExt))                     
        else:
            raise ValueError('You didnt correctly choose a set of images to load!')   
    
    # Plot images
    fig = plt.figure(1)
    plt.clf()    
    for n in range(nViews):
        ax = fig.add_subplot(231+n)
        ax.imshow(nImages[:,:,:,n],interpolation="nearest", aspect='auto')
        plt.title("View {}".format(n))
    plt.show()
    
    return nImages


## Interlaces the images
def imageInterlacer(nImages, nViews, screenRes, imageRes):
    # Create total image
    totImage = np.zeros(np.hstack((screenRes,3)), dtype = np.uint8)
    
    # Loop over images, resize them, then interlace them
    for n in range(nViews):
        # resize image
        tmpImage = resize(nImages[:,:,:,n],imageRes, preserve_range=True)        
        # Interlace image
        totImage[:,n::nViews,:] = tmpImage
        
    # Plot interlaced image
    fig3 = plt.figure(3)
    fig3.clf()
    plt.imshow(totImage, interpolation = 'nearest')
    plt.show()
    
    return totImage


## Save the image
def saveImage(imageTot, imType, generalBase, nViews):
    if imType == 'general':
        fName = 'H:/David/Google Drive/Canopy/Interlaced Images/{}_{}view.png'.format(generalBase,nViews)
    else:
        fName = 'H:/David/Google Drive/Canopy/Interlaced Images/{}_{}view.png'.format(imType,nViews)
    mpimg.imsave(fName, imageTot)


##Running the code
nImages = imageLoader(imageRes, nViews, imType, generalDir, generalBase, generalExt) 
imageTot = imageInterlacer(nImages, nViews, screenRes, imageRes)
saveImage(imageTot, imType, generalBase, nViews)