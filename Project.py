import cv2
import numpy as np
import glob
import os


folderDir = "WeldGapImages/Set 1/"
file_extension = "*.jpg"

processedDir = "Processed/Set 1/"

png_files = glob.glob(os.path.join(folderDir, file_extension))
png_files = [path.replace("\\", "/") for path in png_files]

WeldGapData = []
for file in png_files:


    y = 70

    img = cv2.imread(file)
    save_file = os.path.join(processedDir, os.path.basename(file))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1)
    # cv2.imshow(save_file,img)
    # Setting parameter values
    t_lower = 30 # Lower Threshold
    t_upper = 255 # Upper threshold
    # Applying the Canny Edge filter
    edge = cv2.Canny(blurred_image, t_lower, t_upper)

    row_of_pixels = edge[y, :]
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

        WeldGapData.append([os.path.basename(file), int(np.mean(x_coordinates)), 1])
    else:
        WeldGapData.append([os.path.basename(file), -1, 0])





    # Saving the image
    cv2.imwrite(save_file, img)
    # cv2.imshow('Edge', edge)
    # cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



import csv

csv_file = "WeldGapPositions.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["File Name", "Position", "Valid"])
    writer.writerows(WeldGapData)