# 🤖 3-Axis Vision-Guided Robotic Arm with ArUco Markers and Gemini-Based Spatial Intelligence

## **By: Ayan Syed**

A low-cost, modular 3-axis robotic arm with an integrated vision system that detects ArUco markers for intelligent object manipulation. Designed for personal research, prototyping, and education, this project features end-to-end integration of computer vision, AI path-planning, inverse kinematics, and embedded hardware.



https://github.com/user-attachments/assets/65d640ed-7b3e-4d83-9f5d-62e66aa19349





---

## 📦 Features
- ArUco marker-based block detection and localization with planar Homography
- Inverse kinematics with collision-aware motion planning using URDF and IKPy
- Serial communication between Host computer and Arduino robot controller
- Supports mixed-size markers and elevated block detection
- JSON-based command execution for flexible control, with AI-generated point seqeuences
- Designed for minimal cost(all hardware < $45) and maximum modifiability. Fully Open Source

---


https://github.com/user-attachments/assets/61cfe404-c097-4321-8dbf-4411ba208413

# 🧠 How It Works
Vision: Camera detects ArUco tags to localize block positions.

Planning: Positions, Scene Image, and user command are passed into Google Gemini LLM using a carefully constructed prompt. This outputs a set of points the robot can follow to acheive the task. This is done in the APIArm.py Script

IK + Control: getAngs() calculates angles using IKPy and the robots URDF File → serial → Arduino

Motion: Arm executes pickup/drop sequence with configurable delays.

---

## 🧠 Software Architecture

### 🧭 Vision System
- Uses OpenCV’s `cv2.aruco` module to detect markers
- Performs planar homography mapping to extract 2D positions
- Detects marker height for Z-value estimation
- Supports mixed-size markers
- I created special cubes that can be easily localized and manipulated

### 🦾 Inverse Kinematics
- Uses `ikpy` with URDF-defined kinematic chain
- Computes joint angles for any reachable XYZ target
- Ensures Z-lift before lateral motion to avoid collisions

### AI Integration
- Uses Google Gemini Web API - Gemini-Flash-2.0 LLM Model
- Custom prompt used to describe context and requirements
- Wrote a position/movement sequencer for reliable and consistent robot actions

### 🔌 Control Logic
- Commands are passed via USB serial (PySerial)
- Arduino handles servo control using PWM signals
- Python side maps world coordinates to joint angles and sends instructions

---


![Screenshot 2025-05-06 at 11 32 23 PM](https://github.com/user-attachments/assets/e785ef03-147a-4318-81a5-10357f683599)


## 🛠️ Hardware
CAD was done in Fusion 360 & Onshape
3D Printed on Bambu Lab A1 Mini

| Component              | Description                                   |
|------------------------|-----------------------------------------------|
| **Robotic Arm**        | 3-axis, 3D-printed, modular mechanical design |
| **Gripper**            | Parallel claw gripper                         |
| **Servos**             | 5x SG90 / MG90S motors                        |
| **Controller**         | Arduino Uno                                   |
| **Host Computer**    | Any Modern Computer
| **Camera**             | USB webcam mounted top-down                   |
| **Power Supply**       | 3.5V Lipo Battery, 2A–5A external line        |
| **Workspace**          | Flat surface with ArUco markers               |

All hardware is easily accessible. For a full B.O.M. pls reach out

---

## 🧪 Technologies Used

- **Languages**: Python, C++, Assembly (for low-level control)
- **Libraries**:
  - OpenCV
  - ikpy
  - pyserial
- **Mechanical Design**: Fusion 360
- **Fabrication**: 3D printing, CNC
- **Future Support**: ROS2, MoveIt2

---


https://github.com/user-attachments/assets/c0df00d9-8648-4762-a208-6bb8f0a5d23d

---
## 📁 File Structure
![image](https://github.com/user-attachments/assets/4304e204-74ed-4cf2-b96c-a7fc33a3d8d4)


---

## 🧾 JSON Command Format
[ x: int, y: int, z: int, delay: int, claw: int ]
All coordinates in millimeters

To run the code, you will need a config file, that can be parsed by configpaser by Python, 
Here is the format:

[Arm]
shoulderArm = 120
elbowArm = 100
wristArm = 110
servoResets = 150, 90, 0 , 90, 90
armXpos = 210
armYpos = 50
  
[API]
APIKey = XXX

[Serial]
port = XXX
baudrate = 115200




