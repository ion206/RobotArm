class Marker:
    #ArUco Maker variables
    id = 0
    x = 0
    y = 0 
    rot = [0,0,0]

    multip = 100
    add = 0

    def __init__(self,id, pos, rot):
        self.id = id
        self.pos = pos
        self.rot = rot
        
    def __str__(self):
        return f"{self.id} at {self.x} , {self.y}"
    

    def updatePos(self, newPos): #Putting this here in case we want to add smoothing in the future (comp filter etc.)
        if newPos[0] != -1 and newPos[1] != -1: ##If position lost, ensuring that last known position saved
            self.x = newPos[0] 
            self.y = newPos[1]

    def updateRot(self, newRot):
        self.rot = newRot

