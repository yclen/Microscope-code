from driverslib.drivers import *
from driverslib.funcs import *
from driverslib.my_csv import *
import numpy as np
import time
import plot


ready = True
filename = "pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv"

#wavelength information
start_wavelength = 600
end_wavelength = 790
width = 15
step = 5
wavelengths = np.arange(start_wavelength, end_wavelength, step)
print("Scanning through", wavelengths.size, "wavelengths")
print(wavelengths)

#wavelengths = np.array([650, 700])


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

def set_wavelength(wavelength, width):
    position1, position2 = set_bandwidth(wavelength, width)
    z.move_to(position1, 1, velocity=fast_speed)
    z.move_to_waiting(position2, 2, velocity=fast_speed)

start_position = 90
end_position = 3.5
slow_position = 22
slow_speed = 2
fast_speed = 18
super_fast_speed = 30
start=time.time();i=0
table = {}

laser.on();print("Turning laser on ...");time.sleep(2)

for wave in wavelengths:


    set_wavelength(wave, width);i+=1



    print("Moving to", wave, "staring measurement...")

    pm.set_correction_wavelength(wave)
    powers = []
    positions = []

    z.move_to_waiting(start_position, ND, velocity=super_fast_speed)

    z.move_velocity(-fast_speed, ND)
    
    going_slow = False
    while True:
        position = z.get_position(ND)
        power = pm.power()*1000
        powers.append(power)
        positions.append(position)
        print(f"Wavelength: {wave} nm, Position: {round(position, 2)} mm. {round(power, 2)} mW")
        


        if position <= slow_position and not going_slow:
            going_slow = True
            z.move_velocity(-slow_speed, ND)
            
        if position <= end_position:

            break


   
    
    table[wave] = np.array([powers, positions])
    print("Collected positions and powers:",len(powers), "-------", int(i/wavelengths.size*100),"% complete")

laser.off()
laser.__exit__(None, None, None)
pm.close()
columns_names = ['Wavelength (nm)', 'Power (mW)', 'Position (mm)']
mc.save_table_to_csv(table, filename, columns_names)


    


end=time.time();print("Total experiment time:",round(end-start,4),"seconds")

plot.plot_pab(filename)

