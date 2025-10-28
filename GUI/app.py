#!/usr/bin/env python
"""Simple Zaber Stage Control GUI"""
import sys

from nspyre import nspyreApp, MainWidget, MainWidgetItem
from widgets import zaber_widget, connections_widget


def main():
    """Launch the Zaber control GUI application."""
    print("Starting Zaber Stage Control GUI")
    
    # Create Qt application with nspyre styling
    app = nspyreApp()
    
    # Create the main widget with Connections and Zaber control
    main_widget = MainWidget(
        {
            'Connections': {
                'Device Connections': MainWidgetItem(
                    connections_widget,
                    'ConnectionsWidget',
                    stretch=(1, 1)
                ),
            },
            'Zaber Stages': {
                'Filter Stages': MainWidgetItem(
                    zaber_widget,
                    'ZaberControlWidget',
                    stretch=(1, 1)
                ),
            }
        }
    )
    
    # Show the GUI
    main_widget.show()
    print("GUI launched successfully!")
    
    # Run the GUI event loop
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
