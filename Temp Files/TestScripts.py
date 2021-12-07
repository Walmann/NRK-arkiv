from tqdm import tqdm
import time

pbar = tqdm(range(100))

x = 0
for i in pbar:
    x += i
    y = x**2
    pbar.set_description("y = %d" % y)
    time.sleep(0.5)
