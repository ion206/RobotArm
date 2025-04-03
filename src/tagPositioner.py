import cv2
import numpy as np

# Camera Calibration Parameters (from your camera calibration)
camera_matrix = np.array([[4602.25871, 0, 2249.91543],
                          [0, 4619.42349, 1583.36098],
                          [0, 0, 1]], dtype=np.float32)

# Distortion Coefficients
dist_coeffs = np.array([0.06408, -0.13626, -0.00030, 0.00012, -0.16315], dtype=np.float32)

# Define marker side length in meters (adjust if needed)
marker_length = 0.048  # 5 cm marker

# Define dictionary and detector parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())

# Define 3D marker corner positions relative to marker center
objp = np.array([[-marker_length / 2,  marker_length / 2, 0],
                 [ marker_length / 2,  marker_length / 2, 0],
                 [ marker_length / 2, -marker_length / 2, 0],
                 [-marker_length / 2, -marker_length / 2, 0]], dtype=np.float32)


# Start video capture

def getpos(frame):
    marker0pos, marker0rot,marker1pos, marker1rot,marker2pos, marker2rot,marker3pos, marker3rot, marker4pos, marker4rot = np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0])
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Draw detected markers
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Estimate pose for each marker
        for i in range(len(ids)):
            ret_pnp, rvec, tvec = cv2.solvePnP(objp, corners[i].reshape((4, 2)), 
                                            camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_IPPE_SQUARE)
            if ret_pnp:
                # Draw the axis on the marker
                cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.03)
                if ids[i][0] == 0:
                    marker0pos = tvec.flatten()
                    marker0rot = rvec.flatten()
                elif ids[i][0] == 1:
                    marker1pos = tvec.flatten()
                    marker1rot = rvec.flatten()
                elif ids[i][0] == 2:
                    marker2pos = tvec.flatten()
                    marker2rot = rvec.flatten()
                elif ids[i][0] == 3:
                    marker3pos = tvec.flatten()
                    marker3rot = rvec.flatten()
                elif ids[i][0] == 4:
                    marker4pos = tvec.flatten()
                    marker4rot = rvec.flatten()
    #print("Marker positions:", marker0pos, marker1pos, marker2pos, marker3pos, marker4pos)
    if marker4pos[0] != 0:
        imagepoints = [
            (marker0pos[0],marker0pos[1]),
            (marker1pos[0],marker1pos[1]),
            (marker2pos[0],marker2pos[1]),
            (marker3pos[0],marker3pos[1])
        ]
        mappoints = [
            (480,390),
            (0,390),
            (480,0),
            (0,0)
        ]

        testpoint = [(marker4pos[0], marker4pos[1])]
        mapped = map_desk_coordinates(imagepoints, mappoints, testpoint)
        return int(mapped[0]), int(mapped[1])
    print("Marker 4 location not found")
    return (-1,-1) #Marker Not Found

def map_desk_coordinates(image_points, desk_points, test_points):
    """
    Compute a homography that maps from image coords -> desk coords.
    Then transform the test_points from image coords -> desk coords.
    """
    # Convert to float32 for OpenCV
    img_pts = np.array(image_points, dtype=np.float32)  # Shape (N,2)
    desk_pts = np.array(desk_points, dtype=np.float32)  # Shape (N,2)
    test_pts = np.array(test_points, dtype=np.float32)  # Shape (M,2)

    # Ensure we have at least 4 corresponding points
    if img_pts.shape != desk_pts.shape or img_pts.shape[0] < 4:
        raise ValueError(f"Mismatch in point shapes or not enough points: "
                         f"image_points={img_pts.shape}, desk_points={desk_pts.shape}")

    # Find the homography
    H, mask = cv2.findHomography(img_pts, desk_pts, cv2.RANSAC, 5.0)
    
    if H is None:
        raise RuntimeError("Homography calculation failed. Check that the points are correct.")

    # Reshape test points properly to (N,1,2)
    test_pts = test_pts.reshape(-1, 1, 2)  # Convert (M,2) -> (M,1,2)

    # Apply the homography
    desk_mapped = cv2.perspectiveTransform(test_pts, H)

    return desk_mapped.squeeze()  # Output as (M,2)

