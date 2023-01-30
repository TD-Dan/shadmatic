"""Main program logic and dom"""

from shadowui import Section,Input,Label,PageView

from enum import Enum

from handlers import *

# main loop control exceptions
class ProgramExit(Exception):
    """Raised when program exit is requested"""
class ProgramConfirm(Exception):
    """Raised when current program state can advance or needs to be committed"""
class ProgramCancel(Exception):
    """Raised when current program state can needs to be reversed"""

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
        ])
]
