import cv2
import numpy as np

y = 70

img = cv2.imread("WeldGapImages/Set 3/image0307.jpg")
# img = cv2.imread("WeldGapImages/Set 2/image0200.jpg")
# img = cv2.imread("WeldGapImages/Set 1/image0001.jpg")
save_file = r'WeldGapImages/ProcessedSet1/image0001.jpg'
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1)
# cv2.imshow(save_file,img)
# Setting parameter values
t_lower = 100 # Lower Threshold
t_upper = 255 # Upper threshold
# Applying the Canny Edge filter
edge = cv2.Canny(blurred_image, t_lower, t_upper)

# Assuming 'edge' is your edge-detected image
row_of_pixels = edge[y, :]
# Find indices of white pixels (where pixel value is 255)
x_coordinates = np.where(row_of_pixels >= 120)[0]





if(len(x_coordinates) > 0):
    x_coordinate = int(np.mean(x_coordinates))
    print(x_coordinate)
    thickness = 5

    start_point = (0, y)  # Starting point of line (x, y)
    end_point = (x_coordinate-thickness, y)  # Ending point of line (x, y)


    color = (0,255, 0)

    cv2.line(img, start_point, end_point,  color, thickness)

    start_point_2 = (x_coordinate+thickness, y)
    end_point_2 = (img.shape[1], y)

    cv2.line(img, start_point_2, end_point_2, color, thickness)

    start_point_3 = (x_coordinate, y)
    end_point_3 = (x_coordinate, y)

    cv2.line(img, start_point_3, end_point_3, (0,95,255), thickness)


# Saving the image
cv2.imwrite(save_file, edge)
# cv2.imshow('Edge', edge)
cv2.imshow("result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()