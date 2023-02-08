
import state
from modules import ModuleBase
from modules.command import ProgramCommand
from modules.log import Log
from shadowui import Label


def load_client_label(**kwargs):
    section : Label = kwargs.get('section') #section kwarg contains calling section
    section.content = "status unknown"

class IotaClientError(Exception):
    pass

def wrap_client_call(func:callable, *args, **kwargs):
    ret = func(*args,**kwargs)
    if "type" in ret:
        print(ret)
        raise IotaClientError(ret["type"])
    else:
        return ret

class ClientModule(ModuleBase):
    """Network client for Node connections
    """
    name = "client"
    short = "c"

    default_configuration = {
        "networks": {
            "Shimmer": ["https://api.shimmer.network"],
            "Shimmer testnet":["https://api.testnet.shimmer.network"]
            },
        "selected_network":"Shimmer",
        "airdrop_delay_seconds":5.0,
        "claim_expiration_seconds":604800
    }

    commands = [
        ProgramCommand('status', help="Query network status")
    ]

    widget = Label('iota_client_status', on_load=load_client_label, pre_content="iotaclnt[", post_content="]")

    def load(self):
        super().load()
        self.log = Log('iotaclnt')
        # Load configuration if available
        self.conf = state.configuration.get('iotaclnt')
        if not self.conf:
            self.conf = self.default_configuration

        # Add status widget
        status_area = state.root['header.status_widget']
        status_area += self.widget
        
        # Open iota client
        try:
            from iota_client import IotaClient
        except ModuleNotFoundError:
            self.log.error('Cant find IotaClient. Iota client library needs to be installed:\n https://wiki.iota.org/shimmer/iota.rs/getting_started/python/')

        try:
             self.client = IotaClient({'nodes': self.conf['networks'][self.conf['selected_network']]})
             try:
                node_info = wrap_client_call(self.client.get_info)
             except IotaClientError as e:
                 self.log.warning(str(e))
                 self.set_widget_status(str(e.args),error=True)
        except Exception:
             raise

    def unload(self):
        super().unload()
        self.log.close()


    def status(self,**kwargs):
        if hasattr(self, 'client'):
            # Get the node info
            self.node_info = self.client.get_info()
            self.log.info(f"Status: {self.node_info}")
            print(self.node_info)
            self.set_widget_status('Ok?')
        else:
            self.log.warning('Client not loaded')
            self.set_widget_status('Client not loaded')

        
    def set_widget_status(self, status, error=False):
        self.error = error
        self.widget.content = status

#register to main program as a module
state.modules.append(ClientModule())