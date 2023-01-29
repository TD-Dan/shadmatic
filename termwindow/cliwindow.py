"""Simple commandline interface that supports color and input
One line of input&status and a rolling wall of messages
"""
import time
import platform

from shadowui import WindowBase, Label, Log, ProgramExit

from termwindow.inputlistener import InputListener

# User pressed enter
class InputCommit(Exception): pass
# Signals input chracters have been control characer (enter, esc, etc...)
class InputConsumed(Exception): pass
# signal moving back to previous menu level
class ProgramBack(Exception): pass

#convenience variables
CSI = '\033['
OSC = '\033]'
BEL = '\a'

# non CSI variables used for terminal control
TO_LINE_START = '\r'
LINE_END = None #None for automatic
if platform.system().find('MINGW')!=-1:
    LINE_END='\r\n'

# CSI/OSC Variables used for color etc.
#CLEARLINE = CSI+'2K' # clear line
def SET_TITLE(t): return OSC + '2;' + t + BEL
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
    has_csi_support = None
    use_csi = False


    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self.log = Log("CLI")
            
    def run(self):
        super().run()
        
        if self.use_csi and platform.system() == "Windows":
            try:
                from colorama import init,Cursor
                init(autoreset=True)
                self.has_csi_support = True
            except ModuleNotFoundError:
                self.log.warning("Colorama not found; advanced text output not available for windows.\nUse 'pip install colorama' to enable.")
                print("INFO: Colorama not found; advanced text output not available for windows.\nUse 'pip install colorama' to enable.\nPress enter to continue...")
                self.has_csi_support = False
                input()
        else:
            #Assume all other platforms have CSI/OSC support
            self.has_csi_support = True
        
        if self.use_csi and not self.has_csi_support:
            self.use_csi = False

        try:
            self.input_listener.start()
            
            if self.use_csi:
                print(SET_TITLE('Shadow-wallet'),end='')

            self.draw_command_line()

            while True:
                try:
                    try:
                        ch : str = self.input_listener.getInput()

                        if ch:
                            self.log.info("CommandlineWindow main loop got input: "+str(ch)+" "+str(ch.encode('utf-8'))+" printable:"+str(ch.isprintable()))
                            if self.read_arrow_control:
                                #previous character was arrow key start, read rest here
                                match ch.encode('utf-8'):
                                    case b'H':
                                        self.log.info('up arrow')
                                        pass
                                    case b'P':
                                        self.log.info('down arrow')
                                    case b'K':
                                        self.log.info('left arrow')
                                    case b'M':
                                        self.log.info('right arrow')
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
                        words = self.input_line.split()
                        self.input_line = ""
                        self.input_line_buffer = ""
                        if words:
                            command = words[0]
                            match command:
                                case 'x'|'exit':
                                    raise ProgramExit()
                                case _:
                                    self.draw_textline(command+" is not a command. type 'help' for all commands.")
                    except InputConsumed:
                        self.draw_command_line()
                        pass
                except ProgramBack:
                    raise ProgramExit()
                except KeyboardInterrupt:
                    raise
        finally:
            self.draw_textline('-'.center(79),redraw_commandline=False)
            self.draw_textline('"Tis but a scratch" - The Black Knight'.center(79),redraw_commandline=False)
            self.draw_textline('-'.center(79),redraw_commandline=False)
            self.input_listener.close()
            del self.log

    def draw_textline(self,str:str,redraw_commandline=True):
        """Output one line to the screen"""
        remainder = None
        #self.log.info("drawing textline")
        #clean input away
        print(TO_LINE_START, end='', flush=True)
        #format line
        if len(str)>80:
            #find last space character
            cut_at = str.rfind(' ')
            if cut_at == -1:
                cut_at = 80
            remainder = str[cut_at:]
            str = str[:cut_at]
        #replace clean line with textline and advance one line down
        if LINE_END:
            print(str.ljust(79), end=LINE_END, flush=True)
        else:
            print(str.ljust(79), flush=True)
        #redraw commandline
        if remainder:
            self.draw_textline(remainder)
        elif redraw_commandline:
            self.draw_command_line()

    def draw_command_line(self):
        """Draw input&status area"""
        #self.log.info("drawing command line")
        #clean input line
        print(TO_LINE_START,end='', flush=True)
        #format commandline
        logo = ''
        il = self.input_line_buffer
        if len(il)>17:
            il = il[len(il)-17:]
        filler = '[   ----   ]'
        #print command line
        print("░▒▓█SHAD>"+il.ljust(17)+"]"+filler+filler+filler+filler+'█▓▒░',end='', flush=True)
        #place input caret
        print(TO_LINE_START,end='', flush=True)
        print("░▒▓█SHAD>"+il,end='', flush=True)


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

