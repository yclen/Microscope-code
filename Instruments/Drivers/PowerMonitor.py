from pyvisa import ResourceManager






class PM100D:
    def __init__(self, address=ResourceManager().list_resources()[0]):
        """
        Args:
            address: PyVISA resource path.
        """
        try:
            self.rm = ResourceManager()
            self.address = address
            print(f"Connecting to PM100D @ [{self.address}]")
        except:
            self.rm = None
            self.address = None
            print("Failed to connect to PM100D")
            

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def __str__(self):
        return f'{self.address} {self.idn}'

    def open(self):
        try:
            try:
                self.device = self.rm.open_resource(self.address)
            except Exception as err:
                raise ConnectionError(f'Failed connecting to PM100D @ [{self.address}]') from err
            # 1 second timeout
            self.device.timeout = 1000
            self.idn = self.device.query('*IDN?')
            
            return self
        except:
            self.device = None
            self.address = None
            print("Failed to connect to PM100D")
            return None

    def close(self):
        try:
            self.device.close()
        except:
            print("Failed to close PM100D")

    def idn(self):
        try:
            return self.device.query('*IDN?')
        except:
            print("Failed to get IDN")
            return None

    def power(self):
        return float(self.device.query('MEAS:POWER?'))

    def get_correction_wavelength(self):
        return float(self.device.query('SENS:CORR:WAV?'))

    def set_correction_wavelength(self, wavelength):
        self.device.write('SENSE:CORRECTION:WAVELENGTH {}'.format(wavelength))

    def correction_wavelength_range(self):
        cmd = 'SENSE:CORRECTION:WAVELENGTH? {}'
        cmd_vals = ['MIN', 'MAX']
        return tuple(float(self.device.query(cmd.format(cmd_val))) for cmd_val in cmd_vals)