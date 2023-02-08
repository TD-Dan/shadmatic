"""Globally available program state, where __main__.py and modules can share variables
Not thread safe!
"""

program_help_doc = """\
\nShadwallet - The superboosted Shimmer wallet

\t-help for usage. (eg. 'python . -help')

\tVisit shadwallet.com for more info.
"""

program_name = "Shadwallet"
program_slogan = "The superboosted Shimmer wallet"
program_version_str = "v0.0.1"
program_website = "shadwallet.com"


# main program control exceptions
class ProgramState(Exception):
    """Base class for all Program state changes"""
    
class ProgramExit(ProgramState):
    """Raised when program exit is requested"""
class ProgramConfirm(ProgramState):
    """Raised when current program state can advance or needs to be committed"""
class ProgramCancel(ProgramState):
    """Raised when current program state needs to be reversed"""
class ProgramEnterInteractive(ProgramState):
    """Raised when module requests interactive mode
    Results in all modules getting loaded"""
class InvalidInput(ProgramState):
    """Raised when user input is not valid"""


#global modules
modules = list[object]()
#global root
root= None

class Color():
    def __init__(self, index:int, r:int, g:int, b:int) -> None:
        self.index:int = index
        self.r:int = r
        self.g:int = g
        self.b:int = b

default_color_theme = {
    'Error':Color(1, 203,91,163),
    'Error2':Color(9, 80,55,87),
    'Ok1':Color(2, 24,171,135),
    'Ok2':Color(10, 37,83,86),
    'Active1':Color(3, 233,176,112),
    'Active2':Color(11, 37,83,86),
    'Select':Color(4, 32,78,131),
    'BG':Color(5, 32,35,57),
    'BG2':Color(12, 32,42,72),
    'BG3':Color(13, 43,53,84),
    'Text':Color(7, 206,206,206),
    'Text2':Color(15, 125,129,144),
}

configuration = {
    'color_theme':default_color_theme
}
