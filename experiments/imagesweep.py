from driverslib.drivers import *
from pointscandriver import pointscandriver
import matplotlib.pyplot as plt
import time
from driverslib.my_csv import *
import numpy as np
import driverslib.my_csv as mc
from driverslib.funcs import *
from tif_saver import TiffSaver

width = 10
ND = 3
fast_speed = 30
position = 4
power = 10
laser = Laser()
laser.__enter__()
scan_range_x = 100e-6 
scan_range_y = 100e-6 
pixel_size = 1e-6
dwell_time = 0.1e-3
center_pos_x = 0 
center_pos_y = 0
z = ZaberDriver()
ps = pointscandriver()
ps.generate_sequence(scan_range_x, scan_range_y, pixel_size, dwell_time)


pabfile = "pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv"
pab = mc.read_csv(pabfile)
pab_table = pab.table
wavelengths = pab.wavelengths
print(wavelengths)

def set_wavelength(wavelength, width):
    position1, position2 = set_bandwidth(wavelength, width)
    z.move_to(position1, 1, velocity=fast_speed)
    z.move_to_waiting(position2, 2, velocity=fast_speed)


tif_saver = TiffSaver("zstack2.tif")
laser.on()
print("Laser on...")
time.sleep(2)
means = []
for wavelength in wavelengths:
    set_wavelength(wavelength, width)
    # powers_pab = pab_table[wavelength][1]
    # positions_pab = pab_table[wavelength][2]
    # position = np.interp(power, powers_pab, positions_pab)
    # if power > powers_pab.max():
    #     wavelengths = wavelengths[wavelengths != wavelength]
    #     continue
    z.move_to_waiting(position, ND, velocity=fast_speed)
    print(f"Wavelength: {wavelength} nm, Position: {position} mm")
        


    
    img = ps.fullscan()
    tif_saver.save(img)
    mean = np.mean(img)
    means.append(mean)
    print(f"Mean: {mean}")
    # plt.imshow(img, origin='lower', interpolation='nearest', cmap='gray')
    # plt.colorbar(label="counts")
    # plt.show()

laser.off()
print("Laser off...")
plt.plot(wavelengths, means, '.-')
plt.xlabel("Wavelength (nm)")
plt.ylabel("Mean counts")
plt.title("Mean counts vs Wavelength")
plt.show()