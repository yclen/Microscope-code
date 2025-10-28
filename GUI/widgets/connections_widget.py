"""Connections Widget for managing device connections"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                              QPushButton, QLabel)
from PyQt6.QtCore import QTimer
from nspyre import InstrumentManager


class ConnectionsWidget(QWidget):
    """Widget for connecting/disconnecting to instruments"""
    
    def __init__(self):
        super().__init__()
        self.inserv = InstrumentManager()
        self.init_ui()
        
        # Timer for updating connection status
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)  # Update every 1 second
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Device Connections")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Zaber device
        zaber_group = self.create_device_group("Zaber Stages", "zaber")
        layout.addWidget(zaber_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_device_group(self, device_name, device_key):
        """Create a connection group for a device"""
        group = QGroupBox(device_name)
        layout = QVBoxLayout()
        
        # Status display
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        status_label = QLabel("Disconnected")
        status_label.setObjectName(f"status_{device_key}")
        status_label.setStyleSheet("color: red; font-weight: bold;")
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Connect/Disconnect buttons
        button_layout = QHBoxLayout()
        
        connect_btn = QPushButton("Connect")
        connect_btn.setObjectName(f"connect_{device_key}")
        connect_btn.clicked.connect(lambda: self.connect_device(device_key))
        button_layout.addWidget(connect_btn)
        
        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.setObjectName(f"disconnect_{device_key}")
        disconnect_btn.clicked.connect(lambda: self.disconnect_device(device_key))
        disconnect_btn.setEnabled(False)
        button_layout.addWidget(disconnect_btn)
        
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def connect_device(self, device_key):
        """Connect to a device"""
        try:
            device = getattr(self.inserv, device_key)
            success = device.connect()
            
            if success:
                print(f"{device_key} connected successfully")
                self.update_button_states(device_key, True)
            else:
                print(f"Failed to connect to {device_key}")
        except Exception as e:
            print(f"Error connecting to {device_key}: {e}")
    
    def disconnect_device(self, device_key):
        """Disconnect from a device"""
        try:
            device = getattr(self.inserv, device_key)
            device.disconnect()
            print(f"{device_key} disconnected")
            self.update_button_states(device_key, False)
        except Exception as e:
            print(f"Error disconnecting from {device_key}: {e}")
    
    def update_button_states(self, device_key, connected):
        """Update button enabled states based on connection"""
        connect_btn = self.findChild(QPushButton, f"connect_{device_key}")
        disconnect_btn = self.findChild(QPushButton, f"disconnect_{device_key}")
        
        if connect_btn and disconnect_btn:
            connect_btn.setEnabled(not connected)
            disconnect_btn.setEnabled(connected)
    
    def update_status(self):
        """Update connection status displays"""
        # Update Zaber status
        try:
            zaber = self.inserv.zaber
            connected = zaber.is_connected()
            
            status_label = self.findChild(QLabel, "status_zaber")
            if status_label:
                if connected:
                    status_label.setText("Connected")
                    status_label.setStyleSheet("color: green; font-weight: bold;")
                else:
                    status_label.setText("Disconnected")
                    status_label.setStyleSheet("color: red; font-weight: bold;")
            
            self.update_button_states("zaber", connected)
        except Exception as e:
            print(f"Error updating status: {e}")

