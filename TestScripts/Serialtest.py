import serial
import time

def main():
    # Set your serial port and baud rate (match Arduino's Serial.begin(9600))
    port = '/dev/cu.usbmodem1301'  # e.g., on Linux; change to 'COM3' on Windows if needed
    baud_rate = 11500

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
    except Exception as e:
        print("Error opening serial port: ", e)
        return

    # Wait for the serial connection to initialize
    time.sleep(2)

    # Initialize servo angles for servos 1-4 with default values (e.g., 90°)
    servo_angles = [150, 90, 90, 90]
    print("Current servo angles:", servo_angles)
    print("Enter a servo number (1-4) and a new angle (0-180) separated by a space, or type 'exit' to quit.")

    while True:
        user_input = input("Servo and angle (e.g., 2 150): ")
        if user_input.lower().strip() == 'exit':
            break

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid format. Please enter a servo number and an angle separated by a space.")
            continue

        try:
            servo_num = int(parts[0])
            angle = int(parts[1])
        except ValueError:
            print("Please enter numeric values.")
            continue

        if not (1 <= servo_num <= 4):
            print("Servo number must be between 1 and 4.")
            continue
        ##if not (0 <= angle <= 180):
         ##   print("Angle must be between 0 and 180.")
         ##   continue

        # Update the selected servo's angle
        servo_angles[servo_num - 1] = angle

        # Create a comma-separated message and append a newline
        msg = "{},{},{},{}\n".format(*servo_angles)
        ser.write(msg.encode())
        print("Sent:", msg.strip())
        print("Updated servo angles:", servo_angles)

    ser.close()
    print("Serial connection closed.")

if __name__ == '__main__':
    main()
