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
            pointsStart += [item-1]
        if (points[item] - points[item - 1]) < 0 and not lastMinus:
            pointsEnd += [item+1]
        lastPlus = (points[item] - points[item - 1]) > 0
        lastMinus = (points[item] - points[item - 1]) < 0
    return {'start' : pointsStart, 'end' : pointsEnd}


curFolder = os.path.dirname(__file__)
trainsetFolder = os.path.join(curFolder, 'trainset')

def prepareImage(path, needInverse = False, drawPlot = False, saveToFiles = False):
    img = cv2.imread(path)
    if needInverse:
        img = cv2.bitwise_not(img)
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv2.imwrite(os.path.join(curFolder, 'test_inverse.png'), img)

    xGist = [sum(imgGray[k]) / len(imgGray[k]) for k in range(imgGray.shape[0])]
    xGist_median = numpy.median(xGist) * 0.78
    xGistNorm = [0 if x < xGist_median else 1 for x in xGist]
    if drawPlot:
        plt.title("Гистограмма по строкам")
        plt.plot(range(len(xGist)), xGist); plt.show()
        plt.title("Гистограмма по строкам new")
        plt.plot(range(len(xGistNorm)), xGistNorm); plt.show()

    xPoints = calcBorders(xGistNorm)

    yGist = [sum(imgGray[:, k]) / len(imgGray[:, k]) for k in range(imgGray.shape[1])]
    yGist_median = numpy.median(yGist) * 0.78
    yGistNorm = [0 if x < yGist_median else 1  for x in yGist]

    if drawPlot:
        plt.title("Гистограмма по столбцам")
        plt.plot(range(len(yGist)), yGist); plt.show()
        plt.title("Гистограмма по стобцам new")
        plt.plot(range(len(yGistNorm)), yGistNorm); plt.show()

    yPoints = calcBorders(yGistNorm)

    trainData = []
    responses = []
    number = 0
    for x in range(min(len(xPoints['start']), len(xPoints['end']))):
        for y in range(min(len(yPoints['start']), len(yPoints['end']))):
            imageNumber = imgGray[xPoints['start'][x]:xPoints['end'][x] + 1,
                          yPoints['start'][y]:yPoints['end'][y] + 1]
            if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
                # Save pictures to harddrive
                if saveToFiles:
                    cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png", cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
                    number += 1
                imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                    17 * 17, -1)
                trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
                responses.append(len(responses) // 500)

    return trainData

def prepareImageNew(path, needInverse = False, drawPlot = False, saveToFiles = False):
    img = cv2.imread(path)
    if needInverse:
        img = cv2.bitwise_not(img)
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv2.imwrite(os.path.join(curFolder, 'test_inverse.png'), img)

    # Save pictures to harddrive
    # number = 0
    # for item in trainData:
    #     cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png", item)
    #     number += 1

    xGist = [sum(imgGray[k]) / len(imgGray[k]) for k in range(imgGray.shape[0])]
    xGist_median = numpy.median(xGist) *0.45
    xGistNorm = [0 if x < 10 else 1 for x in xGist]
    if drawPlot:
        plt.title("Гистограмма по строкам")
        plt.plot(range(len(xGist)), xGist); plt.show()
        plt.title("Гистограмма по строкам new")
        plt.plot(range(len(xGistNorm)), xGistNorm); plt.show()

    xPoints = calcBorders(xGistNorm)

    trainData = []
    responses = []
    number = 0
    for x in range(min(len(xPoints['start']), len(xPoints['end']))):
        curImage = imgGray[xPoints['start'][x]:xPoints['end'][x] +1, :]
        yGist = [sum(curImage[:, k]) / len(curImage[:, k]) for k in range(curImage.shape[1])]
        yGist_median = numpy.median(yGist) * 0.2
        yGistNorm = [0 if x < 10 else 1 for x in yGist]
        yPoints = calcBorders(yGistNorm)

        if drawPlot:
            plt.title("Гистограмма по столбцам")
            plt.plot(range(len(yGist)), yGist);
            plt.show()
            plt.title("Гистограмма по стобцам new")
            plt.plot(range(len(yGistNorm)), yGistNorm);
            plt.show()

        for y in range(min(len(yPoints['start']), len(yPoints['end']))):
            imageNumber = imgGray[xPoints['start'][x]:xPoints['end'][x] + 1,
                          yPoints['start'][y]:yPoints['end'][y] + 1]
            if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
                if saveToFiles:
                    cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png",
                                cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
                    number += 1
                imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                    17 * 17, -1)
                trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
                responses.append(int(len(responses) / 500))


    return trainData

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
# plt.title("Гистограмма по строкам")
# plt.plot(range(len(xGist)), xGist); plt.show()
#
# plt.title("Гистограмма по строкам new")
# plt.plot(range(len(xGistNorm)), xGistNorm); plt.show()

xPoints = calcBorders(xGistNorm)

yGist = [sum(imgGray[:, k]) / len(imgGray[:, k]) for k in range(imgGray.shape[1])]
yGist_median = numpy.median(yGist) * 0.78
yGistNorm = [min(x, yGist_median) for x in yGist]

# plt.title("Гистограмма по столбцам")
# plt.plot(range(len(yGist)), yGist); plt.show()
# plt.title("Гистограмма по стобцам new")
# plt.plot(range(len(yGistNorm)), yGistNorm); plt.show()

yPoints = calcBorders(yGistNorm)

trainData = []
responses = []
number = 0
for x in range(min(len(xPoints['start']), len(xPoints['end']))):
    for y in range(min(len(yPoints['start']), len(yPoints['end']))):
        imageNumber = imgGray[xPoints['start'][x]:xPoints['end'][x] + 1,
                    yPoints['start'][y]:yPoints['end'][y] + 1]
        if imageNumber.shape[0] > 10 and imageNumber.shape[1] > 10:
            # cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + "_" + str(int(len(responses) / 500)) + ".png",
            #             cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
            imageNumber = numpy.array(cv2.resize(imageNumber, (17,17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1)
            trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
            responses.append(int(len(responses) / 500))
            number +=1


#Save pictures to harddrive
# number = 0
# for item in trainData:
#     cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png", item)
#     number += 1
print("Len trainData:", len(trainData))

# checkData = []
# checkResponse = []
# import random
# for i in range(int(len(trainData)*0.2)):
#     number = random.randint(0, len(trainData) - 1)
#     checkResponse.append(responses[number])
#     del responses[number]
#     checkData.append(trainData[number])
#     del trainData[number]
# print(len(trainData), len(checkData))

knn = cv2.ml.KNearest_create()
responses = numpy.array(responses)
knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)


# for kNeares in range(1, 8):
#     success = 0
#     total = 0
#     for t in range(3):
#         for i in range(len(checkData)):
#             res, results, neighbours, dist = knn.findNearest(numpy.array(checkData[i], dtype=numpy.float32).reshape(1, -1), kNeares)
#             if res == checkResponse[i]:
#                 success += 1
#             total += 1
#     print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)

# test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))
test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

resultsList = []
for item in test:
    res, results, neighbours ,dist = knn.findNearest(numpy.array(item, dtype=numpy.float32).reshape(1,-1), 3)
    resultsList.append(results[0][0])
    # print( "result: ", results,"\n")
    # print( "neighbours: ", neighbours,"\n")
    # print( "distance: ", dist)


print(resultsList)