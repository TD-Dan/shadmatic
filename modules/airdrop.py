

from shadowui import Section, Input

from modules.airdrop_handlers import *

default_configuration = {
    "selected_network":"Shimmer",
    "airdrop_delay_seconds":5.0,
    "claim_expiration_seconds":604800
}

airdrop_page = [
    Section('Airdrop', children=[
        Section('existing_airdrops'),
        Section('new_airdrop', children=[
            Input('token'),
            Input('amount'),
            Input('addresses')
        ])
    ])
]
