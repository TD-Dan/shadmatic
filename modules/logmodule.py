"""Program event logging
Provides in-program event viewing
"""

import state
from shadowui import Section, Label
from modules import ModuleBase

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
    def load(self):
        first_run = state.root['first_run']
        first_run += log_firstrun

    def unload(self):
        pass


#register to main program as a module
state.modules.append(LogModule())