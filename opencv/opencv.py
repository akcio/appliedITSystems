import cv2
import cv2 as cv
import os
import matplotlib as be
from matplotlib import pyplot as plt
import numpy
from matplotlib import pyplot

print(cv2.__version__)

curFolder = os.path.dirname(__file__)
trainsetFolder = os.path.join(curFolder, 'trainset')


im = cv.imread(os.path.join(trainsetFolder, 'digits_inverse.png'))


imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
qr = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)


ret, thresh = cv.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contours, -1, (0,255,0), 3)

img = cv2.imread(os.path.join(trainsetFolder, 'digits_inverse.png'))
imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


img0 = [sum(imgGray[k]) for k in range(imgGray.shape[0])]
img1 = [min(x, 10) for x in img0]
# img1 = [img0[x] - minimal for x in range(len(img0))]
plt.title("Гистограмма по строкам")
plt.plot(range(len(img0)), img0); plt.show()


plt.title("Гистограмма по строкам new")
plt.plot(range(len(img1)), img1); plt.show()
