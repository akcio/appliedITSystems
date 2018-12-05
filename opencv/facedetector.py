import cv2

face_cascade = cv2.CascadeClassifier('trainset/haarcascade_frontalface_default.xml')

img = cv2.imread('trainset/yalefaces.png')

faces = face_cascade.detectMultiScale(img, scaleFactor=6.2)

print(len(faces))
imgNum = 0
faces = sorted(faces ,key=lambda k: k[0] + k[1]*10000)
for (x,y,w,h) in faces:
    tmpImage = img[y:y+h, x:x+w]
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imwrite("tmp/" + str(imgNum) + '.png', tmpImage)
    imgNum += 1
cv2.imwrite("tmp/faces.png", img)
cv2.waitKey(0)