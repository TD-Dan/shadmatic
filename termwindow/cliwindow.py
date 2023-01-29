"""Simple commandline interface that supports color and input"""
import time

from shadowui import WindowBase, Label, Log, ProgramExit

from termwindow.inputlistener import InputListener

# User pressed enter
class InputCommit(Exception): pass
# Signals input chracters have been control characer (enter, esc, etc...)
class InputConsumed(Exception): pass
# signal moving back to previous menu level
class ProgramBack(Exception): pass

CSI = '\033['
OSC = '\033]'
BEL = '\a'

CLEARLINE = CSI+'2K' # clear line
COLOR_WARNING = CSI+'33m' #yellow
COLOR_ERROR = CSI+'31m' #red
COLOR_OK = CSI+'32m' #green
CR = '\r' #carriage return, to start of line
ERASE = '\b'    # erase and move back one character
def CURSOR_BACK(n): return CSI + str(n) + 'D' # move cursor back n steps

xstr = lambda str: str or '' # Returns '' for None else str

class CommandlineWindow(WindowBase):

    input_listener = InputListener()
    input_line_buffer = ""
    input_line = ""
    read_arrow_control=False
    has_control_characters = True

    def add_menu_tool(self, tool: object):
        self.menu_tools.append(tool)

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
            
    def run(self):
        super().run()
        
        log = Log("CLI")
        
        try:
            from colorama import init,Cursor
            init(autoreset=True)
        except ModuleNotFoundError:
            log.warning("Colorama not found; advanced text output not available for windows.\nUse 'pip install colorama' to enable.")
            print("INFO: Colorama not found; advanced text output not available for windows.\nUse 'pip install colorama' to enable.\nPress enter to continue...")
            self.has_control_characters = False
            input()
        
        redraw = True
        redraw_input = True

        try:
            self.input_listener.start()
            while True:
                try:
                    try:
                        ch : str = self.input_listener.getInput()
                        if redraw:
                            self.draw_recursive(self)
                            redraw = False
                        if redraw_input:
                            if self.has_control_characters:
                                print(CURSOR_BACK(80)+CLEARLINE+"COMMAND> " + self.input_line_buffer, end='')
                            else:
                                print("\rCOMMAND> " + self.input_line_buffer, end='')
                            redraw_input = False
                        if ch:
                            #print("CommandlineWindow main loop got input: "+str(ch)+" "+str(ch.encode('utf-8'))+" printable:"+str(ch.isprintable()))
                            if self.read_arrow_control:
                                #previous character was arrow key start, read rest here
                                match ch.encode('utf-8'):
                                    case b'H':
                                        log.info('up arrow')
                                        pass
                                    case b'P':
                                        log.info('down arrow')
                                    case b'K':
                                        log.info('left arrow')
                                        #print(Cursor.BACK(1), end='')
                                    case b'M':
                                        log.info('right arrow')
                                        #print(Cursor.FORWARD(1), end='')
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
                                    self.input_line_buffer = self.input_line_buffer[:-1]
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
                        if words:
                            command = words[0]
                            match command:
                                case 'x'|'exit':
                                    raise ProgramExit()
                                case _:
                                    print(self.input_line+" is not a command. type 'help' for all commands.")
                        self.input_line = ""
                        self.input_line_buffer = ""
                        redraw = True
                        redraw_input = True
                    except InputConsumed:
                        redraw_input = True
                        pass
                except ProgramBack:
                    raise ProgramExit()
                except KeyboardInterrupt:
                    print("Ctrl-C Catched!")
                    raise
        finally:
            self.input_listener.close()

    def draw_recursive(self,section, level=0, debug=False):
        self.draw(section,level,debug)
        for child in section.children.values():
            self.draw_recursive(child,level+1,debug)

    def draw(self,section,level=0,debug=False):
        if debug:
            for n in range(0,level):
                print("\t", end='')

        if isinstance(section, Label):
            label : Label = section
            print(xstr(label.pre_content)+xstr(label.content)+xstr(label.post_content))
        else:
            pass
            if debug:
                print("< "+section.name+" >")


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

