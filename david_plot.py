from driverslib import my_csv as mc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np



def david(power_level=2, plot=True):
    data = mc.read_csv('jf525_col_535-70_2xfesh600_ex_fesh900-felh650.csv')
    table = data.table
    wavelengths = data.wavelengths
    #wavelengths = [655, 670, 700, 750, 785]


    pab = mc.read_csv('pab_FELH650_10nmBW-3.csv')
    pab_table = pab.table

    david_table = {}
    exponents = []
    counts_at_power = []
    for wavelength in wavelengths:
        positions = table[wavelength][1]
        counts = table[wavelength][2]


        positions_pab = pab_table[wavelength][2]
        powers_pab = pab_table[wavelength][1]

        # Debug: check ranges and sorting
        # print(f"positions range: {positions.min():.3f} to {positions.max():.3f}")
        # print(f"positions_pab range: {positions_pab.min():.3f} to {positions_pab.max():.3f}")
        # print(f"positions_pab sorted? {np.all(positions_pab[:-1] <= positions_pab[1:])}")
        
        # Sort positions_pab and powers_pab together
        sort_idx = np.argsort(positions_pab)
        positions_pab = positions_pab[sort_idx]
        powers_pab = powers_pab[sort_idx]
        
        powers = np.interp(positions, positions_pab, powers_pab)


        if plot:
            plt.figure(1)
            plt.plot(positions, counts, '.-')
            plt.figure(2)
            plt.plot(powers, counts, '.-')
            plt.figure(3)
        log_powers = np.log(powers)
        log_counts = np.log(counts)
        slope, intercept = np.polyfit(log_powers[-50:], log_counts[-50:], 1)
        print(f"Slope for wavelength {wavelength} is {slope}")
        if plot:
            plt.plot(log_powers, log_counts, '.-')
            plt.plot(log_powers[-100:], slope*log_powers[-100:] + intercept, '-')

        cap1 = int(np.interp(power_level, powers, counts))
        if powers.max() < power_level:
            cap1 = 0
        #cap2 = counts[np.abs(powers - power_level).argmin()]
        exponents.append(slope)
        counts_at_power.append(cap1)
        print(f"Counts at power {power_level} mW for wavelength {wavelength} is {cap1}")
      
    if plot:
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
        plt.figure(3)
        plt.xlabel('Log Power')
        plt.ylabel('Log Counts')
        plt.legend(wavelengths)
        plt.title('Log-Log Plot')
        plt.show()
    return wavelengths, exponents, counts_at_power




if __name__ == '__main__':
    p = 5
    wavelengths, exponents, counts_at_power = david(power_level=p, plot=False)
    #print(wavelengths, exponents, counts_at_power)
    
    # Convert to numpy arrays
    wavelengths = np.array(wavelengths)
    exponents = np.array(exponents)
    counts_at_power = np.array(counts_at_power)
    
    # Set up figure and axis
    fig, ax = plt.subplots()
    
    # Create colormap normalization
    norm = colors.Normalize(vmin=1, vmax=2.2)
    cmap = cm.jet
    
    # Plot each wavelength segment with color corresponding to its exponent
    for i in range(len(wavelengths) - 1):
        wl_segment = wavelengths[i:i+2]
        cnt_segment = counts_at_power[i:i+2]
        color = cmap(norm(exponents[i]))
        ax.fill_between(wl_segment, cnt_segment, color=color)
    
    # Add colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label="Power exponent")
    
    # Labels and title
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel(f'Counts at {p} mW')
    ax.set_title(f'Counts at {p} mW vs Wavelength')
    plt.show()