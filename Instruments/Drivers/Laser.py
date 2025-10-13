
import sys
# Add the path to nkt_tools package here
sys.path.insert(0, r'G:\My Drive\Cape Microscopy Research\python\nspyre\nkt')
from nkt_tools.nkt_tools import Fianium  # type: ignore


class Laser:
    def __init__(self):
        self.laser = None
    
    def __enter__(self):
        try:
            self.laser = Fianium(portname="COM6")
            print("Attempting to connect to laser...")
            try:
                self.laser.connect()
                print("Laser connected successfully!")
            except Exception as e:
                print(f"Failed to connect: {e}")
                self.laser = None
            return self
        except:
            self.laser = None
            print("Failed to connect to laser")
            return None
    
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
