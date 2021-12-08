



from tqdm import tqdm
from time import sleep
from tqdm.std import trange
from yt_dlp import YoutubeDL
import sys

url = "https://tv.nrk.no/serie/fleksnes/1995/FKUN89000295"


# yt_dlp_options = {
#         # "outtmpl": "%(id)s%(ext)s",
#         # "noplaylist": True,
#         # "quiet": True,
#         # "format": "bestvideo",
#     }

# # org_stout = sys.stdout
# # sys.stdout = tqdm.write(msg)
# for i in trange(100, desc="Progress: ", leave=False, file=sys.stdout):
#     ytdl = YoutubeDL(yt_dlp_options).extract_info(url, download=False)

import inspect
import contextlib
import tqdm
import time

@contextlib.contextmanager
def redirect_to_tqdm():
    # Store builtin print
    old_print = print
    def new_print(*args, **kwargs):
        # If tqdm.tqdm.write raises error, use builtin print
        try:
            tqdm.tqdm.write(*args, **kwargs)
        except:
            old_print(*args, ** kwargs)

    try:
        # Globaly replace print with new_print
        inspect.builtins.print = new_print
        yield
    finally:
        inspect.builtins.print = old_print


def tqdm_redirect(*args, **kwargs):
    with redirect_to_tqdm():
        for x in tqdm.tqdm(*args, **kwargs):
            yield x

for i in tqdm_redirect(YoutubeDL().extract_info(url, download=False)):
    # ytdl = YoutubeDL().extract_info(url, download=False)
    print(i)


print('Done!')