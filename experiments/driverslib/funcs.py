import numpy as np
import driverslib.my_csv as mc
import matplotlib.pyplot as plt


def set_bandwidth(wavelength, width):

    #updated 10/9/25
    def wave(position, i):
        if i == 1:
            return -6.05 * position + 938.07
        elif i == 2:
            return -6.13 * position + 956.45
    
    def position(wave, i):
        if i == 1:
            return (wave - 938.07) / -6.05
        elif i == 2:
            return (wave - 956.45) / -6.13

    #wave1 is right and wave2 is left
    wave1 = wavelength + width/2
    wave2 = wavelength - width/2

    position1 = position(wave1, 1)
    position2 = position(wave2, 2)

    return position1, position2







def positions_from_powers(positions, powers, wavelength=800, log=False):
    
    wave = wavelength
    
    # # Filter for positions > 20
    # cutoff = posistions > 10
    # posistions = posistions[cutoff]
    # powers = powers[cutoff]
    
    max_power = powers.max()
    min_power = powers.min()
    max_index = np.where(powers == max_power)[0][0]
    min_index = np.where(powers == min_power)[0][0]
    # print(max_power, min_power)
    # print(max_index, min_index)
    # print(positions[max_index], positions[min_index])

    if log:
        percentages = np.logspace(-6, 0, 100)
    else:
        percentages = np.arange(1, 101, 1)/100
    #percentages = np.logspace(-6, 0, 100)
    power_values = max_power * percentages
    position_values = np.interp(power_values, powers, positions)
    #print(power_values[-1], position_values[-1])

    return position_values, power_values


if __name__ == "__main__":

    csv = mc.read_csv('pab_FELH650_30nmBW-3.csv')
    table = csv.table
    wavelength = 665
    positions = table[wavelength][2]
    powers = table[wavelength][1]
    positions2, powers2 = positions_from_powers(positions, powers, wavelength)

    plt.xlabel('Position (mm)')
    plt.ylabel('Power (mW)')
    plt.title('Power vs Position')
    plt.legend([wavelength])
    plt.plot(positions, powers)
    plt.plot(positions2, powers2, '.')
    plt.show()