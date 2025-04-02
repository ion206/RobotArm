import cv2
import numpy as np

# Load the ArUco dictionary (Updated syntax for OpenCV 4.7+)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Generate and save marker
marker_size = 200  # 200x200 pixels
marker_img = np.zeros((marker_size, marker_size, 1), dtype=np.uint8)
cv2.aruco.generateImageMarker(aruco_dict, 3, marker_size, marker_img, 1)

cv2.imwrite("marker_3.png", marker_img)
print("Marker saved as marker_3.png")