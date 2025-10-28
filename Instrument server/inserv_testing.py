from nspyre import InstrumentManager
import numpy as np


class test_class:

    def __init__(self):
        self.name = "test_class"
        print(f"test_class initialized with name {self.name}")

    def test_method(self):
        text = f"test_method called with name {self.name}"
        return text

    def test_return_array(self):

        array = [1, 2, 3, 4, 5]
        array = np.array(array)
        return array




if __name__ == "__main__":

    inserv = InstrumentManager()
    test = inserv.test_class

    result = test.test_method()
    print(result)

    result = test.test_return_array()
    print(result)

    zaber = inserv.zaber
    ND = 3
    zaber.move_to(10, ND)
        


