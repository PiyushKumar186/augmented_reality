# -*- coding: utf-8 -*-
import numpy as np
import cv2
import glob

cap = cv2.VideoCapture(0)

images = glob.glob('*.jpg') #all the jpg images in the folder can be displayed
currentImage=6  #the first image is selected in your local directory 

replaceImg=cv2.imread(images[currentImage])
rows,cols,ch = replaceImg.shape
pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])    #this points are necessary for the transformation

zoomLevel = 0   #when zoomLevel is positive it zooms in, when its negative it zooms out
processing = True   #boolean variable using for disabling the image processing
maskThreshold=10

while(True): #IF Condition is true
    # Then the video camera captures frame-by-frame
    ret, img = cap.read()  #ret->return
    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #cvtcolor i.e convert color is used for converting the colored frame into gray
    #This function is used to detect the corners of the chessboard, 9x6 is the number of corners to find
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None) #9 X 6 is our defined chessboard pattern you can use any the best case is (9,6),(9,5) etc or basically it depends on the image dimension 

    # If found, do the processing
    if ret == True and processing:
        #pts2 is used for defining the perspective transform
        pts2 = np.float32([corners[0,0],corners[8,0],corners[len(corners)-1,0],corners[len(corners)-9,0]])
        #compute the transform matrix
        M = cv2.getPerspectiveTransform(pts1,pts2)
        rows,cols,ch = img.shape
        #make the perspective change in a image of the size of the camera input
        dst = cv2.warpPerspective(replaceImg,M,(cols,rows))
        #A mask is created for adding the two images
        #maskThreshold is a variable because that allows to subtract the black background from different images
        ret, mask = cv2.threshold(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY),maskThreshold, 1, cv2.THRESH_BINARY_INV)
        #Erode and dilate are used to delete the noise
        mask = cv2.erode(mask,(3,3))
        mask = cv2.dilate(mask,(3,3))
        #The two images are added using the mask
        for c in range(0,3):
            img[:, :, c] = dst[:,:,c]*(1-mask[:,:]) + img[:,:,c]*mask[:,:]
#           cv2.imshow('mask',mask*255) #This is the masking technique which will show how this whole program works uncomment it, if you want to understand the basic principle
     #finally the result is presented
    cv2.imshow('img',img)  
    
    #Wait for the key 
    key = cv2.waitKey(1)
    print key
    #decide the action based on the key value (quit, zoom, change image)
    if key == ord('q'): # quit
        print 'Quit'
        break
    if key == ord('p'): # processing
        processing = not processing
        if processing: 
            print 'Activated image processing'
        else: 
            print 'Deactivated image processing'
    if key == 43: # + zoom in
        zoomLevel=zoomLevel+0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print 'Zoom in'
    if key == 45: # - zoom out
        zoomLevel=zoomLevel-0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print 'Zoom in'
        print 'Zoom out'
    if key == 2555904: # -> next image
        if currentImage<len(images)-1:
            currentImage=currentImage+1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
            print 'Next image'
        else:
            print 'No more images on the right'
    if key == 2424832: # <- previous image
        if currentImage>0:
            currentImage=currentImage-1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])

            print 'Previous image'
        else:
            print 'No more images on the left'
            
    if key == 2490368: # increase threshold
        if maskThreshold<255:
            maskThreshold=maskThreshold+1
            print 'Increase Mask Threshold'
        else:
            print 'Mask Threshold at the maximum value'
    if key == 2621440: # decrease threshold
        if maskThreshold>0:
            maskThreshold=maskThreshold-1
            print 'Decrease Mask Threshold'
        else:
            print 'Mask Threshold at the minimum value'

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
