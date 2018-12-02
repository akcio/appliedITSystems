import cv2
import numpy as np


# def sort_contours(cnts, method="left-to-right"):
#      # initialize the reverse flag and sort index
#      reverse = False
#      i = 0
#
#      # handle if we need to sort in reverse
#      if method == "right-to-left" or method == "bottom-to-top":
#           reverse = True
#
#      # handle if we are sorting against the y-coordinate rather than
#      # the x-coordinate of the bounding box
#      if method == "top-to-bottom" or method == "bottom-to-top":
#           i = 1
#
#      # construct the list of bounding boxes and sort them from top to
#      # bottom
#      boundingBoxes = [cv2.boundingRect(c) for c in cnts]
#      (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
#                                          key=lambda b: b[1][i], reverse=reverse))
#
#      # return the list of sorted contours and bounding boxes
#      return (cnts, boundingBoxes)
#
# img = cv2.imread('test5.png')
#
img = cv2.imread('trainset/digits.png')
# ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
# ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
# refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# # refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
# refCnts = refCnts[1]
# refCnts = sort_contours(refCnts, method="left-to-right")[0]
# digits = {}
#
# for (i, c) in enumerate(refCnts):
# 	# compute the bounding box for the digit, extract it, and resize
# 	# it to a fixed size
# 	(x, y, w, h) = cv2.boundingRect(c)
# 	roi = ref[y:y + h, x:x + w]
# 	roi = cv2.resize(roi, (57, 88))
#
# 	# update the digits dictionary, mapping the digit name to the ROI
# 	digits[i] = roi
#
# print(len(digits))
#
#
#
# exit(0)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mser = cv2.MSER_create()
regions, _ = mser.detectRegions(imgGray)

hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
print(hulls)

mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)

for contour in hulls:
    cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

cv2.imshow('img',mask)
cv2.waitKey(0)
exit(0)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
contours,hierarchy = cv2.findContours(img_gray,2,1)
cnt = contours[0]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)
for i in range(defects.shape[0]):
     s,e,f,d = defects[i,0]
     start = tuple(cnt[s][0])
     end = tuple(cnt[e][0])
     far = tuple(cnt[f][0])
     cv2.line(img,start,end,[0,255,0],2)
     cv2.circle(img,far,5,[0,0,255],-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()