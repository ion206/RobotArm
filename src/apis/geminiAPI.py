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
    
    prompt = f"""I have a robotic arm with a claw that I need you to send commands to by taking
    in commands and outputting an array of xyz coordinates performing those in JSON format with certain delays(seconds) in between

    I have also given you an image. the top left qrcode is 0,0 and the more left is higher x values while down is higher y-values


    EVERYTHING IS IN MM
    the robot will move to your xyz position and the claw will face down ready to pick up an object
    reset position = (210, 200, 40)
    pick up height is 0
    always stay above z=40 unless dropping or picking
    any point which has x<300 AND y< 150 is off limit
    move the z=60 before traveling a long distance
    when dropping and picking, move to the point at z=40 first, then go down to the necessary height, then engage the claw
    drop height is 15
    you have to be smart about how you move objects, if you pick up an object and move it to where there anotehr object, they both will hit right. so you have manage that smartly
    reset at the end of the whole sequence as well
    when you want to have the claw closed, set claw value to 1, otherwise keep it at 0
    delays dont need to be longer than 5 seconds
    DONT PRINT ANYTHING OTHER THAN THE JSON, not a single word
    only put ints, not expression as values
    Example Command format in JSON:
    {{
        "x": 250,
        "y": 10,
        "z": 0,
        "delay": 3,
        "claw" : 0
    }},
    object1 position = {str(object1)} object2 position = {str(object2)}
    Command: {command}"""

    with open('src/GeminiImage.jpg', 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            prompt
    ]
  )
    return processResponse(response.text)



    