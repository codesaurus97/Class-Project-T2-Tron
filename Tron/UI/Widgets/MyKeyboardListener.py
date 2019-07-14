from kivy.uix.widget import Widget
from kivy.core.window import Window
import UI.mainUI
from Backend.Core.Vect2D import Vect2D
from kivy.properties import ListProperty, NumericProperty


class MyKeyboardListener(Widget):
    ## keyboard listener, listen to keyboard inputs
   
    trackPoints = ListProperty([])
    __client = None # Game Client


    def __init__(self, **kwargs):
        self.__client = kwargs['client']
        self._player = self.__client.me
        # SET BASIC VELOCITY 
        self._player.setVelocity(1,0)
        self._keyboard = Window.request_keyboard( self._keyboard_closed, self, 'text')

        ## needed to implement clone fucntion to create reference to new RAM space
        
        playerPosVec2D = self._player.getPosition()
        self.trackPoints.append(playerPosVec2D.clone())


        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        super(MyKeyboardListener, self).__init__()


    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        
        # enterPause Menu
        if keycode[1] == 'p':
            print("not Implemented Yet Pause Menu")
            UI.mainUI.GAME.RequestPause()

        if keycode[1] == 'a':
            self.press_a_key()
            # self.addingTrack_to_player()

        if keycode[1] == 'd':
            self.press_d_key()
            # self.addingTrack_to_player()

        if keycode[1] == 'w':
            self.press_a_key()
            # self.addingTrack_to_player()

        if keycode[1] == 's':
            self.press_d_key()
            # self.addingTrack_to_player()
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def press_d_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with d we go clockwise
        self.__player.setVelocity(1, 0)
    

    def press_a_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with a we go counter-clockwise
        self.__player.setVelocity(-1, 0)


    def press_w_key(self):
        self.__player.setVelocity(0, 1)

    def press_s_key(self):
        self.__player.setVelocity(0, -1)
