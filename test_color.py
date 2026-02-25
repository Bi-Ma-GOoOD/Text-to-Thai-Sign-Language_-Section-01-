import cv2
import numpy as np

img = np.full((500, 500, 3),255, dtype = np.uint8)
img = cv2.circle(img, (50, 50), 20, (219, 198, 156), -1)
img = cv2.circle(img, (350, 350), 20, (219, 198, 156), -1)
img = cv2.line(img, (50, 50), (350, 350), (255, 255, 255), 8)

cv2.imshow("Canvas Line", img)
cv2.waitKey(0)
cv2.destroyAllWindows()