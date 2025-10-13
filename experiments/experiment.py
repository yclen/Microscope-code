from driverslib.drivers import *
from driverslib.my_csv import *
from driverslib.funcs import *
from plot import *



def declare_varibles(turn_on_laser=True):

    global experiment_filename
    global ready
    global activate_laser
    global pabfile
    global width
    global dwell_time
    global max_power
    global start_position
    global end_position
    global slow_position
    global slow_speed
    global fast_speed
    global ND
    global table

    experiment_filename = "cvp4.csv"
    pabfile = "pab_FELH650_10nmBW-3.csv"

    ready = True
    activate_laser = turn_on_laser

    ND = 3
    width = 10
    dwell_time = 0.01
    max_power = 11
    start_position = 100
    end_position = 10
    slow_position = 20
    slow_speed = 5
    fast_speed = 20
    table = {}

def setup_devices():
    global z
    global tt
    global laser

    print("Setting up devices...")
    z = ZaberDriver()
    tt = TimetaggerDriver()
    laser = Laser()
    laser.__enter__()
    z.move_to_waiting(start_position, ND, velocity=fast_speed)
    print("Devices ready.")

def create_pab_table(plot_pab=False, plot_wavelength=655):
    global pab_table
    global wavelengths

    pab = read_csv(pabfile)
    pab_table = pab.table
    wavelengths = pab.wavelengths

    if plot_pab:
        positions_pab = pab_table[plot_wavelength][2]
        powers_pab = pab_table[plot_wavelength][1]
        plt.plot(positions_pab, powers_pab, '.-')
        plt.xlabel('Position (mm)')
        plt.ylabel('Power (mW)')
        plt.title(f'pab plot for {plot_wavelength} nm')
        plt.legend([plot_wavelength])
        plt.show()
        

def turn_on_laser():
    if activate_laser:
        print("Turning laser on...")
        laser.on()
        time.sleep(2)
        print("Laser on.")
    else:
        print("Laser is not activated.")

def turn_off_laser():
    if activate_laser:
        print("Turning laser off...")
        laser.off()
        time.sleep(2)
        print("Laser off.")



def sweep_powers(wavelength):
    positions_pab = pab_table[wavelength][2]
    powers_pab = pab_table[wavelength][1]

    power_values = np.linspace(0.1, max_power, 100)
    position_values = np.interp(power_values, powers_pab, positions_pab)
    counts = np.zeros(len(position_values))
   
    for i in range(len(position_values)):       
        z.move_to_waiting(position_values[i], ND, velocity=fast_speed)
        counts[i] = tt.count_for_time(dwell_time, 100).sum()     
        print(f"{i}: Position: {round(position_values[i], 2)} mm.  Power: {round(power_values[i], 2)} mW.  Counts: {round(counts[i], 2)}")

    table[wavelength] = np.array([position_values, power_values, counts])


def save_table():
    mc.save_table_to_csv(table, experiment_filename, 
    ["Wavelength (nm)", "Position (mm)", "Power (mW)", "Counts"])
    


    

    
   

def test():
    print(experiment_filename)






if __name__ == "__main__":
    declare_varibles(turn_on_laser=1)
    setup_devices()
    create_pab_table(plot_pab=False, plot_wavelength=700)
    turn_on_laser()
    sweep_powers(700)
    turn_off_laser()
    save_table()
    plot1(experiment_filename)
    



