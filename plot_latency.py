import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import os, json

for i in os.listdir():
    splitname = os.path.splitext(i)
    if splitname[-1].lower() == ".json":
        print(i,"✓" if os.path.exists(splitname[0]+".jpg") else "X")

file = input("File: ")

filename = os.path.splitext(file)[0]

data = []

with open(filename+".json", "r") as f:
    data = json.load(f)

# plotting

bincount = input("Bin count (default 20): ")
if bincount == "":
    bincount = 20

bincount = int(bincount)

fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

# We can set the number of bins with the *bins* keyword argument.
axs.hist(data, bins=bincount)

relaytime = input("Relay Rate (ms): ")
samplingtime = input("Sampling Rate (ms): ")

plt.title(f"SimuLINKLINK Round-Trip Latency ({relaytime}ms Relay / {samplingtime}ms Sampling)")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")

plt.savefig(filename+".jpg")

print("Plot saved to",filename+".jpg")

plt.show()
