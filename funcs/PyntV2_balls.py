import numpy as np
from PyntV2_TwoD import TwoD
from guiFuncs import BALL_RADIUS
#-------------------- BALL IMPLEMENTATION CLASS---------------------------#

class Ball:
    #BALL_RADIUS = 15.0        # FOR ballS IN PIXELS
    def __init__(self,x,y):
         self.position = TwoD(x,y)
        
	 #--Picking up antenna--#
    def userPick (self, mouse_x, mouse_y):
        # distance between click and antenna position
        x = mouse_x - self.position.x;
        y = mouse_y - self.position.y;
		
        # Pythagoras for cacling distance between click and antenna cent
        distance = np.sqrt ((x*x) + (y*y));
		
        if (distance < BALL_RADIUS*1.1):
            return True
        else:
            return False
        
    #** Picking up antenna */
    def antwasPick (self, mouse_x, mouse_y):
        # distance between click and antenna position
        self.position.x=mouse_x
        self.position.y=mouse_y
        
    def colliding (self, other):
        if (self == other):
            return False;
        else:
            xd = self.position.x - other.position.x
            yd = self.position.y - other.position.y
            
            
            sumRadius = BALL_RADIUS
            sqrRadius = sumRadius * sumRadius
			
            distSqr = (xd * xd) + (yd * yd)
			
            if (distSqr <= sqrRadius):
                return True
            else:
                return False

#-----------------------------------------------------------------------#
