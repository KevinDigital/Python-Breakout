# models.py
# SHELLY ZHANG (SXZ2), KEVIN LI (KL553)
# DECEMBER 11, 2015
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as
    move it left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, xvalue):
        GRectangle.__init__(self, x = xvalue, y = PADDLE_OFFSET,
               width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
               fillcolor = colormodel.BLACK)

    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    
    def movePaddle(self, value):
        #create variables for the x coordinate
        if value.is_key_down('left'):
            self.x = max(self.x - 10, PADDLE_WIDTH/2)
        if value.is_key_down('right'):
            self.x = min(self.x + 10, GAME_WIDTH - PADDLE_WIDTH/2)
        
    def collides(self, ball):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        assert isinstance(ball, Ball)
        
        if self.contains(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS) or\
        self.contains(ball.x + BALL_RADIUS, ball.y - BALL_RADIUS) == True:
            ball._vy = ball._vy * -1
            return True
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may
    wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, xcoordinate, ycoordinate, row_number):
        """Creates a brick"""
        
        GRectangle.__init__(self, x = BRICK_WIDTH/2 + xcoordinate,
                            y = GAME_HEIGHT - BRICK_Y_OFFSET-BRICK_HEIGHT/2 - ycoordinate,
                            width = BRICK_WIDTH, height = BRICK_HEIGHT,
                            fillcolor = COLOR_LIST[row_number%10/2])
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self, ball):
        """Returns: True if the ball collides with this brick
            
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
    
        assert isinstance(ball, Ball)
        
        if ball.top == self.bottom and self.contains(ball.x - BALL_RADIUS,
                                                     ball.y - BALL_RADIUS) or\
        self.contains(ball.x + BALL_RADIUS, ball.y - BALL_RADIUS):
            ball._vy = -ball._vy
            return True
        if ball.bottom == self.top and self.contains(ball.x - BALL_RADIUS,
                                                     ball.y + BALL_RADIUS) or\
        self.contains(ball.x + BALL_RADIUS, ball.y + BALL_RADIUS):
            ball._vy = -ball._vy
            return True
        if ball.left == self.right and self.contains(ball.x + BALL_RADIUS,
                                                     ball.y - BALL_RADIUS) or\
        self.contains(ball.x + BALL_RADIUS, ball.y + BALL_RADIUS):
            ball._vx = -ball._vx
            return True
        if ball.right == self.left and self.contains(ball.x - BALL_RADIUS,
                                                     ball.y - BALL_RADIUS) or\
        self.contains(ball.x - BALL_RADIUS, ball.y + BALL_RADIUS):
            ball._vx = -ball._vx
            return True
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getXVelocity(self):
        return self._vx
    
    def getYVelocity(self):
        return self._vy
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self, xvalue, yvalue):
        GEllipse.__init__(self,x = xvalue, y = yvalue, width = BALL_DIAMETER,
                          height = BALL_DIAMETER,
                 fillcolor= colormodel.RED)
        self._vx = random.uniform(1.0, 5.0)
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
        
    def moveBall(self):
        self.x = self.x + self.getXVelocity()
        self.y = self.y + self.getYVelocity()
    
    def bounceBall(self):
        """Changes the direction the ball is moving when it hits the walls"""
        
        if self._vy > 0 and self.top >= GAME_HEIGHT:
            self._vy = self._vy * -1
        #if self._vy < 0 and self.bottom <= 0 + PADDLE_HEIGHT:
         #   self._vy = self._vy * -1
        if self._vx < 0 and self.left <= 0:
            self._vx = self._vx * -1
        if self._vx > 0 and self.right >= GAME_WIDTH:
            self._vx = self._vx * -1
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def increasespeed(self):
        """Increases the ball's speed
        by 50% every 7 times the ball hits the paddle"""
        
        counter = 0
        self._vx = self._vx*1.5

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE


    
        