"""Main program logic handler functions"""

from shadowui import Section,Input,Label

def load_tools(**kwargs):
    section = kwargs.get('section')
    #print("loading tools to "+ section.name +" ...")

    from tools.config import config_page
    from tools.airdrop import airdrop_page
    from tools.help import help_page

    section += config_page
    section += airdrop_page
    section += help_page

def test_input(**kwargs):
    section = kwargs.get('section')
    value = kwargs.get('value')
    print("I'v got input: "+value+" from:"+section.name)

def load_client_label(**kwargs):
    section : Label = kwargs.get('section')
    section.content = "unknown"

def load_wallet_label(**kwargs):
    section = kwargs.get('section')
    section.content = "unknown"
