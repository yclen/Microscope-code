from driverslib.my_csv import *


def plot1():
    data = read_csv("cvp1.csv")
    
    wavelengths = data.wavelengths
    for wavelength in wavelengths:
        powers = data.table[wavelength][2]
        counts = data.table[wavelength][3]
        plt.plot(powers, counts, '.-')

    plt.xlabel('Power (mW)')
    plt.ylabel('Counts')
    plt.legend(wavelengths)
    plt.title('Counts vs Power')
    plt.show()

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


if __name__ == "__main__":
    plot2()