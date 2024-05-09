import cv2
import numpy as np
import glob
import os


folderDir = "WeldGapImages/Set 1/"
file_extension = "*.jpg"

processedDir = "Processed/Set 1/"
imterimDir = "Interim/Set 1/"

png_files = glob.glob(os.path.join(folderDir, file_extension))
png_files = [path.replace("\\", "/") for path in png_files]

WeldGapData = []
for file in png_files:


    y = 70

    img = cv2.imread(file)
    y1, x1 = img.shape[:2]
    img = img[0:140, 850:1150]
    save_file = os.path.join(processedDir, os.path.basename(file))
    imterim_file = os.path.join(imterimDir, os.path.basename(file))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    gray_image = cv2.filter2D(gray_image, -1, kernel2)
    blurred_image = cv2.GaussianBlur(gray_image, (15, 15), 1)

    
    
    # cv2.imshow(save_file,img)
    # Setting parameter values
    t_lower = 240 # Lower Threshold
    t_upper = 255 # Upper threshold


    # Applying the Canny Edge filter
    # edge = cv2.Canny(blurred_image, t_lower, t_upper)

    #apply sobel filter
    grad_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
    afterSobel = cv2.magnitude(grad_x, grad_y)
    afterSobel_uint8 = cv2.convertScaleAbs(afterSobel)
    afterSobel_uint8_blurred = cv2.GaussianBlur(afterSobel_uint8, (35, 35), 1)
    #edge = cv2.GaussianBlur(afterSobel_uint8, (15, 15), 1)

    #use edge enhancement method
    _, edges_thresh = cv2.threshold(afterSobel_uint8_blurred, 125, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges_thresh, kernel, iterations=1)
    edge = cv2.erode(edges_dilated, kernel, iterations=1)

    

    row_of_pixels = edge[y, :]
    x_coordinates = np.where(row_of_pixels >= 120)[0]

    

    
    loop = True

    while loop:
        if(len(x_coordinates) > 6):
            edge = cv2.erode(edge, kernel, iterations=1)
            row_of_pixels = edge[y, :]
            x_coordinates = np.where(row_of_pixels >= 120)[0]
        else:
           loop = False

    # if there is no line detected, extend each white area 1 pixel up/down until detects line
    kernel3 = np.array([[1], [1], [1]])
    loop = True

    while loop:
      if(len(x_coordinates) > 0):
        loop = False
      else:
        edge = cv2.filter2D(edge, -1, kernel3)
        row_of_pixels = edge[y, :]
        x_coordinates = np.where(row_of_pixels >= 120)[0]

    

    
    

    if(len(x_coordinates) > 0):

        if x_coordinates[-1] - x_coordinates[0] > 11:
            valid = 0
            print(x_coordinates[-1] - x_coordinates[0])
        else:
            valid = 1

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

        WeldGapData.append([os.path.basename(file), int(np.mean(x_coordinates)), valid])
    else:
        WeldGapData.append([os.path.basename(file), -1, 0])





    # Saving the image
    cv2.imwrite(save_file, img)
    cv2.imwrite(imterim_file, edge)
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