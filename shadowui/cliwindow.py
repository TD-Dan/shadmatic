"""Simple commandline interface
One line of input&status and a rolling wall of messages
Optionally supports color on *nix
Supports color on windows when colorama library is available
"""

import platform
import queue
import sys
import time

import state
from helper.stringtool import *
from modules import ModuleBase
from modules.log import Log
from shadowui import WindowBase
from shadowui.inputlistener import InputListener


# User pressed enter
class InputCommit(Exception): pass
# Signals input chracters have been control characer (enter, esc, etc...)
class InputConsumed(Exception): pass

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


# Capture print() statements to display them in cli
_capture_output_buffer:str = ''
_capture_output_queue = queue.Queue()
class CaptureOutput:
    def write(self, message):
        global _capture_output_buffer
        _capture_output_buffer += message

    def flush(self):
        global _capture_output_buffer
        global _capture_output_queue
        _capture_output_queue.put(_capture_output_buffer)
        _capture_output_buffer = ''


class CommandlineWindow(WindowBase):

    has_csi_support = None
    use_csi = True

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
        
        self.log = Log("CLIWindow")

        self.use_color = kwargs.get('use_color')
        
        if self.use_csi and platform.system() == "Windows":
            try:
                from colorama import Cursor, init
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
        
        self.input_listener = InputListener()
        self.input_line_buffer = ""
        self.input_line = ""
        self.read_arrow_control=False
        self.selected_module = None

        self.on_load.connect(self.load_handler)
        self.on_unload.connect(self.unload_handler)
        self.on_frame.connect(self.frame_handler)

    def load_handler(self,**kwargs):
        #print("cliwindow loadhandler "+str(kwargs))
        
        #capture print()
        #sys.stdout = CaptureOutput()

        self.input_listener.start()
        if self.use_csi:
            print(SET_TITLE(state.program_name),end='')

        self.draw_textline(f'Welcome to {state.program_name}!')
        self.draw_textline('type help to get started!')

    def unload_handler(self, **kwargs):
        self.draw_textline('-'.center(79),redraw_commandline=False)
        self.draw_textline('"Tis but a scratch" - The Black Knight'.center(79),redraw_commandline=False)
        self.draw_textline('-'.center(79),redraw_commandline=False)
        self.input_listener.close()
        # restore stdout
        #sys.stdout = sys.__stdout__
        del self.log
    
    def frame_handler(self,**kwargs):
        #print("cliwindow framehandler "+str(kwargs))
        
        global _capture_output_queue
        try:
                printable = _capture_output_queue.get_nowait()
                self.draw_textline(printable)
        except queue.Empty:
            pass
        
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
                            raise state.ProgramCancel()
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

            except InputCommit:
                words = self.input_line.split()
                self.input_line = ""
                self.input_line_buffer = ""
                if words:
                    command_or_module = words[0]
                    command = None
                    args = None
                    # try to execute module command
                    if not self.selected_module and len(words)==1:
                        #if only one word provided enter module specific mode
                        for module in state.modules:
                            if module.name == command_or_module or module.short == command_or_module:
                                self.selected_module = module
                                raise InputConsumed()
                    
                    #try to select module to run
                    mod_to_run:ModuleBase = None
                    if self.selected_module:
                        mod_to_run = self.selected_module
                        command = words[0]
                        args = words[1:]
                    else:
                        for module in state.modules:
                            if module.name == command_or_module or module.short == command_or_module:
                                mod_to_run = module
                                command = words[1]
                                args = words[2:]
                    # run it if found
                    if mod_to_run:
                        (args,kwargs) = convert_lststr_to_argskwargs(args)
                        try:
                            mod_to_run.exec(command, **kwargs)
                        except NotImplementedError as e:
                            self.draw_textline(str(e))
                    else:
                        command = words[0]
                        # default cli specific commands
                        match command:
                            case 'x'|'exit':
                                raise state.ProgramExit()
                            case _:
                                self.draw_textline(str(command)+" is not a command. type 'help' for all commands.")
            
            except state.ProgramCancel:
                if self.selected_module:
                    self.selected_module = None
                    raise InputConsumed()
                else:
                    raise
        except InputConsumed:
            self.draw_command_line()
            pass
        except state.ProgramCancel:
            raise state.ProgramExit()
        except KeyboardInterrupt:
            raise
    
    def print(self, text, *args, **kwargs):
        print(text, *args,**kwargs)
        # sys.__stdout__.write(text)
        # if kwargs.get('end'):
        #     sys.__stdout__.write(kwargs.get('end'))
        # if kwargs.get('flush'):
        #     sys.__stdout__.flush()

    def draw_textline(self,str:str,redraw_commandline=True):
        """Output one line to the screen"""
        remainder = None
        #self.log.info("drawing textline")
        #clean input away
        self.print(TO_LINE_START, end='', flush=True)
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
            self.print(str.ljust(79), end=LINE_END, flush=True)
        else:
            self.print(str.ljust(79), flush=True)
        #if more than one line keep drawing
        if remainder:
            self.draw_textline(remainder)
        elif redraw_commandline:
            #last iteration redraws commandline
            self.draw_command_line()

    def draw_command_line(self):
        """Draw input&status area"""
        #self.log.info("drawing command line")
        #clean input line
        self.print(TO_LINE_START,end='', flush=True)
        #format commandline
        logo = ''
        il='>'
        if self.selected_module:
            il += self.selected_module.name+'>'
        il += self.input_line_buffer
        if len(il)>17:
            il = il[len(il)-17:]
        filler = '[   ----   ]'
        #print command line
        self.print("░▒▓█SHAD"+il.ljust(17)+"]"+filler+filler+filler+filler+'█▓▒░',end='', flush=True)
        #place input caret
        self.print(TO_LINE_START,end='', flush=True)
        self.print("░▒▓█SHAD>"+il,end='', flush=True)


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