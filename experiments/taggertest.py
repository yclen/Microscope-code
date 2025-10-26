from driverslib.drivers import *
import numpy as np
import matplotlib.pyplot as plt
import time
from TimeTagger import createTimeTagger, CountBetweenMarkers

def count_test():
    tt = TimetaggerDriver()
    while True:
        counts = tt.get_counts_per_second()
        print(counts)
        time.sleep(0.2)


def histo_test():
    laser = Laser()
    laser.__enter__()
    laser.on()
    print("Laser on..")
    time.sleep(2)
    

    # 1) Open the Time Tagger
    tt = TimetaggerDriver()
    tagger = tt.tagger

    # 2) Assign your physical channels
    LASER_CH  = 3   # your laser sync on channel 3
    PHOTON_CH = 1   # your detector on channel 1

    # 3) Optional: choose edges
    #   +N  = rising edge on channel N
    #   -N  = falling edge on channel N
    start_ch = +LASER_CH
    stop_ch  = +PHOTON_CH

    # 4) (Strongly recommended) Set trigger levels to match your logic
    #    TTL ~1.0–1.5 V usually works well. If your laser/detector is NIM,
    #    you need a discriminator/level converter before the Tagger.
    try:
        tagger.setTriggerLevel(LASER_CH, 1)   # volts
        tagger.setTriggerLevel(PHOTON_CH, 0.075)  # volts
    except Exception:
        # Some models/firmware don’t expose adjustable thresholds—safe to ignore.
        pass

    # 5) (Optional) Add a virtual delay to align signals if needed
    #    e.g., shift laser by +2 ns to center the peak in the window
    #    Comment this out until you know you need it.
    # laser_delayed = TimeTagger.DelayedChannel(tagger, start_ch, delay=2000)  # ps
    # start_for_hist = laser_delayed.getChannel()
    start_for_hist = start_ch

    # 6) Configure the histogram (TCSPC)
    binwidth_ps = 1000    # ps per bin (pick to suit your timing/jitter)
    window_ns  = 50     # total window length you want to see
    n_bins = int((window_ns * 1000) / binwidth_ps)

    hist = TimeTagger.Histogram(
        tagger=tagger,
        click_channel=1,     # photons
        start_channel=3,  # laser sync
        binwidth=binwidth_ps,      # in ps
        n_bins=n_bins
    )

    # 7) Acquire for a while
    acq_time_s = 5.0
    time.sleep(acq_time_s)

    # 8) Read & plot
    counts = hist.getData()
    print(counts)
    print("length:", len(counts))
    print("max:", np.max(counts))
    time_ns = np.arange(len(counts)) * (binwidth_ps * 1e-3)

    laser.off()
    print("Laser off...")

    plt.plot(time_ns, counts)
    plt.xlabel("Delay from laser (ns)")
    plt.ylabel("Counts")
    plt.title("TCSPC Histogram: CH3 (start) → CH1 (stop)")
    plt.show()

    # 9) Cleanup
    del hist
    TimeTagger.freeTimeTagger(tagger)

def cmb_test():
    laser = Laser()
    laser.__enter__()
    laser.on()
    print("Laser on..")
    time.sleep(2)
    
    tt = createTimeTagger()
    c = CountBetweenMarkers(tt, 3, 1, 1000)
    

    data = c.getData()
    print(data)
    print("length:", len(data))
    print("max:", np.max(data))

    laser.off()
    print("Laser off...")

    time_ns = np.arange(len(data)) * (1000 * 1e-3)
    plt.plot(time_ns, data)
    plt.xlabel("Delay from laser (ns)")
    plt.ylabel("Counts")
    plt.title("CMB Histogram: CH3 (start) → CH1 (stop)")

if __name__ == "__main__":
    #histo_test()
    #cmb_test()
    count_test()