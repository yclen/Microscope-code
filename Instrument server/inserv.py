#!/usr/bin/env python
"""
Start up an instrument server to host drivers. For the purposes of this demo,
it's assumed that this is running on the same system that will run experimental
code.
"""

from nspyre import InstrumentServer
from nspyre import InstrumentGateway
from pathlib import Path
from nspyre import serve_instrument_server_cli




with InstrumentServer() as inserv:
    inserv.add(
            name='test_class',
            class_path=Path(__file__).parent / 'inserv_testing.py',
            class_name='test_class'
        )

    inserv.add(
            name='zaber',
            class_path=Path(__file__).parent / 'Instruments/zaber.py',
            class_name='ZaberDriver'
        )
    
    # run a CLI (command-line interface) that allows the user to enter
    # commands to control the server
    serve_instrument_server_cli(inserv)
