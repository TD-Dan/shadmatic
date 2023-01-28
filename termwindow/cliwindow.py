
import curses

import time

import shadowui

from termwindow.inputlistener import InputListener

class CommandlineWindow(shadowui.WindowBase):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
    
    def run(self):
        super().run()
        
        try:
            stdscr = curses.initscr()
            stdscr.timeout(0)
            if curses.has_colors():
                print("Has colors!")
                curses.start_color()
            if curses.has_extended_color_support():
                print("Has extended colors!")
            if curses.can_change_color():
                print("Can change colors!")
                curses.init_color(0, 100,255,55)
                curses.init_color(curses.COLOR_RED, 255,0,0)
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
            stdscr.addstr("Foobar")
            stdscr.addstr("goobers", curses.color_pair(1))

            #input_listener = InputListener(self.on_input)
            #input_listener.start()

            while True: 
                try:
                    time.sleep(0.025) # restrain loop to 50 fps
                    ch = stdscr.getch()
                    #user_input : str = input_listener.getInput()
                    if ch != -1:
                        print("CommandlineWindow main loop got input: "+str(ch))
                        match ch:
                            case 'x'|'exit':
                                exit()
                            case b'0x1b':
                                print("esc")
                        self._user_input = None
                except KeyboardInterrupt:
                    print("Ctrl-C Catched!")
                    raise
        finally:
            pass
            #input_listener.close()
        
    def on_input(self, input):
        print("CommandlineWindow got input: " + input)
        self._user_input = input