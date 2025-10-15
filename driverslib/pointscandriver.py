import math
import time
import matplotlib.pyplot as plt
import numpy as np
from pulsestreamer import PulseStreamer, Sequence, OutputState
from TimeTagger import createTimeTagger, CountBetweenMarkers



class pointscandriver:

    PIXEL_START_CH = 2
    SPD_CH = 1
    volts_per_micron = 2/400

    def __init__(self):
        try:
            # connect to Time Tagger
            print("connecting to time tagger...")
            self.tt = createTimeTagger()
            self.tt.setTriggerLevel(self.PIXEL_START_CH, 1)
            self.tt.setTriggerLevel(self.SPD_CH, 1)
            print("time tagger connected")

             # connect to Pulse Streamer
            self.ps = PulseStreamer('192.168.0.100')
            print("pulse streamer connected")
        except Exception as e:
            print(f"Error connecting to Hardware. Check connections: {e}")
            raise e


    def generate_sequence(self, scan_range_x, scan_range_y, pixel_size, dwell_time, center_pos_x=0, center_pos_y=0, block=True):
        
        # convert to ns and round
        dwell_time_ns = np.round(dwell_time * 1e9)
        
        # calculate number of pixels
        self.npixels_x = math.ceil(scan_range_x / pixel_size)
        self.npixels_y = math.ceil(scan_range_y / pixel_size)
        self.npixels = self.npixels_x * self.npixels_y
        

        # calculate X and Y positions
        x_pts_m = np.linspace(center_pos_x - self.npixels_x*pixel_size/2, center_pos_x + self.npixels_x*pixel_size/2, self.npixels_x)
        y_pts_m = np.linspace(center_pos_y - self.npixels_y*pixel_size/2, center_pos_y + self.npixels_y*pixel_size/2, self.npixels_y)
        
        # convert to volts
        x_pts_volts = x_pts_m * 1e6 * self.volts_per_micron
        y_pts_volts = y_pts_m * 1e6 * self.volts_per_micron
        
        wait_time = 1000e3
        line_return_time = 1000e3  # time to move between lines
        
        # initialize pulse patterns
        galvo_x_volts = [(wait_time, x_pts_volts[0])]
        galvo_y_volts = [(wait_time, y_pts_volts[0])]
        pixel_clk = [(wait_time, 0)]
        
        # generate sequence for entire image
        for y_volts in y_pts_volts:
            for x_volts in x_pts_volts:
                # add pixel data
                galvo_x_volts.append((dwell_time_ns, x_volts))
                galvo_y_volts.append((dwell_time_ns, y_volts))
                pixel_clk.append((dwell_time_ns - 10, 1))
                pixel_clk.append((10, 0))
            
            # add line return (move to start of next line)
            if y_volts != y_pts_volts[-1]:  # not the last line
                galvo_x_volts.append((line_return_time, x_pts_volts[0]))
                galvo_y_volts.append((line_return_time, y_volts))
                pixel_clk.append((line_return_time, 0))
        
        # final state
        self.final_state = OutputState([], x_pts_volts[0], y_pts_volts[0])
        
        # calculate sequence statistics
        total_duration_ns = sum([pulse[0] for pulse in galvo_x_volts])
        total_duration_s = total_duration_ns / 1e9
        total_pulses = len(galvo_x_volts) + len(galvo_y_volts) + len(pixel_clk)
        
        # create and run sequence
        self.sequence = self.ps.createSequence()
        self.sequence.setDigital(0, pixel_clk)
        self.sequence.setAnalog(0, galvo_x_volts)
        self.sequence.setAnalog(1, galvo_y_volts)
        
        print(f"Sequence generated")
        print(f"Total duration: {total_duration_s:.3f} seconds")
        print(f"Total pulses: {total_pulses:,}")

    def fullscan(self, block=True):
        cbm = CountBetweenMarkers(self.tt, self.SPD_CH, self.PIXEL_START_CH, n_values=self.npixels)
        time.sleep(0.1)
        self.ps.stream(self.sequence, n_runs=1, final=self.final_state)
        
        if block:
            while not self.ps.hasFinished():
                time.sleep(0.0001)
        
        data = cbm.getData()
        print(data.shape)
        # Preallocate an empty 2D array
        img = data.reshape(self.npixels_y, self.npixels_x)
        # remove the last pixel of each row which is overexposed due to the galvo moving to the next line
        # remove the last row of pixels because ?
        img = img[0:-1, 0:-1]

        return img


if __name__ == "__main__":
    a = 1
    b = 0.1
    scan_range_x = 300e-6 * b
    scan_range_y = 300e-6 * b
    pixel_size = 1e-6 / a
    dwell_time = 0.1e-3
    center_pos_x = 0 
    center_pos_y = 0
    ps = pointscandriver()
    ps.generate_sequence(scan_range_x, scan_range_y, pixel_size, dwell_time, center_pos_x, center_pos_y)

    for i in range(50):
        img = ps.fullscan()
        plt.imshow(img, origin='lower', interpolation='nearest', cmap='gray')
        plt.colorbar(label="counts")
        plt.show()