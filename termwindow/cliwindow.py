"""Simple commandline interface that supports color and input"""
import time

from colorama import Fore, Back, Style, init, Cursor
init(autoreset=True)

import shadowui

from termwindow.inputlistener import InputListener

class CommandlineWindow(shadowui.WindowBase):

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
    
    def run(self):
        super().run()
        
        try:

            input_listener = InputListener(self.on_input)
            input_listener.start()

            while True: 
                try:
                    time.sleep(0.025) # restrain loop to 50 fps
                    ch : str = input_listener.getInput()
                    if ch:
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
            input_listener.close()
        
    def on_input(self, input):
        print("CommandlineWindow got input: " + input)
        self._user_input = input