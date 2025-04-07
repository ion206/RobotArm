import robotController as RC

RC.init()
values = [150,90,90,90,0]
RC.updateArm(values)
while True:
    servo = input("Enter Servo #: ")
    angle = input("Enter requested angle: ")
    if (servo == "q" or angle == "q"):
        break
    values[int(servo)] = int(angle)
    print(values)
    print(RC.updateArm(values.copy()))

RC.close()
