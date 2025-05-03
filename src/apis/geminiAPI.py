from google import genai
import json
import configparser
parser = configparser.ConfigParser()
parser.read("src/config.cfg")

key = parser['API'].get('APIKey')
def processResponse(txt):
    txt = txt[7:-3]
    y = json.loads(txt)
    return y

def sendCommand(command):
    client = genai.Client(api_key=key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=("""I have a robotic arm that I need you to impersonate by taking 
        in commands and outputting an array of xyz coordinates performing those in JSON format with certain delays in between

        idle position is (250, 30, 100)
    
        Context: The robot is centered at world coordinates x=250mm, y=-10mm, z=0mm. right is towards lesser x values, z is height. Shoulder Arm is 120mm long, Elbow arm is 100mm long. Please dont print anything other than the JSON.
        EVERYTHING IS IN MM
        distance from base of the robot cannot exceed a bubble of radius 230mm
        There are three servos controlling this, a base rotation servo, a shoulder servo, and an elbow joint. 
        try not to make the motions too jerky
        Example Command format in JSON:
        {
            "x": 250,
            "y": -10,
            "z": 0,
            "delay": 3
        }, 
        
        Command:""" + command)
    )
    return processResponse(response.text)



    