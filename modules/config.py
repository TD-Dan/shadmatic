from shadowui import Section

default_configuration = {
    "networks": {
        "Shimmer": ["https://api.shimmer.network"],
        "Shimmer testnet":["https://api.testnet.shimmer.network"]
        },
    "selected_network":"Shimmer",
    "airdrop_delay_seconds":5.0,
    "claim_expiration_seconds":604800
}

config_page = [
    Section('Settings',command='settings', short='s', __doc__=
    """Manage settings that are shared by all tools.
    """,children=[
        Section('network'),
        Section('wallet'),
        Section('theme'),
    ])
]