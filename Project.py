import cv2


img = cv2.imread("WeldGapImages/Set 2/image0200.jpg")
save_file = r'WeldGapImages/ProcessedSet1/image0001.jpg'
cv2.imshow(save_file,img)
# Setting parameter values
t_lower = 120 # Lower Threshold
t_upper = 255 # Upper threshold
# Applying the Canny Edge filter
edge = cv2.Canny(img, t_lower, t_upper)
# Saving the image
cv2.imwrite(save_file, edge)
cv2.imshow('Edge', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()