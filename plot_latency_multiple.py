import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import os, json

for i in os.listdir():
    splitname = os.path.splitext(i)
    if splitname[-1].lower() == ".json":
        print(i)

files = []
labels = []
while True:
    file = input("File: ")
    if file == "":
        break
    elif os.path.exists(file):
        labels.append(input("Label: "))
        files.append(file)
        print(f"File {file} added with label {labels[-1]}")
    else:
        print(f"File {file} not found.")

data = []

for i in files:
    with open(i, "r") as f:
        data.append(json.load(f))

# plotting

bincount = input("Bin count (default 20): ")
if bincount == "":
    bincount = 20

bincount = int(bincount)

colors = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue"
]

for i in range(len(files)):
    sns.histplot(
        data=data[i],
        color=colors[i],
        alpha=0.5,
        label=labels[i],
        binrange=(0,50),
        binwidth=2,
        kde=True
    )

# Adding labels and legend
samplingtime = input("Sampling time: ")
plt.title(f"SimuLINKLINK Round-Trip Latency ({samplingtime}ms Sampling)")

plt.xlabel('Latency (ms)')
plt.ylabel('Frequency')
plt.legend()

plt.show()