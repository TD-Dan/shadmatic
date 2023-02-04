"""Globally available program state, where __main__.py and modules can share variables
Not thread safe!
"""

program_help_doc = """\
\nShadmatic - The superboosted Shimmer wallet

\t-help for usage. (eg. 'python . -help')

\tVisit shadmatic.com for more info.
"""

program_name = "Shadmatic"
program_slogan = "The superboosted Shimmer wallet"
program_version_str = "v0.0.2"
program_website = "shadmatic.com"


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
