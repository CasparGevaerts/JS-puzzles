import numpy as np

from scipy.integrate import dblquad

# Define the probability of the point existing. This is two semi-cirkles that go through point A, with the corners of the square being their centre, excluding their overlap.
def compute_probability(x, y):
    R = np.sqrt(x ** 2 + y ** 2)
    r = np.sqrt(x ** 2 + (1 - y) ** 2)
    area_c1 = np.pi * R**2
    area_c2 = np.pi * r**2
    d = 1
    part1 = R ** 2 * np.arccos((d ** 2 + R ** 2 - r ** 2) / (2 * d * R))
    part2 = r ** 2 * np.arccos((d ** 2 + r ** 2 - R ** 2) / (2 * d * r))
    part3 = 0.5 * np.sqrt((-d + R + r) * (d + R - r) * (d - R + r) * (d + R + r))
    area_overlap = part1 + part2 - part3
    return 1/4 * area_c1 + 1/4 * area_c2 - area_overlap

# Compute the integral over 1/8th of the total area (the other parts have the same value due to symmetries.
area = dblquad(compute_probability,0, 0.5, 0, lambda x: x)
# Multiply by 8 to get the total value.
answer = area[0]*8
print(answer)
