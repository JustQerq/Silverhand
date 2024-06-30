import numpy as np
import math
import time
import contextlib

@contextlib.contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"Time elapsed: {end - start}s")

def distance(p1, p2):
    return math.sqrt(pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2) + pow((p1[2] - p2[2]), 2))


with timer():
    print(distance([6, 1, 4], [3, 2, 2]))

with timer():
    p1 = np.array([6, 1, 4])
    p2 = np.array([3, 2, 2])
    print(np.linalg.norm(p1-p2))