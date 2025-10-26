from driverslib.drivers import *
from driverslib.my_csv import *
from driverslib.funcs import *
from plot import *

ready = True
normalize_to_power = True

ND = 3
width = 10
dwell_time = 0.01
max_power = 11
start_position = 100
end_position = 13
slow_position = 40
slow_speed = 2
fast_speed = 30
going_slow = False
table = {}
experiment_filename = "jf525_di561_Ex-FGL630M-FELH625.csv"
pabfile = "pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv"
pab = mc.read_csv(pabfile)
pab_table = pab.table
wavelengths = pab.wavelengths
#wavelengths = wavelengths[7:]
#wavelengths = [655, 670, 700, 790]

def turn_on_laser(ready):
    if ready:
        print("Turning laser on...")
        laser.on()
        time.sleep(2)
        print("Laser on.")
   
    
def turn_off_laser(ready):
    if ready:
        print("Turning laser off...")
        laser.off()
        time.sleep(2)
        print("Laser off.")



print("Setting up devices...")
z = ZaberDriver()
tt = TimetaggerDriver()
g = GalvoController()
laser = Laser()
laser.__enter__()
print("Devices ready.")

def set_wavelength(wavelength, width):
    position1, position2 = set_bandwidth(wavelength, width)
    if ready:
        z.move_to(position1, 1, velocity=fast_speed)
        z.move_to_waiting(position2, 2, velocity=fast_speed)
        #print(f"Wavelength: {wavelength} nm, Position1: {position1} mm, Position2: {position2} mm")
    else:
        print(f"Wavelength: {wavelength} nm, Position1: {position1} mm, Position2: {position2} mm")


power = 10







counts = []
print("starting sweep...")
turn_on_laser(ready)
g.set_position(14, 44)
for wavelength in wavelengths:


    powers_pab = pab_table[wavelength][1]
    positions_pab = pab_table[wavelength][2]
    position = np.interp(power, powers_pab, positions_pab)
    if power > powers_pab.max():
        wavelengths = wavelengths[wavelengths != wavelength]
        continue

    z.move_to_waiting(position, ND, velocity=fast_speed)
            
    
    set_wavelength(wavelength, width)

    
    count = tt.get_counts_per_second()
    print(f"wavelength: {wavelength} nm, Counts: {count}, Power: {power} mW")
    counts.append(count)
   
g.zero_position()
turn_off_laser(ready)
plt.plot(wavelengths, counts, '.-')
plt.title("Counts vs Wavelength")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Counts")
plt.show()


