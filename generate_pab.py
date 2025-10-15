from driverslib.drivers import *
from driverslib.funcs import *
from driverslib.my_csv import *
import numpy as np
import time



ready = True
filename = "pab_FELH650_10nmBW-3.csv"

#wavelength information
start_wavelength = 655
end_wavelength = 795
width = 10
step = 5
wavelengths = np.arange(start_wavelength, end_wavelength, step)
print("Scanning through", wavelengths.size, "wavelengths")
print(wavelengths)

#wavelengths = np.array([655])


if ready:
    ND = 3
    pm = PM100D(ResourceManager().list_resources()[0])
    pm.open()
    print("PM100D connected")

    z = ZaberDriver()
    laser = Laser()
    laser.__enter__()
else:
    print("Not ready")
    print("Starting without drivers")



start_position = 100
end_position = 10
slow_position = 20
slow_speed = 2
fast_speed = 10
start=time.time();i=0
table = {}

laser.on();print("Turning laser on ...");time.sleep(2)

for wave in wavelengths:
    position1, position2 = set_bandwidth(wave, width);i+=1
    if ready:
        z.move_to(position1, 1, velocity=20)
        z.move_to_waiting(position2, 2, velocity=fast_speed)
    print("Moving to", wave, "staring measurement...")

    pm.set_correction_wavelength(wave)
    powers = []
    positions = []

    z.move_to_waiting(start_position, ND, velocity=20)
    z.move_to(slow_position-1, ND, velocity=20)
    while True:
        position = z.get_position(ND)
        power = pm.power()
        powers.append(power*1000)
        positions.append(position)
        print(f"Position: {position} mm.  Power: {power} W, {power*1000} mW")
        time.sleep(0.01)
        if position <= slow_position:
            break

    z.move_to(end_position-1, ND, velocity=slow_speed)
    while True:
        position = z.get_position(ND)
        power = pm.power()
        powers.append(power*1000)
        positions.append(position)
        print(f"Position: {position} mm.  Power: {power} W, {power*1000} mW")
        time.sleep(0.01)
        if position <= end_position:
            break
    
    table[wave] = np.array([powers, positions])
    print("Collected positions and powers","-------", int(i/wavelengths.size*100),"% complete")

laser.off()
laser.__exit__(None, None, None)
pm.close()
columns_names = ['Wavelength (nm)', 'Power (mW)', 'Position (mm)']
mc.save_table_to_csv(table, filename, columns_names)


    


end=time.time();print("Total experiment time:",round(end-start,4),"seconds")



