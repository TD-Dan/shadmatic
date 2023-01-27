"""Main program logic and dom"""

from shadowui import Section,Input,Label

from handlers import *

#Program document object model
program_dom = [
    Section('header', on_load=load_tools, children=[
        Section('status'),
        Section('logo')
        ]),
    Input('prompt', on_value_changed=test_input),
    Section('menu'),
    Section('content'),
    Section('footer',children=[
        Label('hintline')
        ])
]
