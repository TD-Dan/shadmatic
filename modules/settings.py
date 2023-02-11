import state
from modules import ModuleBase
from shadowui import Section

config_page = [
    Section('Settings', __doc__=
    """Manage settings that are shared by all tools.
    """)
]

class SettingsModule(ModuleBase):
    """Settings module
    Adds configuration files and ui for changing program and module settings."""
    name = "settings"
    short = "set"
    
    def load(self):
        super().load()

    def unload(self):
        super().unload()
        pass

#register to main program as a module
state.modules.append(SettingsModule())
