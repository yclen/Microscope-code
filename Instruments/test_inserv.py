from nspyre import InstrumentManager
import sys


inserv = InstrumentManager()

test = inserv.testclass
v = test.test_method()
print(v)