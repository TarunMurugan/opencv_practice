import cv2
import numpy as np
def nothing(x):
    pass

cap=cv2.VideoCapture("tennis6.avi")
ret,frame1=cap.read()
ret,frame2=cap.read()
# cv2.namedWindow("Tracking")
# cv2.createTrackbar("LH","Tracking",0,255,nothing)
# cv2.createTrackbar("LS","Tracking",0,255,nothing)
# cv2.createTrackbar("LV","Tracking",0,255,nothing)
# cv2.createTrackbar("UH","Tracking",255,255,nothing)
# cv2.createTrackbar("US","Tracking",255,255,nothing)
# cv2.createTrackbar("UV","Tracking",255,255,nothing)
graph=[]
while cap.isOpened():
    xaxis=frame1.shape[1]
    yaxis=frame1.shape[0]
    xaxisdiff=int(xaxis/9)
    yaxisdiff=int(yaxis/10)

    frame1a=frame1.copy()[yaxisdiff:yaxis-yaxisdiff,xaxisdiff:xaxis-xaxisdiff]
    frame2a=frame2.copy()[yaxisdiff:yaxis-yaxisdiff,xaxisdiff:xaxis-xaxisdiff]
    diff=cv2.absdiff(frame1a,frame2a)
    gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    DILATED=cv2.dilate(thresh,None,iterations=3)
    contours,_=cv2.findContours(DILATED,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if (cv2.contourArea(contour)<700 and cv2.contourArea(contour)>75) or cv2.contourArea(contour)>10000:
            continue
        cv2.rectangle(frame1a,(x,y),(x+w,y+h),(0,0,0),-1)
    frame1b=frame1.copy()[yaxisdiff:yaxis-yaxisdiff,xaxisdiff:xaxis-xaxisdiff]
    frame2b=frame2.copy()[yaxisdiff:yaxis-yaxisdiff,xaxisdiff:xaxis-xaxisdiff]
    diff=cv2.absdiff(frame1b,frame2b)
    hsv=cv2.cvtColor(diff,cv2.COLOR_BGR2HSV)
   
    # # l_h=cv2.getTrackbarPos("LH","Tracking")
    # # l_s=cv2.getTrackbarPos("LS","Tracking")
    # # l_v=cv2.getTrackbarPos("LV","Tracking")
    # # u_h=cv2.getTrackbarPos("UH","Tracking")
    # # u_s=cv2.getTrackbarPos("US","Tracking")
    # # u_v=cv2.getTrackbarPos("UV","Tracking")
   
    # # l_b=np.array([l_h,l_s,l_v])
    # # u_b=np.array([u_h,u_s,u_v])

    l_b=np.array([33,48,26])
    u_b=np.array([45,244,135])

    mask=cv2.inRange(hsv,l_b,u_b)
    res=cv2.bitwise_and(diff,diff,mask=mask)
    frameres=cv2.bitwise_and(frame1a,res)
    gray=cv2.cvtColor(frameres,cv2.COLOR_HSV2BGR)
    gray=cv2.cvtColor(frameres,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    DILATED=cv2.dilate(thresh,None,iterations=3)
    contours,_=cv2.findContours(DILATED,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour)>700:
            continue
        graph.append(list([x,y]))
        cv2.rectangle(frame1,(x+xaxisdiff,y+yaxisdiff),(x+xaxisdiff+w,y+yaxisdiff+h),(0,255,0),2)
    
    # for i in graph:
    #     img=cv2.circle(frame1,(int(i[0]),int(i[1])),2,(0,255,0),-1)
    # cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    cv2.imshow("feed",res)
    frame1=frame2
    ret,frame2=cap.read()

    if cv2.waitKey(40)==27:
        break
cv2.destroyAllWindows()
cap.release()