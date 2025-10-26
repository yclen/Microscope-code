import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 10, 100)
#y = 2*x**1.5 + 3*x + 5 + np.random.randn(100)
y = x**2 + 0*x + 1


plt.figure()
plt.plot(x, y, '.-')
plt.figure()
plt.plot(np.log(x), np.log(y), '.-')
plt.show()