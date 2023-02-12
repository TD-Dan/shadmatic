
from queue import Queue
from threading import Thread

import state
from modules import ModuleBase
from modules.command import ProgramCommand
from modules.log import Log
from shadowui import Label, Signal, Timer


def load_client_label(**kwargs):
    section : Label = kwargs.get('section') #section kwarg contains calling section
    section.content = "unknown"

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

    on_status = Signal()
    status_thread = None
    
    result_queue = Queue()
    commands = [
        ProgramCommand('status', help="Query network status")
    ]

    widget = Label('iota_client_status', on_load=load_client_label, pre_content="iotanetw:")

    def load(self):
        super().load()
        self.log = Log('iotaclnt')
        # Load configuration if available
        self.conf = state.configuration.get('iotaclnt')
        if not self.conf:
            self.conf = self.default_configuration

        # Add periodic status checks
        self.sync_timer = Timer('iota_client_sync', on_timer=self.sync_status_on_timer, on_frame=self.status_checker_on_frame, interval_seconds=5)
        state.root += self.sync_timer

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
        silent_mode = kwargs.get('silent')
        threaded_mode = kwargs.get('threaded')

        if hasattr(self, 'client'):
            if threaded_mode:
                # Start a thread to get node info
                self.status_thread = Thread(target=self.threaded_status, args=(self.input_queue, self.control_queue))
                self.status_thread.start()
            else:
                # Get the node info
                self.node_info = self.client.get_info()
                self.log.info(f"Status: {self.node_info}")
                if not silent_mode:
                    print(self.node_info)
                try:
                    healty = self.node_info['nodeInfo']['status']['isHealthy']
                    if healty:
                        self.set_widget_status('ok')
                    else:
                        self.set_widget_status('down', True)
                except KeyError:
                        self.set_widget_status('error', True)
        else:
            self.log.warning('Client not loaded')
            self.set_widget_status('Not loaded', True)

       
    def sync_status_on_timer(self, **kwargs):
        actual_seconds= kwargs.get('actual_interval_seconds')
        self.status(silent=True, threaded=False)
        #print("Client module got timer sync "+str(actual_seconds))

    def status_checker_on_frame(self, **kwargs):
        if self.status_thread:
            pass

    def threaded_status(self, result_queue):
        """Client info getter for launching in separate thread."""

        # Access to self.client might not be thread safe, might need a mutex here
        node_info = self.client.get_info()

        result_queue.put(node_info)
        return
                        
                         
    def set_widget_status(self, status, error=False):
        self.error = error
        self.widget.content = status

#register to main program as a module
state.modules.append(ClientModule())