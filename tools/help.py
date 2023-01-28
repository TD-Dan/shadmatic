
from shadowui import Section

class HelpTool(Section):
    """Get help on program and tool usage"""
    short = 'h'
    long = 'help'


help_page = [
    Section('Help',command='help', short='h')
]