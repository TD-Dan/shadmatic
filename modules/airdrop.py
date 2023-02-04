

from shadowui import Section

from modules.airdrop_handlers import *

airdrop_page = [
    Section('Airdrop',command='airdrop', short='a', __doc__=
    """Prepare and send out an airdrop to multiple recipients.
    Airdrops are managed by stages: staging, drop active, follow.
    If "simulate" is enabled will only do a test airdrop run without sending any actual coins or tokens.
    """,children=[
        Section('new_airdrop'),
        Section('existing_airdrops'),
    ])
]
