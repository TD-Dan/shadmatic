
from shadowui import Label

def client_setup():
    pass

def load_client_label(**kwargs):
    section : Label = kwargs.get('section')
    section.content = "unknown"


client_status = [
    Label('client_status', on_load=load_client_label, pre_content="client: [ ", post_content=" ]"),
]