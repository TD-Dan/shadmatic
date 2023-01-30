"""Main program logic handler functions"""

from shadowui import Section,Input,Label

def load_tools(**kwargs):
    section = kwargs.get('section')
    #print("loading tools to "+ section.name +" ...")

def test_input(**kwargs):
    section = kwargs.get('section')
    value = kwargs.get('value')
    print("I'v got input: "+value+" from:"+section.name)

def load_wallet_label(**kwargs):
    section = kwargs.get('section')
    section.content = "unknown"
