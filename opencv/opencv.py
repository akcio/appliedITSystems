import cv2
import cv2 as cv
import os
import matplotlib as be
from matplotlib import pyplot as plt
import numpy
from matplotlib import pyplot

print(cv2.__version__)

def calcBorders(points : list):
    lastPlus = False
    lastMinus = True
    pointsStart = []
    pointsEnd = []
    for item in range(2, len(points)):
        if (points[item] - points[item - 1]) > 0 and not lastPlus:
            pointsStart += [item]
        if (points[item] - points[item - 1]) < 0 and not lastMinus:
            pointsEnd += [item]
        lastPlus = (points[item] - points[item - 1]) > 0
        lastMinus = (points[item] - points[item - 1]) < 0
    return {'start' : pointsStart, 'end' : pointsEnd}


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

xGist = [sum(imgGray[k]) / len(imgGray[k]) for k in range(imgGray.shape[0])]
xGist_median = numpy.median(xGist) * 0.78
xGistNorm = [min(x, xGist_median) for x in xGist]
# img1 = [img0[x] - minimal for x in range(len(img0))]
plt.title("Гистограмма по строкам")
plt.plot(range(len(xGist)), xGist); plt.show()

plt.title("Гистограмма по строкам new")
plt.plot(range(len(xGistNorm)), xGistNorm); plt.show()

xPoints = calcBorders(xGistNorm)

yGist = [sum(imgGray[:, k]) / len(imgGray[:, k]) for k in range(imgGray.shape[1])]
yGist_median = numpy.median(yGist) * 0.78
yGistNorm = [min(x, yGist_median) for x in yGist]

plt.title("Гистограмма по столбцам")
plt.plot(range(len(yGist)), yGist); plt.show()
plt.title("Гистограмма по стобцам new")
plt.plot(range(len(yGistNorm)), yGistNorm); plt.show()

yPoints = calcBorders(yGistNorm)

trainData = []
responses = []
for x in range(min(len(xPoints['start']), len(xPoints['end']))):
    for y in range(min(len(yPoints['start']), len(yPoints['end']))):
        imageNumber = imgGray[xPoints['start'][x]:xPoints['end'][x] + 1,
                    yPoints['start'][y]:yPoints['end'][y] + 1]
        if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
            trainData += [imageNumber]
            responses.append(int(len(responses) / 500))



#Save pictures to harddrive
# number = 0
# for item in trainData:
#     cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png", item)
#     number += 1
print("Len trainData:", len(trainData))

knn = cv2.ml.KNearest_create()
trainData = numpy.array(trainData)
responses = numpy.array(responses).astype(numpy.float32)
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)
# ret, results, neighbours ,dist = knn.find_nearest(trainData[0], 3)
#
# print( "result: ", results,"\n")
# print( "neighbours: ", neighbours,"\n")
# print( "distance: ", dist)

plt.show()