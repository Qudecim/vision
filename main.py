import cv2
import numpy as np
import video

if __name__ == '__main__':
    def callback(*arg):
        print (arg)

cv2.namedWindow( "result" )

cap = video.create_capture(0)
hsv_min = np.array((51, 87, 61), np.uint8)
hsv_max = np.array((132, 241, 180), np.uint8)

color_yellow = (0,255,255)


while True:
    flag, img = cap.read()
    inverted = 255 - img.copy()
    img = cv2.flip(img,1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    contours = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    moments = cv2.moments(thresh, 1)
    
    #moments = cv2.moments(cnt)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 5, color_yellow, 2)
        cv2.putText(img, "%d-%d" % (x,y), (x+10,y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
        x,y,w,h = cv2.boundingRect(cnt)


    cv2.imshow('result', img)
 
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()