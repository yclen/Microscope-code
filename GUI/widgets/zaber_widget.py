"""Simple Zaber Stage Control Widget"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                              QPushButton, QLabel, QDoubleSpinBox, QSlider)
from PyQt6.QtCore import QTimer, Qt
from nspyre import InstrumentManager


class ZaberControlWidget(QWidget):
    """Widget for controlling Zaber stages 1, 2, and 3"""
    
    def __init__(self):
        super().__init__()
        self.inserv = InstrumentManager()
        self.zaber = self.inserv.zaber
        self.init_ui()
        
        # Timer for updating positions
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_positions)
        self.update_timer.start(500)  # Update every 500ms
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create controls for stages 1, 2, and 3
        for stage_num in [1, 2, 3]:
            group = self.create_stage_group(stage_num)
            layout.addWidget(group)
        
        self.setLayout(layout)
    
    def create_stage_group(self, stage_num):
        """Create control group for a single stage"""
        group = QGroupBox(f"Stage {stage_num}")
        layout = QVBoxLayout()
        
        # Position display
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("Current Position:"))
        pos_label = QLabel("--- mm")
        pos_label.setObjectName(f"pos_label_{stage_num}")
        pos_layout.addWidget(pos_label)
        pos_layout.addStretch()
        layout.addLayout(pos_layout)
        
        # Slider with step buttons
        slider_layout = QHBoxLayout()
        
        # Left arrow button (-1mm)
        left_btn = QPushButton("◄")
        left_btn.setFixedWidth(40)
        left_btn.clicked.connect(lambda: self.step_stage(stage_num, -1))
        slider_layout.addWidget(left_btn)
        
        # Slider
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 15000)  # 0 to 150mm in 0.01mm increments
        slider.setValue(1000)  # Start at 10mm
        slider.setObjectName(f"slider_{stage_num}")
        slider.valueChanged.connect(lambda: self.slider_changed(stage_num))
        slider_layout.addWidget(slider)
        
        # Right arrow button (+1mm)
        right_btn = QPushButton("►")
        right_btn.setFixedWidth(40)
        right_btn.clicked.connect(lambda: self.step_stage(stage_num, 1))
        slider_layout.addWidget(right_btn)
        
        layout.addLayout(slider_layout)
        
        # Move to position controls
        move_layout = QHBoxLayout()
        move_layout.addWidget(QLabel("Move to:"))
        
        position_spin = QDoubleSpinBox()
        position_spin.setRange(0, 150)
        position_spin.setSuffix(" mm")
        position_spin.setDecimals(2)
        position_spin.setValue(10.0)
        position_spin.setObjectName(f"position_spin_{stage_num}")
        move_layout.addWidget(position_spin)
        
        velocity_spin = QDoubleSpinBox()
        velocity_spin.setRange(0.1, 50)
        velocity_spin.setSuffix(" mm/s")
        velocity_spin.setDecimals(1)
        velocity_spin.setValue(10.0)
        velocity_spin.setObjectName(f"velocity_spin_{stage_num}")
        move_layout.addWidget(velocity_spin)
        
        move_btn = QPushButton("Move")
        move_btn.clicked.connect(lambda: self.move_stage(stage_num))
        move_layout.addWidget(move_btn)
        
        layout.addLayout(move_layout)
        
        # Stop button
        stop_btn = QPushButton("STOP")
        stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        stop_btn.clicked.connect(lambda: self.stop_stage(stage_num))
        layout.addWidget(stop_btn)
        
        group.setLayout(layout)
        return group
    
    def move_stage(self, stage_num):
        """Move stage to specified position"""
        position_spin = self.findChild(QDoubleSpinBox, f"position_spin_{stage_num}")
        velocity_spin = self.findChild(QDoubleSpinBox, f"velocity_spin_{stage_num}")
        
        position = position_spin.value()
        velocity = velocity_spin.value()
        
        self.zaber.move_to(position, stage_num, velocity=velocity)
        print(f"Stage {stage_num} moving to {position} mm at {velocity} mm/s")
    
    def stop_stage(self, stage_num):
        """Stop stage immediately"""
        self.zaber.stop(stage_num)
        print(f"Stage {stage_num} stopped")
    
    def slider_changed(self, stage_num):
        """Handle slider movement"""
        slider = self.findChild(QSlider, f"slider_{stage_num}")
        velocity_spin = self.findChild(QDoubleSpinBox, f"velocity_spin_{stage_num}")
        
        # Convert slider value (0-15000) to position (0-150mm)
        position = slider.value() / 100.0
        velocity = velocity_spin.value()
        
        self.zaber.move_to(position, stage_num, velocity=velocity)
    
    def step_stage(self, stage_num, step_mm):
        """Move stage by a fixed step (1mm left or right)"""
        try:
            current_position = self.zaber.get_position(stage_num)
            velocity_spin = self.findChild(QDoubleSpinBox, f"velocity_spin_{stage_num}")
            velocity = velocity_spin.value()
            
            new_position = max(0, min(150, current_position + step_mm))
            
            self.zaber.move_to(new_position, stage_num, velocity=velocity)
            
            # Update slider
            slider = self.findChild(QSlider, f"slider_{stage_num}")
            slider.setValue(int(new_position * 100))
            
            print(f"Stage {stage_num} stepped {step_mm:+.1f}mm to {new_position:.2f}mm")
        except Exception as e:
            print(f"Error stepping stage {stage_num}: {e}")
    
    def update_positions(self):
        """Update position displays for all stages"""
        for stage_num in [1, 2, 3]:
            try:
                position = self.zaber.get_position(stage_num)
                pos_label = self.findChild(QLabel, f"pos_label_{stage_num}")
                pos_label.setText(f"{position:.2f} mm")
            except Exception as e:
                print(f"Error reading position for stage {stage_num}: {e}")

