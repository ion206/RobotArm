from apis import geminiAPI as api
import time
from robotControl import robotController as RC
from robotControl import inverseKinematics as IK

RC.init()
armVals = [160,45,90,60,0]
RC.updateArm(armVals.copy())
command = input("Enter Command: ")
row = api.sendCommand(command)
print(row)
for i in range(len(row)):
    print(str(row[i]['x']) + " " + str(row[i]['y']) + " " + str(row[i]['z']) + " " + str(row[i]['delay']))
    armVals = IK.getAngs(row[i]['x'],row[i]['y'], row[i]['z']+25, 100, 125)
    RC.updateArm(armVals.copy())
    time.sleep(row[i]['delay'])
RC.release()
RC.close()
print("End")