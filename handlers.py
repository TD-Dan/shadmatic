"""Main program logic handler functions"""

from shadowui import Section,Input,Label

def load_tools(**kwargs):
    section = kwargs.get('section')
    print("loading tools to "+ section.name +" ...")

    from tools.config import ConfigTool
    from tools.airdrop import airdrop_program

    #mainwin.add_tool(config_tool)
    section += airdrop_program

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
