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


im = cv.imread(os.path.join(trainsetFolder, 'digits.png'))


imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
qr = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
xr = qr.reshape(50,20,100,20)
br = xr.swapaxes(1,2)
train = br.reshape(-1,400)


ret, thresh = cv.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contours, -1, (0,255,0), 3)

img = cv2.imread(os.path.join(trainsetFolder, 'digits.png'),0)
plt.hist(img.ravel(),256,[0,256]); plt.show()


qr = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
xr = qr.reshape(50,20,100,20)
br = xr.swapaxes(1,2)
train = br.reshape(-1,400)
knn = cv2.ml.KNearest_create()
tags = numpy.arange(10).repeat(500)
train = train.astype(numpy.float32)
knn.train(train,cv2.ml.ROW_SAMPLE,tags)
sm = numpy.array(train)
test = cv2.imread(os.path.join(curFolder, 'dione.png'))
test = cv2.cvtColor(test,cv2.COLOR_BGR2GRAY)
test = 255-test
t = numpy.zeros((test.shape[0],1),'uint8')
test=numpy.column_stack((t,test))
v = numpy.sum(test, 1)
b = v > 100
b = b.astype(int)
bd = numpy.diff(b)
s = numpy.array([numpy.where(bd == 1),numpy.where(bd == -1)])
q = s.reshape(s.shape[0],s.shape[2])
q0 = q.swapaxes(0,1)
r = [test[idx[0]:idx[1]+1] for idx in q0]
lst=[]

for idx in r:
    vs = numpy.sum(idx, 0)
    pyplot.plot(vs)
    b = vs > 10
    b = b.astype(int)
    bd = numpy.diff(b)
    s = numpy.array([numpy.where(bd == 1),numpy.where(bd == -1)])
    q = s.reshape(s.shape[0],s.shape[2])
    q1 = q.swapaxes(0,1)
    lst1=[]
    for id2 in q1:
        oneof=idx[0:idx.shape[0],id2[0]:id2[1]+1]
        oneof = cv2.resize(oneof, (20,20), cv2.INTER_MAX)
        sm=oneof.reshape(1,-1)
        sm=sm.astype(numpy.float32)
        res=knn.findNearest(sm,20)
        res=res[1][0][0].astype(int)
        lst1.append(res)
    lst.append(lst1)
print(lst)


