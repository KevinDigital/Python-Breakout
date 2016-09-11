# breakout.py
# SHELLY ZHANG (SXZ2), KEVIN LI (KL553)
# DECEMBER 11, 2015
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application.
There is no need for any any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the play module
or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle,
                ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for
    the method update().
    
    You may have more attributes if you wish (you might need an attribute to
    store any text messages you display on the screen). If you add new
    attributes, they need to be documented here.
    
        _mssg2  [GLabel or None if there is no message to display]
                 the currently active message
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    def getView(self):
        return self.view
    
    def getInput(self):
        return self.input
    
    def getState(self):
        return self._state
    
    def setState(self, state):
        assert type(state) == int and 0 <= state <= 5
        self._state = state
        
    def getGame(self):
        return self._game
    
    def setGame(self, value):
        assert isinstance(value, Play) or value is None
        self._game = value
    
    def getMssg(self):
        return self._mssg

    def setMssg(self, txt):
        assert type(txt) == str
        if self.getState == STATE_ACTIVE or self.getState() == STATE_COUNTDOWN:
            self._mssg = None
        else:
            self._mssg = GLabel(text = txt, font_size = 30,
                                font_name = 'ArialItalic.ttf', halign='center',
                                valign = 'middle', x = GAME_WIDTH/2,
                                y = GAME_HEIGHT/2)
            
    def getMssg2(self):
        return self._mssg2
    
    def setMssg2(self, txt, fontsize, x, y):
        assert type(txt) == str
        self._mssg2 = GLabel(text = txt, font_size = fontsize,
                        font_name = 'ArialItalic.ttf', halign = 'center',
                        valign = 'middle', x = x,
                        y = y)
    
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _mssg) saying that the user should press
        to play a game."""
        
        self.setGame(None)
        self.time_elapsed = 0
        self.setMssg2('New Game', 30, GAME_WIDTH/2, GAME_HEIGHT/3)
        self.last_keys = 0 #number of keys being pressed at that state
        self.setState(STATE_INACTIVE)
        self.image = GImage(x = GAME_WIDTH/2, y = GAME_HEIGHT/4,
                            width = GAME_WIDTH/4, height = GAME_HEIGHT/4,
                            source = 'walkerwhite.png')
        
        if self.getState()==STATE_INACTIVE:
            self.setMssg('Press any key to begin')
         
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Play.  The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Play object _game to play the
        game.
        
        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWGAME,STATE_COUNTDOWN, STATE_PAUSED, and
        STATE_ACTIVE.  Each one of these does its own thing, and so should have
        its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It
        is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the
        screen.  
        This state only lasts one animation frame before switching to
        STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball
        is served.  The player can move the paddle during the countdown, but
        there is no ball on the screen.  Paddle movement is handled by the Play
        object.  Hence the Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move
        the paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).
        Hence the Play class should have methods named updatePaddle() and
        updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the
        game is still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so
        long as the player never presses a key.  In addition, the application
        switches to this state if the previous state was STATE_ACTIVE and the
        game is over (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent
        3 seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are
        still some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.
        
        STATE_COMPLETE: The application switches to this state after the ball is
        lost and there are no tries remaining. The game is then over.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == float or type(dt) == int
        
        if self.getState() == STATE_INACTIVE:
            self.update_state_inactive()
        if self.getState() == STATE_NEWGAME:
            self.update_state_newgame()
        if self.getState() == STATE_COUNTDOWN:
            self.update_state_countdown(dt)
        if self.getState() == STATE_ACTIVE:
            self.update_state_active(dt)
        if self.getState() == STATE_PAUSED:
            self.update_state_paused()
        if self.getState() == STATE_COMPLETE:
            self.update_state_complete(dt)
        
    def update_state_inactive(self):
        """STATE_INACTIVE: This is the state at the beginning, and is the state
        so long as the player never presses a key.  In addition, the application
        switches to this state if the previous state was STATE_ACTIVE and the
        game is over (e.g. all balls are lost or no more bricks are on the screen).
        """

        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.last_keys == 0
        if change:
            self.setState(STATE_NEWGAME)
        
    def update_state_newgame(self):
        """STATE_NEWGAME: The application switches to this state if the state 
        was STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        This is the state creates a new game and shows it on the
        screen.  This state only lasts one animation frame before switching to
        STATE_COUNTDOWN."""
        
        self.time_elapsed = 0
        self.setGame(Play())       
        self.setState(STATE_COUNTDOWN)
 
    def update_state_countdown(self, dt):
        """STATE_COUNTDOWN: The application switches to this state after the
        ball is lost and there are no tries remaining. The game is then over.
        
        This is a 3 second countdown that lasts until the ball
        is served.  The player can move the paddle during the countdown, but
        there is no ball on the screen.  Paddle movement is handled by the Play
        object.  Hence the Play class should have a method called updatePaddle()
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
    
        assert type(dt) == float or type(dt) == int
        
        self.setMssg('Deleting message')
        self.countdown_timer()
        self._game.updatePaddle(self.input)
        self.time_elapsed = self.time_elapsed + dt
        if self.time_elapsed >= 3:
            self._mssg = None
            self.num_bricks_remaining()
            self.setState(STATE_ACTIVE)
        
    def update_state_active(self, dt):
        """STATE_ACTIVE: The application switches to this state after it has
        spent 3 seconds in the state STATE_COUNTDOWN.
        
        This is a session of normal gameplay.  The player can move
        the paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).
        Hence the Play class should have methods named updatePaddle() and
        updateBall().
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == float or type(dt) == int
        
        self._mssg2.text = 'Bricks Remaining: ' + str(len(self._game._bricks))
        self._game.updatePaddle(self.input)
        self.time_elapsed = self.time_elapsed + dt
        if self.time_elapsed > 4:
            self._game.drawBall(self.view)
            self._game.updateBall()
        self._game.bounceBall()
        if self._game.life_lost() == True and self._game.getTries() != 0:
            self.last_keys = self.input.key_count
            self.setState(STATE_PAUSED)
        if self._game.life_lost() == False:
            self.last_keys = self.input.key_count
            self.setState(STATE_COMPLETE)
        if self._game.win() == True:
            self.last_keys = self.input.key_count
            self.last_active_frame = self.time_elapsed
            self.setState(STATE_COMPLETE)
            
    def update_state_paused(self):
        """STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are
        still some tries remaining.
        
        Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.
        """
        self._game.setCounter(0)
        self.setMssg('Press any key to try again')
        self.setMssg2('Number of lives remaining: ' + str(self._game.getTries()),
                      30, GAME_WIDTH/2, GAME_HEIGHT/3)
        if self.input.key_count == 0:
            self.last_keys = 0
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.last_keys == 0
        if change:
            self.time_elapsed = 0
            self.setState(STATE_COUNTDOWN)
            
    def update_state_complete(self, dt):
        """STATE_COMPLETE: The application switches to this state after the ball
        is lost and there are no tries remaining. The game is then over.
        
        The game can be reset if user presses a key.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == float or type(dt) == int
        
        self._mssg2 = None
        if self._game.life_lost() == False:
            self.setMssg('Out of lives! Press to reset')
        if self._game.win() == True:
            self.setMssg('YOU WIN! Press to start new game')
            self.image.draw(self.view)
            if self.time_elapsed == self.last_active_frame:
                self.winSound = Sound('kidscheering.wav')
                self.winSound.play()
        self.time_elapsed = self.time_elapsed + dt
        if self.input.key_count == 0:
            self.last_keys = 0
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.last_keys == 0
        if change:
            self.setState(STATE_INACTIVE)
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw
        a GObject g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Play. 
        In order to draw them, you either need to add getters for these
        attributes or you need to add a draw method to class Play.  We suggest
        the latter.  See the example subcontroller.py from class."""
        
        if self.getMssg() != None:
            self._mssg.draw(self.view)
            
        if self._game != None:
            self._game.draw(self.view)
            
        if self.getMssg2() != None:
            self._mssg2.draw(self.view)
    
    # HELPER METHODS FOR THE STATES GO HERE

    def countdown_timer(self):
        """Displays the countdown numbers (3...2...1) during the countdown state
        before the ball moves"""
        
        if 0 <= self.time_elapsed < 1:
            self.setMssg2('3', 30, GAME_WIDTH/2, GAME_HEIGHT/2)
        if 1 <= self.time_elapsed < 2:
            self.setMssg2('2', 30, GAME_WIDTH/2, GAME_HEIGHT/2)
        if 2 <= self.time_elapsed < 3:
            self.setMssg2('1', 30, GAME_WIDTH/2, GAME_HEIGHT/2)
            
    def num_bricks_remaining(self):
        """Method that prints the number of bricks remaining"""
        
        self.setMssg2('bricks remaining: ' + str(len(self._game._bricks)), 10,
                      GAME_WIDTH/2, GAME_HEIGHT - BRICK_Y_OFFSET/2 )
            

    