######
# the digit recognition method is modified from the tutorial from: 
# http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html
# important note:
# the core algorithm of matrix recognition (from handwritten matrices to 2D-list) is solely developed and written by Tianyi Zhu
######
# Import the necessary modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import copy
# this function takes in the image filename in the local path, processes the image, classifies the digits in the image based on the pre-loaded MNIST classifier, and converts the handwritten matrix image into a 2D list
def recog(filename):
    # Load the "pickled" classifier
    classifier = joblib.load("digits_cls.pkl")
    
    # Read the input image in the local path
    im = cv2.imread(filename)
    
    # Convert to grayscale
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian filtering to smoothe image
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
    
    # Threshold the image by turning it into a binary image, text is white and background is black
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours in the image
    # cv2.RETR_EXTERNAL: extract only the outer contours
    # cv2.CHAIN_APPROX_SIMPLE: removes redundant points and compresses the contour, saving memory
    image, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get rectangles contains each contour
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

########## Customized algorithm to convert rectangular regions of handwritten digits into a 2D list
    matrix = [] # a shell list for the 2D list
    hValues = [] # a list of height values
    
    # find the smallest height value from the list of rectangle
    for rect in rects:
        hValues.append(rect[3])
    smallestH = sorted(hValues)[0]
    errorTh = smallestH
    
    # sort the rectangle list (of tuples) by y-values
    rectByY = sorted(rects, key = lambda x: x[1])
    
    # slice the 1D list into rows and append them to the list shell
    index = 0
    if len(rectByY) == 1:
        matrix = rectByY
    else:
        for i in range(1, len(rectByY)):
            if rectByY[i][1] - rectByY[i-1][1] > errorTh:
                matrix.append(rectByY[index:i])
                index = i
        # append the last line, not reachable by indexing
        matrix.append(rectByY[index:])

    # sort each row of the 2D list by x-values
    for row in matrix:
        row.sort()
########## Customized algorithm to convert rectangular regions of handwritten digits into a 2D list
    # create a deep copy of matrix
    newMatrix = copy.deepcopy(matrix)

    # For each rectangular region, calculate HOG (histogram of oriented gradients) features and predict the digit using Linear Supporting Vector Machine
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            # Make the rectangular region around the digit
            leng = int(matrix[i][j][3] * 1.6)
            pt1 = int(matrix[i][j][1] + matrix[i][j][3] // 2 - leng // 2)
            pt2 = int(matrix[i][j][0] + matrix[i][j][2] // 2 - leng // 2)
            roi = im_th[pt1:pt1+leng, pt2:pt2+leng]

            # Resize the image to locate region of interest
            # cv2.INTER_AREA: resample using pixel area relation, preferred method for image decimation
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))

            # Calculate the HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)

            # destructively modify the newMatrix by filling it with classified digits
            newMatrix[i][j] = classifier.predict(np.array([roi_hog_fd], 'float64')).tolist()[-1]
    return newMatrix