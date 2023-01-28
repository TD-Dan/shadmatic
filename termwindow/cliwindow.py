"""Simple commandline interface that supports color and input"""
import time

import shadowui
from termwindow.inputlistener import InputListener

# User pressed enter
class InputCommit(Exception): pass
# Signals input chracters have been control characer (enter, esc, etc...)
class InputConsumed(Exception): pass
# signal main loop exit
class ProgramExit(Exception): pass
# signal moving back to previous menu level
class ProgramBack(Exception): pass

CLEAR_LINE = '\033[2K'


class CommandlineWindow(shadowui.WindowBase):

    input_listener = InputListener()
    input_line_buffer = ""
    input_line = ""
    read_arrow_control=False

    def add_menu_tool(self, tool: object):
        self.menu_tools.append(tool)

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
            
    def run(self):
        super().run()
        
        try:
            from colorama import Fore, Back, Style, init, Cursor
            init(autoreset=True)
        except ModuleNotFoundError:
            print("INFO: Colorama not found; no color output available.\nUse 'pip install colorama' to enable.\nPress enter to continue...")
            input()
        
        redraw = True

        try:
            self.input_listener.start()
            while True:
                try:
                    try:
                        ch : str = self.input_listener.getInput()
                        if redraw:
                            print(Cursor.BACK(80)+CLEAR_LINE+"COMMAND> " + self.input_line_buffer, end='')
                            redraw = False
                        if ch:
                            #print("CommandlineWindow main loop got input: "+str(ch)+" "+str(ch.encode('utf-8'))+" printable:"+str(ch.isprintable()))
                            if self.read_arrow_control:
                                #previous character was arrow key start, read rest here
                                match ch.encode('utf-8'):
                                    case b'H':
                                        print('up')
                                    case b'P':
                                        print('down')
                                    case b'K':
                                        #print('left')
                                        print(Cursor.BACK(1), end='')
                                    case b'M':
                                        #print('right')
                                        print(Cursor.FORWARD(1), end='')
                                self.read_arrow_control=False
                                raise InputConsumed()
                            match ch.encode('utf-8'):
                                case b'\r':
                                    #print("enter")
                                    self.input_line = self.input_line_buffer
                                    raise InputCommit()
                                case b'\x1b':
                                    #print("esc")
                                    raise ProgramBack()
                                case b'\x08':
                                    #print("backspace")
                                    raise InputConsumed()
                                case b'\xc3\xa0':
                                    #print("arrow")
                                    self.read_arrow_control = True
                                    raise InputConsumed()
                                case b'\x03':
                                    #print("ctrl-c")
                                    raise KeyboardInterrupt()
                            if ch.isprintable:
                                self.input_line_buffer += ch
                                raise InputConsumed()
                            
                        time.sleep(0.02) # restrain loop to 50 fps
                    except InputCommit:
                        print('\n')
                        words = self.input_line.split()
                        command = words[0]
                        match command:
                            case 'x'|'exit':
                                exit()
                            case _:
                                print(self.input_line+" is not a command. type 'help' for all commands.")
                        self.input_line = ""
                        self.input_line_buffer = ""
                        redraw = True
                    except InputConsumed:
                        redraw = True
                        pass
                except ProgramBack:
                    pass
                except KeyboardInterrupt:
                    print("Ctrl-C Catched!")
                    raise
        finally:
            self.input_listener.close()


    """Prompts an yes or no input from user."""
    def prompt_yes_no(self, prompt: str) -> bool:
        print(prompt+ " (y/n) > ", end='')
        while True:
            ch = self.input_listener.getInput()
            if ch:
                match ch: 
                    case 'Y'|'y'|'Yes'|'yes':
                        return True
                return False    
            time.sleep(0.02) # restrain loop to 50 fps

