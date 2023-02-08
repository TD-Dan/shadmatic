"""Program event logging
Provides in-program event viewing
"""

import state
from shadowui import Section, Label
from modules import ModuleBase
from modules.log import Log
from modules.command import ProgramCommand

log_firstrun = [
    Section('setup_logging', children=[
        Label('logging-info', content="""This program is cabable of collecting logfiles from program usage.
                                      These are used for: ... and stored in ...,Following things are logged but not limited to ..., 
                                      Do you want to disable logging to filesystem? ...whole module?""")
    ])
]
class LogModule(ModuleBase):
    """Program event logging
    Provides in-program event viewing
    """
    name = "log"
    short = "l"

    commands = [
    ProgramCommand('write', help="Write a warning to the log.",
                        required_kwargs = {'text':"Text to log"},
                        optional_kwargs= {'level':"Logging level: INFO / WARN / ERROR"}
    )]

    def load(self):
        self.log = Log('log_modl')
        first_run = state.root['first_run']
        first_run += log_firstrun

    def unload(self):
        del self.log

    def write(self, **kwargs):
        text = kwargs.get('text')
        level = kwargs.get('level')
        if not level:
            level ='info'
        match level.lower():
            case 'i'|'info':
                self.log.info(text)
            case 'w'|'warn'|'warning':
                self.log.warning(text)
            case 'e'|'err'|'error':
                self.log.error(text)
        pass


#register to main program as a module
state.modules.append(LogModule())