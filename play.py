# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DECEMBER 11, 2015
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout
App. 
Instances of Play represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model
objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is won,
    it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make
    a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want toaccess an attribute in class Breakout. It is okay if you do, but you
    MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any
    attribute that you need to access in Breakout.  Only add the getters and
    setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    may want to add new objects on the screen (e.g power-ups).  If you make
    changes, please listthe changes with the invariants.
    
        _sound  [Sound, makes a random sound when the ball hits a brick]
        _counter    [int, counts the number of times the ball hits the paddle]
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
        
    def getTries(self):
        return self._tries
    
    def setTries(self, value):
        assert type(value) == int and value >= 0
        self._tries = value
        
    def getCounter(self):
        return self._counter
    
    def setCounter(self, value):
        assert type(value) == int and value >= 0
        self._counter = value
  
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer to create the paddles and bricks and also the ball
        (the ball doesn't get drawn here though). Also sets the number of tries
        left to 3"""
        
        self._bricks = []
        xcoordinate = BRICK_SEP_H/2
        for i in range(BRICKS_IN_ROW):
            ycoordinate = 0
            for j in range(BRICK_ROWS):
                abrick = Brick(xcoordinate, ycoordinate, j)
                ycoordinate = ycoordinate + BRICK_HEIGHT + BRICK_SEP_V
                self._bricks.append(abrick)
            xcoordinate = xcoordinate + BRICK_SEP_H + BRICK_WIDTH
            
        self._paddle = Paddle(GAME_WIDTH/2)
        self._ball = Ball(GAME_WIDTH/2, GAME_HEIGHT/2)
        self.setTries(NUMBER_TURNS)
        self.setCounter(0)
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL

    def updateBall(self):
        """Method that moves the ball and bounces it off walls, the paddle, and
        the bricks. If the ball hits a brick, this method clears the brick.
        
        Additionally, this method increases the ball's speed every 7 times the
        ball hits the paddle
        """

        self._ball.moveBall()
        if self._paddle.collides(self._ball) == True:
            bounceSound = Sound('bounce.wav')
            bounceSound.play()
            self.setCounter(self._counter + 1)
            if self.getCounter() == 7:
                self._ball.increasespeed()
                self.setCounter(0)
        for b in self._bricks:
            if b.collides(self._ball) == True:
                bounceSound = Sound(random.choice(LIST_OF_SOUNDS))
                #generates a random sound
                self._bricks.remove(b)
                bounceSound.play()

    def updatePaddle(self, value):
        """Method that moves the paddle."""
        
        self._paddle.movePaddle(value)
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self,view):
        """Method that draws the bricks and paddle"""
        
        for b in self._bricks:
            b.draw(view)
        self._paddle.draw(view)
        
    def drawBall(self,view):
        """Method that draws the ball"""
        
        self._ball.draw(view)

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def bounceBall(self):
        """Method that bounces the ball if it hits the edges of the screen,
        calls function from Ball class in models
        """
        self._ball.bounceBall()

    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED)
    
    def life_lost(self):
        """Returns True if the paddle misses the ball and there are still tries
        remaining, False if there are no tries remaining.
        """
        
        if self._ball.bottom <= 0:
            self.setTries(self.getTries()-1)
            self._ball = Ball(GAME_WIDTH/2, GAME_HEIGHT/2)
            return True
        if self._tries == 0:
            return False
    
    def win(self):
        """Returns true if all of the bricks are cleared."""
        
        if len(self._bricks) == 0:
            return True
        
    
    