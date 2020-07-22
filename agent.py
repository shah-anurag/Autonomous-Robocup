import time
import behaviour as beh
import os

class Agent:
    def __init__(self, id_, b, x, y):
    	self.id = id_
    	self.b = b
    	self.x = x
    	self.y = y
    
    def get_coordinates(self):
        return self.x, self.y
    
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        x,y = self.x, self.y
        self.x, self.y = self.b.next(self.x, self.y)
        print('Agent', self.id, 'moved to ', self.x, self.y, 'from', x, y)

    def run(self):
    	while True:
    		try:
    			x,y = self.x, self.y
	    		self.x, self.y = self.b.next(self.x, self.y)
	    		print('Agent', self.id, 'moved to ', self.x, self.y, 'from', x, y)
	    		time.sleep(5)
	    	except Exception as e:
	    		print("Killed process for agent", self.id, "due to reason", e)
	    		return

# player = Agent(beh.Behaviour(), 11, 22)
