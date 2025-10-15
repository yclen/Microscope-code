import TimeTagger
import time
import numpy as np


class TimetaggerDriver:
    def __init__(self, binwidth=10e9, num_bins=5):
        self.binwidth = binwidth #in ps (10e9 ps is 10ms)
        self.num_bins = num_bins
        print("connecting to timetagger...")
        self.tagger = TimeTagger.createTimeTagger()
        self.tagger.setTriggerLevel(1, 1.0)  # 1V threshold on channel 1
        self.counter = TimeTagger.Counter(self.tagger, channels=[1], binwidth=self.binwidth, n_values=self.num_bins) #binwidth is in ps (10e9 is 10ms)

    def get_counts_per_second(self):
        #returns counts per second
        counts = self.counter.getData()[0]
        return np.mean(counts)*1e12/self.binwidth

    def set_counter(self, binwidth, num_bins):
        self.binwidth = binwidth
        self.num_bins = num_bins
        self.counter = TimeTagger.Counter(self.tagger, channels=[1], binwidth=self.binwidth, n_values=self.num_bins)

    def get_counts(self):
        return self.counter.getData()[0]

    def count_for_time(self, t, n_bins):
        binwidth = t/n_bins
        self.set_counter(binwidth*1e12, n_bins)
        #print(f"counting for {t} seconds")
        while self.counter.getData()[0][0] == 0:
            time.sleep(0)

        time.sleep(t)
        counts = self.get_counts()
        return counts

   
from zaber_motion import Units
from zaber_motion.ascii import Connection
import time


class ZaberDriver:
    def __init__(self, com_port="COM5", baud_rate=115200):
        self.conn = Connection.open_serial_port(com_port, baud_rate)
        self.devices = self.conn.detect_devices()
        
        
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
        #print(f"Device {i+1} moving at {speed} mm/s")

    def stop(self, i):
        device = self.devices[i]
        axis = device.get_axis(1)
        axis.stop()
        print(f"Device {i+1} stopped")






    
   

from pulsestreamer import PulseStreamer



class GalvoController:
    # Calibration constant from original code
    volts_per_micron = 2/400
    
    def __init__(self, ip_address='192.168.0.100'):
        """Initialize connection to PulseStreamer."""
        self.ps = PulseStreamer(ip_address)
        print(f"Connected to PulseStreamer at {ip_address}")
    
    def set_position(self, x_meters, y_meters):
        """
        Set galvo position to specified coordinates.
        
        Args:
            x_meters: X position in meters
            y_meters: Y position in meters
        """
        # Convert meters to micrometers, then to volts
        x_volts = x_meters * 1e6 * self.volts_per_micron
        y_volts = y_meters * 1e6 * self.volts_per_micron
        
        # Set constant output: (digital_channels_list, x_analog_voltage, y_analog_voltage)
        self.ps.constant(([], x_volts, y_volts))
        
        print(f"Galvo position set to: ({x_meters*1e6:.1f} µm, {y_meters*1e6:.1f} µm)")
        print(f"Voltage output: ({x_volts:.3f} V, {y_volts:.3f} V)")
    
    def set_voltage(self, x_volts, y_volts):
        """
        Set galvo position using direct voltage values.
        
        Args:
            x_volts: X galvo voltage
            y_volts: Y galvo voltage
        """
        # Set constant output directly with voltage values
        self.ps.constant(([], x_volts, y_volts))
        
        #print(f"Galvo voltage set to: ({x_volts:.3f} V, {y_volts:.3f} V)")
    
    def zero_position(self):
        """Set galvos to zero position (center)."""
        self.set_position(0, 0)
    
    def close(self):
        """Close connection and set galvos to zero."""
        self.zero_position()
        print("Galvo controller closed")

    def set_spot(self, x, y):
        self.spot = (x, y)

    def goto_spot(self):
        self.set_voltage(self.spot[0], self.spot[1])

    def zero(self):
        self.set_voltage(0, 0)

from pyvisa import ResourceManager



class PM100D:
    def __init__(self, address):
        """
        Args:
            address: PyVISA resource path.
        """
        self.rm = ResourceManager()
        self.address = address

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def __str__(self):
        return f'{self.address} {self.idn}'

    def open(self):
        try:
            self.device = self.rm.open_resource(self.address)
        except Exception as err:
            raise ConnectionError(f'Failed connecting to PM100D @ [{self.address}]') from err
        # 1 second timeout
        self.device.timeout = 1000
        self.idn = self.device.query('*IDN?')
        
        return self

    def close(self):
        self.device.close()

    def idn(self):
        return self.device.query('*IDN?')

    def power(self):
        return float(self.device.query('MEAS:POWER?'))

    def get_correction_wavelength(self):
        return float(self.device.query('SENS:CORR:WAV?'))

    def set_correction_wavelength(self, wavelength):
        self.device.write('SENSE:CORRECTION:WAVELENGTH {}'.format(wavelength))

    def correction_wavelength_range(self):
        cmd = 'SENSE:CORRECTION:WAVELENGTH? {}'
        cmd_vals = ['MIN', 'MAX']
        return tuple(float(self.device.query(cmd.format(cmd_val))) for cmd_val in cmd_vals)


import sys
# Add the path to nkt_tools package here
sys.path.insert(0, r'G:\My Drive\Cape Microscopy Research\python\nspyre\nkt')
from nkt_tools.nkt_tools import Fianium  # type: ignore


class Laser:
    def __init__(self):
        self.laser = None
    
    def __enter__(self):
        self.laser = Fianium(portname="COM6")
        print("Attempting to connect to laser...")
        try:
            self.laser.connect()
            print("Laser connected successfully!")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.laser = None
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.laser:
            self.laser.close() if hasattr(self.laser, 'close') else None
    
    def on(self):
        if self.laser:
            self.laser.set_emission(True)
    
    def off(self):
        if self.laser:
            self.laser.set_emission(False)
    
    def get_status(self):
        if self.laser:
            return self.laser.status_bits
        return None
    
    def get_emission(self):
        if self.laser:
            return self.laser.emission
        return None
