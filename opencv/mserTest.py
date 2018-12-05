import cv2
import numpy as np
import os
from sklearn import datasets

def removeDuplicities(lst : list):
    return list(set(lst))

def detectRoundel( frame, debug=False ):
    g_mser = cv2.MSER_create(_delta=10)# _delta = 10, _min_area=100, _max_area=300*50*2 )
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
    contours = g_mser.detect(gray, None)
    rectangles = []
    circles = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        area = len(cnt) # MSER returns all points within area, not boundary points
        rectangleArea = float(rect[1][0]*rect[1][1])
        rectangleAspect = max(rect[1][0], rect[1][1]) / float(min(rect[1][0], rect[1][1]))
        if area/rectangleArea > 0.70 and rectangleAspect > 3.0:
            (x,y),(w,h),angle = rect
            rectangles.append( ((int(x+0.5),int(y+0.5)), (int(w+0.5),int(h+0.5)), int(angle)) )
        cir = cv2.minEnclosingCircle(cnt)
        (x,y),radius = cir

    rectangles = removeDuplicities( rectangles )
    result = False
    if debug:
        for rect in rectangles:
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours( frame,[box],0,(255,0,0),2)
        for cir in circles:
            (x,y),radius = cir
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (0,255,0), 2)
        if result:
            (x1,y1),(x2,y2) = result
            cv2.line(frame, (int(x1),int(y1)), (int(x2),int(y2)), (0,0,255), 3)
    return result

def find_biggest_contour(image):
    # Copy
    image = image.copy()
    #input, gives all the contours, contour approximation compresses horizontal,
    #vertical, and diagonal segments and leaves only their end points. For example,
    #an up-right rectangular contour is encoded with 4 points.
    #Optional output vector, containing information about the image topology.
    #It has as many elements as the number of contours.
    #we dont need it
    _, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Isolate largest contour
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
    return biggest_contour, mask

#Create MSER object
mser = cv2.MSER_create(_min_area=10)

#Your image path i-e receipt path
curFolder = os.path.dirname(__file__)
img = cv2.imread(os.path.join(curFolder, 'trainset/digits_inverse4.png')) #'test5.png'))
# img = cv2.imread(os.path.join(curFolder, 'test5.png'))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# loop over the digit area candidates
vis = img.copy()

# detectRoundel(img, debug=True)
cv2.waitKey(0)



#detect regions in gray scale image
regions, _ = mser.detectRegions(gray)

# hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
hulls = [cv2.boundingRect(p) for p in regions]
hulls = removeDuplicities(hulls)

# hulls = sorted(hulls, key=lambda k : k[2]*k[3], reverse=True)


# res = []
# alreadyHasBigger = []
# for i in range(len(hulls)):
#     xs, ys, ws, hs = hulls[i]
#     hasBigger = False
#     for k in range(len(hulls)):
#         if i == k or k in alreadyHasBigger:
#             continue
#         xi, yi, wi, hi = hulls[k]
#         a = max(xi, xs)
#         b = min(xs+ws, xi+wi)
#         c = max(yi, ys)
#         d = min(ys+hs, yi+hi)
#
#         if (a < b) and (c < d):
#             # hasBigger = True
#             if (wi*hi > ws*hs):
#                 hasBigger = True
#                 alreadyHasBigger.append(k)
#                 break
#                 # print(ws*hs, wi*hi, hulls[i], hulls[k])
#         # if xs >= xi and xs <= xi+wi and ys >= yi and ys <= yi+hi:
#         #     hasBigger = True
#         # if xs + ws  >= xi and xs + ws <= xi+wi and ys +hs >= yi and ys+hs <= yi+hi:
#         #     hasBigger = True
#     if not hasBigger:
#         res.append(hulls[i])
# print(len(res))
# print(res)
# hulls = res



# cv2.polylines(vis, hulls, 1, (0, 255, 0))

# cv2.imshow('img', vis)

# cv2.waitKey(0)

copyImg = img.copy()

i = 0
[cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), cv2.FILLED) for x, y, w, h in hulls]
# for contour in hulls:
#     x, y, w, h = contour
#     # newimg = img[x : x+w, y:y+h]
#     # area = cv2.minAreaRect(contour)
#     # box. = cv2.boxPoints(area)  # поиск четырех вершин прямоугольника
#     # box = np.int0(box)  # округление координат
#     # cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), cv2.FILLED)


thresh = cv2.inRange(img, (0,0, 255), (0,0, 255))


reg2, _ = mser.detectRegions(thresh)
rectangles = [cv2.boundingRect(p) for p in reg2]
print('rects',len(rectangles))
print('reg', len(reg2))

trainData = []
number = 0
rectangles = sorted(rectangles, key=lambda key: key[0]+key[1]*10000)
for contour in rectangles:
    x, y, w, h = contour
    if w*h < 3*13:
        continue
    imageNumber = gray[y:y + h, x: x + w]
    cv2.imwrite(os.path.join(curFolder, 'tmp/item') + str(number) + ".png",
                cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA))
    imageNumber = np.array(cv2.resize(imageNumber, (17, 17), interpolation=cv2.INTER_AREA)).reshape(
        17 * 17, -1)

    number += 1
    trainData += [np.array(imageNumber, dtype=np.float32)]

print(len(trainData))
# cv2.imshow("t", thresh)
# cv2.waitKey(0)