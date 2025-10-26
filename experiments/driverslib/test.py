import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1, 10, 100)
y = 2*x**1.5 + 3*x + 5 + np.random.randn(100)

p = 1.5  # known exponent
A = np.column_stack([x**p, x, np.ones_like(x)])  # columns: [x^p, x, 1]
coeffs, *_ = np.linalg.lstsq(A, y, rcond=None)
a, b, c = coeffs
print(a, b, c)
plt.plot(x, y, '.-')
plt.plot(x, a*x**p + b*x + c, '-')
plt.show()