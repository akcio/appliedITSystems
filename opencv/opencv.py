import cv2
import cv2 as cv
import os
import matplotlib as be
from matplotlib import pyplot as plt
import numpy
from matplotlib import pyplot
import sklearn
from sklearn.decomposition import KernelPCA

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
            imageNumber = imgGray[
                          # xPoints['start'][x]-1, 0:xPoints['end'][x] + 1,
                          max(xPoints['start'][x]-1, 0):xPoints['end'][x] + 1,
                          max(yPoints['start'][y]-1, 0):yPoints['end'][y] + 1
                          ]
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

def findDigitsInImage():
    # test = prepareImage(os.path.join(curFolder, 'test_inverse2.png'))

    test = prepareImageMSER(os.path.join(curFolder, 'test5.png'), needSave=True)
    # test = prepareImageNew(os.path.join(curFolder, 'test5.png'), False, False, saveToFiles=True)

    resultsList = []
    for item in test:
        res, results, neighbours ,dist = knn.findNearest(kpca.transform(numpy.array(item, dtype=numpy.float32).reshape(-1, 17*17)).reshape(1,-1), 3)
        resultsList.append(results[0][0])
        # print( "result: ", results,"\n")
        # print( "neighbours: ", neighbours,"\n")
        # print( "distance: ", dist)


    print(resultsList)

def prepareImageMSER(path, needSave = False, oldStyleMode = False):
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mser = cv2.MSER_create(_min_area=10)
    regions, _ = mser.detectRegions(imgGray)

    rectangles = list(set([cv2.boundingRect(x) for x in regions]))
    if oldStyleMode:
        res = []
        for i in range(len(rectangles)):
            xs, ys, ws, hs = rectangles[i]
            hasBigger = False
            for k in range(len(rectangles)):
                if i == k:
                    continue
                xi, yi, wi, hi = rectangles[k]
                a = max(xi, xs)
                b = min(xs + ws, xi + wi)
                c = max(yi, ys)
                d = min(ys + hs, yi + hi)

                if (a < b) and (c < d):
                    # hasBigger = True
                    if (wi * hi > ws * hs):
                        hasBigger = True

            if not hasBigger:
                res.append(rectangles[i])

        rectangles = res

        trainData = []

        for contour in rectangles:
            x, y, w, h = contour
            if w < 13 or h < 13:
                continue
            imageNumber = imgGray[y:y + h, x: x + w]
            imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
                17 * 17, -1)
            trainData += [numpy.array(imageNumber, dtype=numpy.float32)]
        return trainData


    copyImg = img.copy()
    [cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), cv2.FILLED) for x, y, w, h in rectangles]

    thresh = cv2.inRange(img, (0, 0, 255), (0, 0, 255))

    reg2, _ = mser.detectRegions(thresh)
    rectangles = [cv2.boundingRect(p) for p in reg2]

    trainData = []
    number = 0
    rectangles = sorted(rectangles, key=lambda key: key[0] + key[1] * 10000)
    test = [x[0] + x[1] * 10000 for x in rectangles]
    for contour in rectangles:
        x, y, w, h = contour
        if w * h < 3 * 13:
            continue
        imageNumber = imgGray[y:y + h, x: x + w]
        if needSave:
            cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png",
                        cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
        imageNumber = numpy.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
            17 * 17, -1)

        number += 1
        trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

    return trainData

def newTrainData():
    from sklearn import datasets
    digits = datasets.load_digits()

    tmp = [[i for i in range(len(digits['target'])) if digits['target'][i] == y] for y in range(10)]

    allDigits = []
    targets = []

    # imageNumber = numpy.array(cv2.resize(imageNumber, (17,17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1)
    #         trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

    for digit in tmp:
        for item in digit:

            allDigits.append(numpy.array(cv2.resize(digits['images'][item], (17, 17), interpolation=cv2.INTER_AREA)).reshape(17*17, -1))
            targets.append(digits['target'][item])

    return allDigits, targets

def face_trainData(needsave = False):
    face_cascade = cv2.CascadeClassifier('trainset/haarcascade_frontalface_default.xml')

    img = cv2.imread('trainset/yalefaces.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, scaleFactor=6.2)

    print(len(faces))
    imgNum = 0
    faces = sorted(faces, key=lambda k: k[0] + k[1] * 10000)
    trainData = []
    responses = []
    for (x, y, w, h) in faces:
        tmpImage = imgGray[y:y + h, x:x + w]
        if needsave:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("tmp/" + str(imgNum) + '.png', tmpImage)
        imageNumber = numpy.array(cv2.resize(tmpImage, (512, 512), interpolation=cv2.INTER_AREA)).reshape(
            512 * 512, -1)
        responses.append(int(imgNum/11))
        imgNum += 1
        trainData += [numpy.array(imageNumber, dtype=numpy.float32)]

    return trainData, responses


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

# trainData, responses = newTrainData()
trainData, responses = face_trainData()
# trainData = prepareImageMSER(os.path.join(curFolder, 'trainset/digits_inverse4.png'))

print("Len trainData:", len(trainData))

checkData = []
checkResponse = []
import random
for i in range(int(len(trainData)*0.2)):
    number = random.randint(0, len(trainData) - 1)
    checkResponse.append(responses[number])
    del responses[number]
    checkData.append(trainData[number])
    del trainData[number]
print(len(trainData), len(checkData))
knn = cv2.ml.KNearest_create()
responses = numpy.array(responses)

print(trainData[0].shape)

knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)

print("Without PCA")
for kNeares in range(1, 6):
    # break
    success = 0
    total = 0
    for t in range(3):
        for i in range(len(checkData)):
            res, results, neighbours, dist = knn.findNearest(numpy.array(checkData[i], dtype=numpy.float32).reshape(1, -1), kNeares)
            if res == checkResponse[i]:
                success += 1
            total += 1
    print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)

print("With PCA")

temp = numpy.array(trainData, dtype=numpy.float32).reshape(len(trainData), -1)
kpca = KernelPCA(n_components=30,kernel='rbf', gamma=1e-9)

kpca.fit(temp)

trainData = kpca.transform(temp)


# knn.train(numpy.array(trainData, dtype=numpy.float32), cv2.ml.ROW_SAMPLE, responses)
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)

for i in range(len(checkData)):
    checkData[i] = kpca.transform(numpy.array(checkData[i]).reshape(1, -1))


for kNeares in range(1, 8):
    # break
    success = 0
    total = 0
    for t in range(3):
        for i in range(len(checkData)):
            try:
                # temp = kpca.transform(numpy.array(checkData[i]).reshape(-1, 17*17))
                res, results, neighbours, dist = knn.findNearest(checkData[i], kNeares)
                if res == checkResponse[i]:
                    success += 1
            except Exception as ex:
                print(ex)
            total += 1
    print("k:", kNeares, "total:", total, "succ:", success, "error:", 1 - success / total)