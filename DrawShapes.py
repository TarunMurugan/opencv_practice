import numpy as np
import cv2
img=cv2.imread("lena.jpg",1)
#img=np.zeros([512,512,3],np.uint8)
img =cv2.line(img,(0,0),(200,200),(255,0,0), 5)
img =cv2.arrowedLine(img,(500,500),(400,400),(25,200,150), 5)
img =cv2.rectangle(img,(200,200),(400,400),(255,255,255),3)
img=cv2.circle(img,(300,300),100,(69,42,99),2)
font=cv2.FONT_ITALIC
img=cv2.putText(img,"practice",(255,255),font,1,(255,255,255),2,cv2.LINE_4)

cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()