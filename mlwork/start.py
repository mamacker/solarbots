import numpy as np
import cv2
import sys
import ml
import time

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

try:
    # Read input image
    img = cv2.imread(sys.argv[1])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,8)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=10)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    i = 0
    for c in cnts:
        i += 1
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            ROI = img[y:y+h, x:x+w]
            #cv2.imshow("area" + str(i), ROI)
            #cv2.waitKey(0)
            break

    img_gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", img_gray)
    #cv2.waitKey(0)
    img_gauss = cv2.GaussianBlur(img_gray, (3,3), 0)
    #cv2.imshow("blur", img_gauss)
    #cv2.waitKey(0)
    kernel = np.ones((4,4), np.uint8) 
    erode = cv2.erode(img_gauss, kernel, iterations=1)
    #cv2.imshow("erod", erode)
    #cv2.waitKey(0)

    th3 = cv2.adaptiveThreshold(erode,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,10)
    ctrs = cv2.findContours(th3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    ctrs, rects = sort_contours(ctrs)
    top = []
    bottom = []
    #print("Height:", img.shape[0], img.shape[0]/2, rects[0][3])
    if rects[0][3] < img.shape[0]/2:
        #print("Yup.  Its a double line.")
        for rect in rects:
            x, y, w, h = rect
            if y > img.shape[0]/2:
                bottom.append(rect)
            else:
                top.append(rect)
        rects = top + bottom
    orig = ROI.copy()
    translation = ""
    imCt = 0
    #ordering = {}
    #imgsall = {}
    for rect in rects:
        imCt = imCt + 1
        x, y, w, h = rect
        tmpImage = orig[y:y+h, x:x+w]
        cv2.rectangle(ROI, (x, y), (x+w, y+h), (0, 255, 0), 3)
        letter = ml.CheckSim(tmpImage)
        print(letter)
        #cv2.imwrite("pictures/"+letter+"_" + str(time.time()) + ".png", tmpImage)
        #ordering[imCt] = letter
        #imgsall[imCt] = tmpImage.copy()

    cv2.imwrite("pictures/whole" + str(time.time()) + ".png", ROI)

    #for i in sorted (ordering.keys()) :
    #    print(i,":", ordering[i], end = " ")
    #    cv2.imwrite("pictures/"+str(i)+"-"+ordering[i]+"part" + str(time.time()) + ".png", imgsall[i])
except Exception as e:
    print("E: " + str(e))
    sys.exit(1)