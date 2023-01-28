"""Terminal gui that supports mouse, color and and other fancy stuff"""


import time
from queue import Queue

#from shadowui.windowbase import WindowBase
#from shadowui.section import Section
import shadowui

# Used to signal main loop continue
class InputUsedContinueLoop(Exception): pass
# Used to signal main loop exit
class ProgramExit(Exception): pass
# Used to signal back to previous menu level
class ProgramBack(Exception): pass


class TerminalWindow(shadowui.WindowBase):
    
    menu_tools = {}
    at_tools = {}

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
    
    def add_menu_tool(self, tool: object):
        self.menu_tools[(tool.short,tool.long)]=tool

    def add_tool(self, tool: object):
        # Check that tool keywords are not used by menu level commands or other tool commands
        for s,l in self.menu_tools | self.at_tools:
            if tool.short == s:
                raise ValueError("shorthand already in use by "+s+" "+l)
            if tool.long == l:
                raise ValueError("tool long keyword already in use by "+s+" "+l)
        self.at_tools[(tool.short,tool.long)]=tool
     
    def run(self):
        super().run()
        
        try:
            import curses
        except ModuleNotFoundError:
            import platform
            if platform.system() == "Windows":
                print("\n\nCurses library not found. For windows run 'pip install windows-curses'\n")
                raise ModuleNotFoundError("\n\nCurses library not found. For windows run 'pip install windows-curses'\n")

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
                color0_mem = curses.color_content(0)
                print("color0 was: " + str(color0_mem))
                curses.init_color(0, 1000,500,0) # 0-1000 range
                curses.init_color(curses.COLOR_RED, 1000,0,0)
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
            stdscr.addstr("Foobar")
            stdscr.addstr("goobers", curses.color_pair(1))

            print('\033]2;'+self.name+'\a')

            self.init()

            self.text(1, 1, ' '+ self.name+' ', Color.text_bold, Color.bg_dark)
            
            self.text(8,3,Color.text_normal + 'Type ' + Color.text_bold + 'help' + Color.text_normal +' for available commands.',back_color=Color.bg_light)
            self.text(8,4,'Use Ctrl-C anytime to abort current command.',Color.text_faded, Color.bg_light)

            self.text(70,2,' ▓█░   ',Color.text_as_bg, Color.bg_accent)
            self.text(70,3,' █  ░▒ ',Color.text_as_bg, Color.bg_accent)
            self.text(70,4,' ▒░  █ ',Color.text_as_bg, Color.bg_accent)
            self.text(70,5,'   ░█▓ ',Color.text_as_bg, Color.bg_accent)


            self.clear(Color.bg_dark, Rect(1,6,80,1))
            self.text(1,6,Color.text_accent + Color.bg_dark+'SW>')

            self.add_menu_tool(ExitCommand())
            self.add_menu_tool(BackCommand())
            self.add_menu_tool(HelpCommand())

            current_tool = None
            user_input=""
            last_update = time.time()

            while True:
                try:
                    time.sleep(0.1) # limit framerate
                    # if time.time()-last_update>0.5:
                    #     sys.stdout.write(".")
                    #     sys.stdout.flush()
                    #     last_update = time.time()

                    current_tool_str = ""
                    if current_tool:
                        current_tool_str = current_tool.long+'>'
                    
                    #self.text(1,6,Color.text_accent + Color.bg_dark+'SW>'+current_tool_str+user_input)
                    try:
                        input_words = user_input.split(" ")
                        for (short,long),tool in self.menu_tools.items():
                            if input_words[0].casefold() == short or input_words[0].casefold() == long:
                                print('> '+long)
                                self.menu_tools[(short,long)](*input_words[1:])
                                raise InputUsedContinueLoop
                        if not current_tool:
                            for (short,long),tool in self.at_tools.items():
                                if input_words[0].casefold() == short or input_words[0].casefold() == long:
                                    current_tool = tool
                                    print('>>> '+long)
                                    self.at_tools[(short,long)](*input_words[1:])
                        else:
                            #reroute input to current tool
                            current_tool(*input_words)
                    except InputUsedContinueLoop:
                        pass
                    except KeyboardInterrupt:
                        if current_tool:
                            BackCommand()()
                        else:
                            ExitCommand()()
                #except KeyboardInterrupt:
                #    pass
                except ProgramBack:
                    current_tool = None
                except ProgramExit:
                    print('Normal program exit')
                    exit()
                except Exception as e:
                    print("Unhandled exception")
                    raise
        finally:
            if curses.can_change_color():
                curses.init_color(0, *color0_mem) # return to terminal previous color


    """Initialize terminal view"""
    def init(self):
        pass
    

    """Empty terminal view"""
    def clear(self):
        pass

    """Print text at specified position"""
    def text(self,x,y,text,):
        pass


class Rect:
    x = 1
    y = 1
    w = 1
    h = 1
    def __init__(self,x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        

class ExitCommand:
    short = 'x'
    long = 'exit'
    def __call__(self,*args):
        if prompt_yes_no("Exit?"):
            raise ProgramExit

class BackCommand:
    short = 'b'
    long = 'back'
    def __call__(self,*args):
        raise ProgramBack

class HelpCommand:
    short = 'h'
    long = 'help'
    help = 'Displays context sensitive help.'
    def __call__(self,*args):
        if len(args)>0:
            for (short,long),tool in self.menu_tools.items()|self.at_tools.items():
                if args[0].casefold() == short or args[0].casefold() == long:
                    try:
                        print("\tcommand:\t"+tool.long)
                        print("\tshortcut:\t"+tool.short)
                        print(tool.help)
                        print(tool.help_long)
                    except AttributeError:
                        pass
            return

        print("Commands available everywhere:")
        for (short,long),tool in self.menu_tools.items():
            print('\t'+short+' - '+long+'\t',end='')
            try:
                print(tool.help)
            except AttributeError:
                print("")
        print("Tools:")
        for (short,long),tool in self.at_tools.items():
            print('\t'+short+' - '+long+'\t',end='')
            try:
                print(tool.help)
            except AttributeError:
                print("")
        print("\nUse help <tool> for more help.\n")
