
from shadowui import Label

from modules import ModuleBase
import state

def load_client_label(**kwargs):
    section : Label = kwargs.get('section') #section kwarg contains calling section
    section.content = "unknown"


client_status = [
    Label('client_status', on_load=load_client_label, pre_content="client: [ ", post_content=" ]"),
]

class ClientModule(ModuleBase):
    """Network client for Node connections
    """
    name = "client"
    short = "c"
    def load(self):
        super().load()
        # Add status widget
        status_area = state.root['header.status']
        status_area += client_status

    def unload(self):
        super().unload()
        pass

#register to main program as a module
state.modules.append(ClientModule())