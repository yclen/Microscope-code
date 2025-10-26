from driverslib.drivers import ZaberDriver
from driverslib.funcs import set_bandwidth

# Default bandwidth
width = 15

# Setup device
print("Setting up device...")
z = ZaberDriver()
fast_speed = 30



while True:
    # Get wavelength from user
    wavelength = float(input("Enter wavelength (nm): "))



    # Calculate positions
    position1, position2 = set_bandwidth(wavelength, width)

    # Move to positions
    print(f"Setting wavelength to {wavelength} nm with {width} nm bandwidth...")
    z.move_to(position1, 1, velocity=fast_speed)
    z.move_to_waiting(position2, 2, velocity=fast_speed)
    print("Done!")

