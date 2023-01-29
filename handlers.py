"""Main program logic handler functions"""

from shadowui import Section,Input,Label,Log

def load_tools(**kwargs):
    section = kwargs.get('section')
    #print("loading tools to "+ section.name +" ...")

    try:
        from tools.client import client_setup
        client_setup()
    except Exception as e:
        Log.error("Can't load client tools: "+str(e))

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

def load_wallet_label(**kwargs):
    section = kwargs.get('section')
    section.content = "unknown"
