from driverslib import my_csv as mc
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

def rolling_derivative(x, y):
    derivatives = []
    indices = []
    for i in range(len(x)):
        slope, intercept = np.polyfit(x[-i:], y[-i:], 1)
        derivatives.append(slope)
        indices.append(i)
    return np.array(derivatives)[50:], np.array(indices)[50:]


def david_3d(power_levels=None, all_waves=True):
    if power_levels is None:
        power_levels = np.linspace(0.5, 10, 20)  # Sample 20 power levels from 0.5 to 10 mW
    
    data = mc.read_csv('jf525_di561_Ex-FGL630M-FELH625.csv')
    table = data.table
    wavelengths = data.wavelengths
    if not all_waves:
        wavelengths = [655, 670, 700, 750, 785]

    pab = mc.read_csv('pab_di785_Ex-FGL630M-FELH625-di561_10nmBW.csv')
    pab_table = pab.table

    # Prepare 3D data arrays
    wavelength_grid = []
    power_grid = []
    counts_grid = []
    exponent_grid = []
    
    exponents = []
    for wavelength in wavelengths:
        positions = table[wavelength][1]
        counts = table[wavelength][2]
        # Filter to only use positions less than 90
        mask = positions < 90
        positions = positions[mask]
        counts = counts[mask]

        positions_pab = pab_table[wavelength][2]
        powers_pab = pab_table[wavelength][1]

        # Sort positions_pab and powers_pab together
        sort_idx = np.argsort(positions_pab)
        positions_pab = positions_pab[sort_idx]
        powers_pab = powers_pab[sort_idx]
        
        powers = np.interp(positions, positions_pab, powers_pab)

        # Calculate exponent for this wavelength
        log_powers = np.log(powers)
        log_counts = np.log(counts)
        # 
        slope, intercept = np.polyfit(log_powers[-50:], log_counts[-50:], 1)
        exponents.append(slope)
        print(f"Slope for wavelength {wavelength} is {slope}")
        
        # Sample counts at different power levels
        for power_level in power_levels:
            if powers.max() >= power_level and powers.min() <= power_level:
                count_at_power = np.interp(power_level, powers, counts)
                wavelength_grid.append(wavelength)
                power_grid.append(power_level)
                counts_grid.append(count_at_power)
                exponent_grid.append(slope)
    
    return (np.array(wavelength_grid), np.array(power_grid), 
            np.array(counts_grid), np.array(exponent_grid))


if __name__ == '__main__':
    # Get 3D data
    wavelengths, powers, counts, exponents = david_3d()
    
    # Create regular grid for surface plot
    wl_grid = np.linspace(wavelengths.min(), wavelengths.max(), 50)
    pw_grid = np.linspace(powers.min(), powers.max(), 50)
    WL, PW = np.meshgrid(wl_grid, pw_grid)
    
    # Interpolate counts and exponents onto regular grid
    points = np.column_stack((wavelengths, powers))
    COUNTS = griddata(points, counts, (WL, PW), method='cubic')
    EXPONENTS = griddata(points, exponents, (WL, PW), method='cubic')
    
    # Create 3D surface plot colored by exponent
    fig = go.Figure(data=[go.Surface(
        x=WL,
        y=PW,
        z=COUNTS,
        surfacecolor=EXPONENTS,
        colorscale='Jet',
        colorbar=dict(title="Power Exponent"),
        cmin=1,
        cmax=2,
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Wavelength (nm)',
            yaxis_title='Power (mW)',
            zaxis_title='Counts',
        ),
        title='3D Surface: Counts vs Wavelength vs Power',
        width=1000,
        height=800,
    )
    
    fig.show()

