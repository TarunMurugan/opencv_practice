import cv2
import numpy as np

img1=np.zeros((512,512,3),np.uint8)
img1=cv2.rectangle(img1,(200,0),(300,100),(97,100,208),-1)
img2=cv2.imread("lena.jpg")
print(img2.shape)


# bit=cv2.bitwise_and(img1,img2)
# bit=cv2.bitwise_or(img1,img2)
bit=cv2.bitwise_and(img1,img2)
# bit=cv2.bitwise_not(img1)

cv2.imshow("img1",img1)
cv2.imshow("img2",img2)
cv2.imshow("bit",bit)

cv2.waitKey(0)
cv2.destroyAllWindows()