import TimeTagger
import time
import numpy as np




class TimetaggerDriver:
    def __init__(self, binwidth=10e9, num_bins=5):
        try:
            self.binwidth = binwidth #in ps (10e9 ps is 10ms)
            self.num_bins = num_bins
            print("connecting to timetagger...")
            self.tagger = TimeTagger.createTimeTagger()
            self.tagger.setTriggerLevel(1, 1.0)  # 1V threshold on channel 1
            self.counter = TimeTagger.Counter(self.tagger, channels=[1], binwidth=self.binwidth, n_values=self.num_bins) #binwidth is in ps (10e9 is 10ms)
        except:
            self.binwidth = None
            self.num_bins = None
            self.tagger = None
            self.counter = None
            print("Failed to connect to timetagger")

    def get_counts_per_second(self):
        #returns counts per second
        counts = self.counter.getData()[0]
        return np.mean(counts)*1e12/self.binwidth

    def set_counter(self, binwidth, num_bins):
        self.binwidth = binwidth
        self.num_bins = num_bins
        self.counter = TimeTagger.Counter(self.tagger, channels=[1], binwidth=self.binwidth, n_values=self.num_bins)

    def get_counts(self):
        return self.counter.getData()[0]

    def count_for_time(self, t, n_bins):
        binwidth = t/n_bins
        self.set_counter(binwidth*1e12, n_bins)
        #print(f"counting for {t} seconds")
        while self.counter.getData()[0][0] == 0:
            time.sleep(0)

        time.sleep(t)
        counts = self.get_counts()
        return counts
