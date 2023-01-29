from .log import Log
from .section import Section
from .windowbase import WindowBase
from .input import Input
from .label import Label
from .pageview import PageView

# signal main loop exit
class ProgramExit(Exception): pass