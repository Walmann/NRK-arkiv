


# _break = "brseak"
# partall = 0
# oddetall = 0
# for i in range(100000):
#     remainer = i % 2
#     if remainer == 0:
#         partall = i
        
#     else: oddetall = i

#     print(
#         "Siste partall: " + str(partall),
#         "Siste oddetall: " + str(oddetall)
#         , sep="\n")

from time import time
from tqdm import tqdm

LOOP = 5000

def task(update_cycle):
    pbar = tqdm(total=LOOP)
    for i, _ in enumerate(range(LOOP)):
        for _ in range(LOOP):
            pass

        if i % update_cycle == 0:
            pbar.update(update_cycle)

    pbar.close()

tic = time()
print(f'Update cycle: {1}')
task(1)
toc = time()
print(f'Time elapsed: {toc-tic:0.2f} seconds\n')

tic = time()
print(f'Update cycle: {500}')
task(500)
toc = time()
print(f'Time elapsed: {toc-tic:0.2f} seconds')