import cv2


img = cv2.imread("WeldGapImages/Set 1/image0001.jpg")
save_file = r'WeldGapImages/ProcessedSet1/image0001.jpg'
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1)
# cv2.imshow(save_file,img)
# Setting parameter values
t_lower = 120 # Lower Threshold
t_upper = 255 # Upper threshold
# Applying the Canny Edge filter
edge = cv2.Canny(blurred_image, t_lower, t_upper,True)
# Saving the image
cv2.imwrite(save_file, edge)
# cv2.imshow('Edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()