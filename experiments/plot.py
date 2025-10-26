from driverslib.my_csv import *


def plot_pab(filename):
    pab = read_csv(filename)
    pab_table = pab.table
    wavelengths = pab.wavelengths
    #wavelengths = [600, 625, 630, 635, 640, 655, 670, 700, 750, 785]
    wavelengths = wavelengths[7:]
    print(len(wavelengths), wavelengths)
    power = 10

    
    for wavelength in wavelengths:
        positions = pab_table[wavelength][2]
        powers = pab_table[wavelength][1]
        plt.plot(positions, powers, '.-')
        position = np.interp(power, powers, positions)
        print(f"Wavelength: {wavelength} nm, Power: {power} mW, Position: {round(position, 2)} mm")
    plt.xlabel('Position (mm)')
    plt.ylabel('Power (mW)')
    plt.legend(wavelengths)
    plt.title(filename)
    plt.show()


def plot1(filename, i=1):
    plt.figure(i)
    data = read_csv(filename)
    
    wavelengths = data.wavelengths
    for wavelength in wavelengths:
        positions = data.table[wavelength][1]
        counts = data.table[wavelength][2]
        plt.plot(positions, counts, '.-')

    plt.xlabel('Position (mm)')
    plt.ylabel('Counts')
    plt.legend(wavelengths)
    plt.title(filename)
    #plt.show()

def plot2():
    data = read_csv("cvp1.csv")
    
    wavelengths = data.wavelengths
    for wavelength in wavelengths:
        powers = data.table[wavelength][2]
        counts = data.table[wavelength][3]
        log_powers = np.log(powers)
        log_counts = np.log(counts)
        #dlog = np.gradient(log_counts, log_powers)
        plt.figure(1)
        plt.plot(powers, counts, '.-')
        plt.figure(2)
        plt.plot(log_powers, log_counts, '.-')
        slope, intercept = np.polyfit(log_powers[-50:], log_counts[-50:], 1)
        print(f"y={slope:.2f}x + {intercept:.2f}")
        plt.plot(log_powers, slope*log_powers + intercept, '-')
        # plt.figure(3)
        # plt.plot(log_powers, dlog, '.-')


    plt.figure(1)
    plt.xlabel('Power (mW)')
    plt.ylabel('Counts')
    plt.legend(wavelengths)
    plt.title('Counts vs Power')
    plt.figure(2)
    plt.xlabel('Log Power (mW)')
    plt.ylabel('Log Counts')
    plt.legend(wavelengths)
    plt.title('Log-Log: Counts vs Power')
    plt.show()


def plot3(wavelength=700):
    data = read_csv("fastpowersweep.csv") 
    pab = read_csv("pab_FELH650_10nmBW-3.csv")
    pab_table = pab.table
    
    positions = data.table[wavelength][1]
    counts = data.table[wavelength][2]
    # Ignore the first 20 points in pab
    positions_pab = pab_table[wavelength][2]
    powers_pab = pab_table[wavelength][1]
    print(len(positions_pab), len(powers_pab))
    
    # Debug: check ranges and sorting
    print(f"positions range: {positions.min():.3f} to {positions.max():.3f}")
    print(f"positions_pab range: {positions_pab.min():.3f} to {positions_pab.max():.3f}")
    print(f"positions_pab sorted? {np.all(positions_pab[:-1] <= positions_pab[1:])}")
    
    # Sort positions_pab and powers_pab together
    sort_idx = np.argsort(positions_pab)
    positions_pab = positions_pab[sort_idx]
    powers_pab = powers_pab[sort_idx]
    
    powers = np.interp(positions, positions_pab, powers_pab)

    plt.figure(1)
    plt.plot(positions, counts, '.-')
    plt.xlabel('Position (mm)')
    plt.ylabel('Counts')
    plt.legend([wavelength])
    plt.title('Counts vs Position')
    plt.figure(2)
    plt.plot(positions_pab, powers_pab, '.-')
    plt.xlabel('Position (mm)')
    plt.ylabel('Power (mW)')
    plt.legend([wavelength])
    plt.title('Power vs Position from pab file')
    plt.figure(3)
    plt.plot(powers, counts, '.-')
    plt.xlabel('Power (mW)')
    plt.ylabel('Counts')
    plt.legend([wavelength])
    plt.title('Counts vs Power')
    plt.figure(4)
    log_powers = np.log(powers)
    log_counts = np.log(counts)
    slope, intercept = np.polyfit(log_powers[-20:], log_counts[-20:], 1)
    print(f"y={slope:.2f}x + {intercept:.2f}")
    plt.plot(log_powers, slope*log_powers + intercept, '-')
    plt.plot(log_powers, log_counts, '.-')
    plt.xlabel('Log Power')
    plt.ylabel('Log Counts')
    plt.legend([wavelength])
    plt.title('Log-Log: Counts vs Power')
    # plt.figure(5)
    # log_counts_smooth = np.convolve(log_counts, np.ones(5)/5, mode='same')
    # dlog = np.gradient(log_counts_smooth, log_powers)
    # plt.plot(log_powers, dlog, '.-')
    # plt.xlabel('Log Power')
    # plt.ylabel('d(Log Counts)/d(Log Power)')
    # plt.legend([wavelength])
    # plt.title('Derivative of Log-Log Plot')
    plt.show()
        


