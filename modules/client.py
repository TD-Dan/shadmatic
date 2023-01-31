
from shadowui import Label

import state



def load_client_label(**kwargs):
    section : Label = kwargs.get('section') #section kwarg contains calling section
    section.content = "unknown"


client_status = [
    Label('client_status', on_load=load_client_label, pre_content="client: [ ", post_content=" ]"),
]

class ClientModule():
    """Network client for Node connections
    """
    name = "client"
    short = "c"
    def load_module(self):
        # Add status widget
        status_area = state.root['header.status']
        status_area += client_status

    def unload_module(self):
        pass

    def run(self, **kwargs):
        args = kwargs.get('args')
        print ("client independent run invoked with :"+str(args))
        raise state.ProgramExit()


#register to main program as a module
state.modules.append(ClientModule())