
import clr
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericPiezoCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.Benchtop.PrecisionPiezoCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericPiezoCLI import *
from Thorlabs.MotionControl.GenericPiezoCLI import Piezo
from Thorlabs.MotionControl.Benchtop.PrecisionPiezoCLI import *
from System import Decimal, Convert  # necessary for real world units
import time





class piezodriver:
    

    def __init__(self):

        try:
            # Initialize the device manager
            DeviceManagerCLI.BuildDeviceList()
            self.serial_number = "44509714"
            self.device = BenchtopPrecisionPiezo.CreateBenchtopPiezo(self.serial_number)
            self.device.Connect(self.serial_number)
            self.channel = self.device.GetChannel(1)
            
            # Ensure that the device settings have been initialized
            if not self.channel.IsSettingsInitialized():
                self.channel.WaitForSettingsInitialized(10000)  # 10 second timeout
                assert self.channel.IsSettingsInitialized() is True

            # Start polling and enable
            self.channel.StartPolling(250)
            time.sleep(0.25)
            self.channel.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            self.position = self.get_position()

        except:
            self.device = None
            self.channel = None
            self.position = None
            print("Failed to connect to Piezo")


    def get_position(self):
        self.position = Convert.ToDouble(self.channel.GetPosition())
        return self.position

    def set_position(self, position):
        if position > 0 and position < 500:
            pos = Decimal(position)
            self.channel.SetPosition(pos)
            # time.sleep(0.1)
            # self.position = self.get_position()
            print(f"Piezo position = {self.position} um")
        else:
            print("Position out of range")

    def move_by(self, step):
        self.set_position(self.get_position() + step)
