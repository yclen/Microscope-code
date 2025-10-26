from driverslib.drivers import *
from driverslib.my_csv import *
from driverslib.funcs import *
from plot import *

ND = 3
width = 15
dwell_time = 0.01
max_power = 11
start_position = 98
end_position = 4
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
#wavelengths = [630, 655, 670, 700, 790]

def turn_on_laser():
    
    print("Turning laser on...")
    laser.on()
    time.sleep(2)
    print("Laser on.")
    

def turn_off_laser():
   
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
z.move_to_waiting(start_position, ND, velocity=fast_speed)
print("Devices ready.")

def set_wavelength(wavelength, width):
    position1, position2 = set_bandwidth(wavelength, width)
    z.move_to(position1, 1, velocity=fast_speed)
    z.move_to_waiting(position2, 2, velocity=fast_speed)


def sweep_powers():
    counts = []
    positions = []
    z.move_to_waiting(start_position, ND, velocity=fast_speed)
    print("Starting sweep...")
    going_slow = False
    z.move_velocity(-fast_speed, ND)
    while True:
        position = z.get_position(ND)
        count = tt.get_counts_per_second()

        if position < end_position:
            break
        if position < slow_position and not going_slow:
            going_slow = True
            z.move_velocity(-slow_speed, ND)



        counts.append(count)
        positions.append(position)
        print(f"Position: {position} mm.  Counts: {count}")
    return counts, positions

turn_on_laser()
g.set_position(14, 44)
for wavelength in wavelengths:
    set_wavelength(wavelength, width)
    z.move_to_waiting(start_position, ND, velocity=fast_speed)
    
    counts, positions = sweep_powers()
    

    #save table
    table[wavelength] = np.array([positions, counts])
    print(f"Saved table for {wavelength} nm")

turn_off_laser()
mc.save_table_to_csv(table, experiment_filename, 
    ["Wavelength (nm)", "Position (mm)", "Counts"])

g.zero_position()
#read table
data = mc.read_csv(experiment_filename)
table = data.table
wavelengths = data.wavelengths
for wave in wavelengths:
    plt.plot(table[wave][1], table[wave][2], '.-', label=f'counts at {wave} nm')
plt.legend()
plt.title("Counts vs Position")
plt.xlabel("Position (mm)")
plt.ylabel("Counts")
plt.show()


