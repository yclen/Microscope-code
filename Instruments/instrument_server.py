#!/usr/bin/env python
"""
Start up an instrument server to host drivers. For the purposes of this demo,
it's assumed that this is running on the same system that will run experimental
code.
"""
from pathlib import Path
import logging

from nspyre import InstrumentServer
from nspyre import InstrumentGateway
from nspyre import nspyre_init_logger
from nspyre import serve_instrument_server_cli

import tripscope

package_root = Path(tripscope.__file__).parent
_HERE = Path(__file__).parent

# log to the console as well as a file inside the logs folder


with InstrumentServer() as inserv:
    inserv.add(
            name='testclass',
            class_path=Path(__file__).parent / 'Drivers/test_driver.py',
            class_name='testClass'
        )
    inserv.add(
            name='PM100D',
            class_path=Path(__file__).parent / 'Drivers/PowerMonitor.py',
            class_name='PM100D'
        )
    inserv.add(
            name='Laser',
            class_path=Path(__file__).parent / 'Drivers/Laser.py',
            class_name='Laser'
        )
    inserv.add(
            name='Zaber',
            class_path=Path(__file__).parent / 'Drivers/Zaber.py',
            class_name='ZaberDriver'
        )
    inserv.add(
            name='XYstage',
            class_path=Path(__file__).parent / 'Drivers/XYstage.py',
            class_name='XYstage'
        )
    
    inserv.add(
            name='Piezo',
            class_path=Path(__file__).parent / 'Drivers/Piezo.py',
            class_name='piezodriver'
        )
    inserv.add(
            name='Timetagger',
            class_path=Path(__file__).parent / 'Drivers/Timetagger.py',
            class_name='TimetaggerDriver'
        )



    # # run a CLI (command-line interface) that allows the user to enter
    # # commands to control the server
    serve_instrument_server_cli(inserv)
