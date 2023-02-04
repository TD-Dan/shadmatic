"""Main program logic and dom"""

from shadowui import Section,Input,Label,PageView

from enum import Enum

from handlers import *

#Program document object model
program_dom = [
    Section('header', children=[
        Section('status', children=[
            Label('wallet_status', on_load=load_wallet_label, pre_content="wallet: [ ", post_content=" ]")
            ]),
        Section('logo')
        ]),
    Input('prompt', on_value_changed=test_input),
    Section('menu'),
    PageView('content', on_load=load_tools, children=[
        Section('welcome_screen')
    ]),
    Section('footer',children=[
        Label('hintline',content='no hint')
        ]),
    Section('exit', command='exit', short='x', hidden=True, children=[
        Input('yes_no')
        ]),
    Section('first_run', children=[
        
    ])
]
