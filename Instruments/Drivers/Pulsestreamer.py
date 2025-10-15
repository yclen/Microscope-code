from pulsestreamer import PulseStreamer, Sequence, OutputState



class pulsestreamer:

    def __init__(self, ip_address='192.168.0.100'):
        try:
            self.ps = PulseStreamer(ip_address)
            print("PulseStreamer connected")
        except:
            self.ps = None
            print("Failed to connect to PulseStreamer")

    def output_state(self, pixel_clk, x, y):
        return OutputState(pixel_clk, x, y)



