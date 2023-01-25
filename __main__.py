
from shadowui import Section,Input,Label
import termwindow

from tools.config import ConfigTool
from tools.airdrop import AirdropTool

def prompt_input(value):
    print("I'v got input: "+value)

program_dom = [
    Section('header',[
        Section('status'),
        Section('logo')
        ]),
    Input('prompt', on_value_changed=prompt_input),
    Section('menu'),
    Section('content'),
    Section('footer',[Label('hintline')])
]

def main():
    mainwin : termwindow.TerminalWindow = termwindow.TerminalWindow('Shadow-wallet')
    mainwin += program_dom
   
    config_tool = ConfigTool()
    airdrop_tool = AirdropTool()

    mainwin.add_tool(config_tool)
    mainwin.add_tool(airdrop_tool)

    mainwin.open()

if __name__ == "__main__":
    main()