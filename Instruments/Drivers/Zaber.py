from zaber_motion import Units
from zaber_motion.ascii import Connection
import time




class ZaberDriver:
    def __init__(self, com_port="COM5", baud_rate=115200):
        try:
            self.conn = Connection.open_serial_port(com_port, baud_rate)
            self.devices = self.conn.detect_devices()
        except:
            self.conn = None
            self.devices = None
            print("Failed to connect to Zaber")
        
        
    def move_to(self, position, i, velocity=None):
        device = self.devices[i]
        axis = device.get_axis(1)
        
        # Set velocity if specified
        if velocity is not None:
            axis.settings.set("maxspeed", velocity, Units.VELOCITY_MILLIMETRES_PER_SECOND)
            
        axis.move_absolute(position, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        #print(f"Device {i+1} moved to {position} mm")

    def move_to_waiting(self, position, i, velocity=None):
        device = self.devices[i]
        axis = device.get_axis(1)
        if velocity is not None:
            axis.settings.set("maxspeed", velocity, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        axis.move_absolute(position, Units.LENGTH_MILLIMETRES, wait_until_idle=False)

        while abs(axis.get_position(Units.LENGTH_MILLIMETRES) - position) > 0.01:
            time.sleep(0.1)
        #print(f"Device {i+1} moved to {position} mm")


    def get_position(self, i):
        device = self.devices[i]
        axis = device.get_axis(1)
        position = axis.get_position(Units.LENGTH_MILLIMETRES)
        return position

    def move_velocity(self, speed, i):
        device = self.devices[i]
        axis = device.get_axis(1)
        axis.move_velocity(speed, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        print(f"Device {i+1} moving at {speed} mm/s")

    def stop(self, i):
        device = self.devices[i]
        axis = device.get_axis(1)
        axis.stop()
        print(f"Device {i+1} stopped")



