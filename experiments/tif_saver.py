import tifffile as tiff
import numpy as np
import os
from datetime import datetime

class TiffSaver:

    def __init__(self, file_name):
        self.now = datetime.now()
        self.path = r"H:\Shared drives\Research\data"
        self.file_name = file_name
        self.writer = tiff.TiffWriter(os.path.join(self.generate_file_path(), self.file_name), bigtiff=True)
        self.description = self.generate_description()
        

    def save(self, data):
        self.writer.write(data, description=self.description)
        print(f"saved {self.file_name}")

    def generate_description(self):
        desc_text = """
        Scan: 
        Scan Range X: 
        Scan Range Y: 
        Pixel Size: 
        Dwell Time: 
        Test Run
        Sample: Random data
        Author: Rafi
        Notes: Created with tifffile
        """
        return desc_text


    def generate_file_path(self):
        
        path_to_data = self.path
        date_folder = os.path.join(path_to_data, self.now.strftime("%Y-%m-%d"))
        time_folder = os.path.join(date_folder, self.now.strftime("time-%H.%M"))
        # Create the date folder if it doesn't exist
        os.makedirs(date_folder, exist_ok=True)
        os.makedirs(time_folder, exist_ok=True)
        return time_folder



if __name__ == "__main__":
    tif_saver = TiffSaver("zstack.tif")

    for i in range(10):
        data = (np.random.rand(256, 256) * 65535).astype(np.uint16)
        tif_saver.save(data)