"""Main program logic handler functions"""

def load_tools(**kwargs):
    section = kwargs.get('section')
    print("loading tools from "+ section.name +" ...")

    from tools.config import ConfigTool
    from tools.airdrop import AirdropTool

    config_tool = ConfigTool()
    airdrop_tool = AirdropTool()

    #mainwin.add_tool(config_tool)
    #mainwin.add_tool(airdrop_tool)

def test_input(**kwargs):
    section = kwargs.get('section')
    value = kwargs.get('value')
    print("I'v got input: "+value+" from:"+section.name)