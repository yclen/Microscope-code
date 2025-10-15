from nspyre import InstrumentManager
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from rpyc.utils.classic import obtain



inserv = InstrumentManager()
pointscandriver = inserv.pointscandriver
volts_per_micron = 2/400
PIXEL_START_CH = 2
SPD_CH = 1
# pointscandriver.set_trigger_level(PIXEL_START_CH, 1)
# pointscandriver.set_trigger_level(SPD_CH, 100)




a = 1
b = 0.1
scan_range_x = 100e-6 
scan_range_y = 100e-6 
pixel_size = 1e-6 
dwell_time = 0.1e-3
center_pos_x = 0 
center_pos_y = 0

pointscandriver.generate_sequence(scan_range_x, scan_range_y, pixel_size, dwell_time, center_pos_x, center_pos_y)

for i in range(5):
    img = obtain(pointscandriver.fullscan())
    plt.imshow(img, origin='lower', interpolation='nearest', cmap='gray')
    plt.colorbar(label="counts")
    plt.show()



