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
    marker0pos = [0,0,0]
    marker0rot = [0,0,0]
    marker1pos = [0,0,0]
    marker1rot = [0,0,0]
    marker2pos = [0,0,0]
    marker2rot = [0,0,0]
    marker3pos = [0,0,0]
    marker3rot = [0,0,0]
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
    
    return [marker0pos,marker0rot,marker1pos,marker1rot,marker2pos,marker2rot,marker3pos,marker3rot]

        



