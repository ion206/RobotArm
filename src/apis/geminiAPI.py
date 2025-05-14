from google import genai
import json
import cv2
import configparser
import base64
from google.genai import types
parser = configparser.ConfigParser()
parser.read("src/config.cfg")

key = parser['API'].get('APIKey')

client = genai.Client(api_key=key)
def processResponse(txt):
    print(txt)
    txt = txt[7:-3]
    y = json.loads(txt)
    return y


def sendCommand(command, object1, object2, num):
    
    prompt = f"""
I have a robotic arm with a claw that moves based on given commands. Output an array of xyz coordinates in JSON format with delays between movements. All measurements are in mm.

- The arm starts at position (210, 200, 40).
- Avoid any points where x < 300 AND y < 150 for temporary placement. temp points should be very far from other points, just for accuracy and repeatability
- To avoid obstacles, always move to at least z = 120 before traveling xy distances and after picking somthing up.
- When picking up or dropping: first move to 40mm above the target position, then descend to the desired height, and engage/release the claw at that position.
- To close the claw, set "claw" to 1; to open, set "claw" to 0.
- Blocks are 60mm tall(for stacking purposes), need to picked up and dropped off the ground from z=40, each with a colored stripe for identification
- to place a block on top of antoher block you need to drop at z=70mm
- Keep in mind the blocks' colors and ensure proper handling when stacking.
- The image's top-left QR code is at (0,0). As you move left, x increases, and as you move down, y increases.
- Do not place blocks in regions where x < 300 AND y < 150 (temporary placement is restricted here).
- Always reset to position (210, 200, 40) at the end of the sequence.
- Do not print anything except the JSON, formatted like this:
[ x: int, y: int, z: int, delay: int, claw: int ]
  The delay is in seconds and between commands should not exceed 5 seconds.
    Red Block position = {str(object1)} Green Block position = {str(object2)}
    Command: {command}"""

    with open('src/GeminiImage.jpg', 'rb') as f:
        image_bytes = f.read()
#gemini-2.0-flash
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            prompt
    ]
  )
    return processResponse(response.text)



    