def plot4():
    data = read_csv("fastpowersweep_live_dark3.csv")



    pab = read_csv("pab_FELH650_10nmBW-3.csv")
    pab_table = pab.table

    wavelengths = data.wavelengths
    print(wavelengths)
    #wavelengths = [655, 700, 750, 785, 790]
    for wavelength in wavelengths:
        positions = data.table[wavelength][1]
        counts = data.table[wavelength][2]

        positions_pab = pab_table[wavelength][2]
        powers_pab = pab_table[wavelength][1]
        # Debug: check ranges and sorting
        print(f"positions range: {positions.min():.3f} to {positions.max():.3f}")
        print(f"positions_pab range: {positions_pab.min():.3f} to {positions_pab.max():.3f}")
        print(f"positions_pab sorted? {np.all(positions_pab[:-1] <= positions_pab[1:])}")
        
        # Sort positions_pab and powers_pab together
        sort_idx = np.argsort(positions_pab)
        positions_pab = positions_pab[sort_idx]
        powers_pab = powers_pab[sort_idx]
        
        powers = np.interp(positions, positions_pab, powers_pab)


        plt.figure(1)
        plt.plot(positions, counts, '.-')
        plt.figure(2)
        plt.plot(powers, counts, '.-')


    plt.figure(1)
    plt.xlabel('Position (mm)')
    plt.ylabel('Counts')
    plt.legend(wavelengths)
    plt.title('Counts vs Position')
    plt.figure(2)
    plt.xlabel('Power (mW)')
    plt.ylabel('Counts')
    plt.legend(wavelengths)
    plt.title('Counts vs Power')
    plt.show()




def plot5():
    data = read_csv("fastpowersweep3.csv")
    dark_data = read_csv("fastpowersweep4.csv")
    pab = read_csv("pab_FELH650_10nmBW-3.csv")
    pab_table = pab.table
    
    wavelengths = [655, 700, 750, 785]
    for wavelength in wavelengths:
        # Signal data
        positions = data.table[wavelength][1]
        counts = data.table[wavelength][2]
        
        # Dark counts data
        dark_positions = dark_data.table[wavelength][1]
        dark_counts = dark_data.table[wavelength][2]
        
        # Sort dark data for interpolation
        sort_idx = np.argsort(dark_positions)
        dark_positions = dark_positions[sort_idx]
        dark_counts = dark_counts[sort_idx]
        
        # Interpolate dark counts at signal positions
        dark_counts_interp = np.interp(positions, dark_positions, dark_counts)
        
        # Subtract dark counts from signal
        counts_corrected = counts - dark_counts_interp
        
        # Convert positions to powers
        positions_pab = pab_table[wavelength][2]
        powers_pab = pab_table[wavelength][1]
        sort_idx = np.argsort(positions_pab)
        positions_pab = positions_pab[sort_idx]
        powers_pab = powers_pab[sort_idx]
        powers = np.interp(positions, positions_pab, powers_pab)
        
        plt.figure(1)
        plt.plot(positions, counts_corrected, '.-')
        plt.figure(2)
        plt.plot(powers, counts_corrected, '.-')
    
    plt.figure(1)
    plt.xlabel('Position (mm)')
    plt.ylabel('Counts (dark-corrected)')
    plt.legend(wavelengths)
    plt.title('Dark-Corrected Counts vs Position')
    plt.figure(2)
    plt.xlabel('Power (mW)')
    plt.ylabel('Counts (dark-corrected)')
    plt.legend(wavelengths)
    plt.title('Dark-Corrected Counts vs Power')
    plt.show()



if __name__ == "__main__":
    plot_pab("pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv")