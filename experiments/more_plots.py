from driverslib import my_csv as mc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
from scipy.ndimage import gaussian_filter1d
import numpy as np
import numpy as np
from scipy.optimize import least_squares
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import gaussian_filter1d

def get_pab(table, wavelength, plot=True):
    
    positions = table[wavelength][2]
    powers = table[wavelength][1]
    
    
    if plot:
        plt.figure()
        plt.plot(positions, powers, '.-')
        plt.xlabel('Position (mm)')
        plt.ylabel('Power (mW)')
        plt.legend([wavelength])
        plt.title('Power vs Position from pab file')
    
    return positions, powers
        

def counts_vs_position(table, wavelength, plot=True):
    
    
    positions = table[wavelength][1]
    counts = table[wavelength][2]  

    mask = (4.45 < positions) & (positions < 90)
    positions = positions[mask]
    counts = counts[mask]

    if plot:
        plt.figure()
        plt.plot(positions, counts, '.-')
        plt.xlabel('Position (mm)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Counts vs Position')
    
    return positions, counts
        

def counts_vs_power(counts_data, pab_data, wavelength, plot=True):
    positions, counts = counts_data
    positions_pab, powers_pab = pab_data

    sort_idx = np.argsort(positions_pab)
    positions_pab = positions_pab[sort_idx]
    powers_pab = powers_pab[sort_idx]

    powers = np.interp(positions, positions_pab, powers_pab)

    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Counts vs Power')

    return powers, counts


def log_log_plot(powers, counts, wavelength, plot=True):
    log_powers = np.log(powers)
    log_counts = np.log(counts)
    slope, intercept = np.polyfit(log_powers[-50:], log_counts[-50:], 1)
    if plot:
        plt.figure()
        plt.plot(log_powers, log_counts, '--')
        #plt.plot(log_powers, slope*log_powers + intercept, '-')
        plt.xlabel('Log Power')
        plt.ylabel('Log Counts')
        plt.legend([wavelength])
        plt.title('Log-Log Plot')
    return log_powers, log_counts

def quadratic_fit(powers, counts, wavelength, p=2, plot=True):
    # Filter out zero or negative powers to avoid numerical issues
    mask = powers > 0
    x = powers[mask]
    y = counts[mask]

    A = np.column_stack([x**p, x, np.ones_like(x)])  # columns: [x^p, x, 1]
    coeffs, *_ = np.linalg.lstsq(A, y, rcond=None)
    a, b, c = coeffs
    
    # Compute fit on filtered data
    counts_fit = a*x**p + b*x + c
    error = y - counts_fit
    print(f"Mean error: {np.mean(error)}")

    if plot:
        plt.figure()
        plt.plot(x, y, '.-', label='Data')
        plt.plot(x, counts_fit, '-', label='Fit')
        plt.plot(x, error, '-', label='Error')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend()
        plt.title(f'Fit: a*x^{p} + b*x + c')
    return a, b, c

def smooth_fit(powers, counts, wavelength, plot=True):
    window_size = 100
    smoothed_counts = savgol_filter(counts, window_size, 3)
    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-', label='Data')
        plt.plot(powers, smoothed_counts, '-', label='Smoothed')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Smoothed Data')
    return smoothed_counts

def rolling_average(powers, counts, wavelength, window_size=10, plot=True):

    rolling_counts = np.zeros_like(counts)
    for i in range(len(powers)):
        if i < window_size:
            rolling_counts[i] = np.mean(counts[:i+window_size])
        elif i > len(powers)-window_size:
            rolling_counts[i] = np.mean(counts[i-3:])
        else:
            rolling_counts[i] = np.mean(counts[i-window_size:i+window_size])
    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-', label='Data')
        plt.plot(powers, rolling_counts, '--', label='Rolling Average')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Rolling Average')
    return rolling_counts

def spline_fit(powers, counts, wavelength, plot=True):
    powers = np.sort(powers)
    spline = UnivariateSpline(powers, counts, s=10)
    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-', label='Data')
        plt.plot(powers, spline(powers), '--', label='Spline')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Spline Fit')
    return spline


def gaussian_fit(powers, counts, wavelength, plot=True):
    smoothed_counts = gaussian_filter1d(counts, sigma=3)
    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-', label='Data')
        plt.plot(powers, smoothed_counts, '-', label='Gaussian')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Gaussian Fit')
    return smoothed_counts


def polynomial_fit(powers, counts, wavelength, order=2, plot=True):
    coefs = np.polyfit(powers, counts, order)
    counts_fit = np.polyval(coefs, powers)
    if plot:
        plt.figure()
        plt.plot(powers, counts, '.-', label='Data')
        plt.plot(powers, counts_fit, '-', label='Polynomial')
        plt.xlabel('Power (mW)')
        plt.ylabel('Counts')
        plt.legend([wavelength])
        plt.title('Polynomial Fit')

    return counts_fit


def derivative(powers, counts, wavelength, plot=True):
    dcounts = np.gradient(counts, powers)
    if plot:
        plt.figure()
        plt.plot(powers, dcounts, '.-', label='Data')
        plt.xlabel('log(Power (mW))')
        plt.ylabel('d(log(Counts))/d(log(Power))')
        plt.legend([wavelength])
        plt.title('Derivative')
    return dcounts


if __name__ == "__main__":
    data = mc.read_csv('jf525_di561_Ex-FGL630M-FELH625.csv')
    table = data.table
    wavelengths = data.wavelengths[:-1]
    pab = mc.read_csv('pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv')
    pab_table = pab.table



    wavelength = 700
    print(wavelength)


    positions_pab, powers_pab = get_pab(pab_table, wavelength, plot=False)
    positions, counts = counts_vs_position(table, wavelength, plot=False)

    pab_data = (positions_pab, powers_pab)
    counts_data = (positions, counts)



    powers, counts = counts_vs_power(counts_data, pab_data, wavelength, plot=False)
    
    

    g = gaussian_fit(powers, counts, wavelength, plot=False)
    sm = smooth_fit(powers, g, wavelength, plot=False)
    poly = polynomial_fit(powers, sm, wavelength, order=6)
    log_powers, log_counts = log_log_plot(powers, poly, wavelength, plot=True)
    dcounts = derivative(log_powers, log_counts, wavelength, plot=True)
    plt.show()