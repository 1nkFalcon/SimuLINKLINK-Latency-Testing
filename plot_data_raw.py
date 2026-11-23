import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import csv, os, json, argparse, sys
from pathlib import Path

def plot_raw(fileinput,fileoutput,labels,title,domain,colors,show):
    data = {
        "timestamps": [],
        "c1": [],
        "c2": []
    }

    with open(fileinput, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        mintime = 0

        n = 0
        for row in csvreader:
            n += 1
            if n < 2:
                continue
            
            time, c1, c2 = [float(i) for i in row]

            mintime = min(time,mintime)

            if (time-mintime) > domain[0] and (time-mintime) < domain[1]:
                data["timestamps"].append(time-mintime)
                data["c1"].append(c1)
                data["c2"].append(c2)
    
    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
    
    # We can set the number of bins with the *bins* keyword argument.
    sns.lineplot(
        x=data["timestamps"],
        y=data["c1"],
        color=colors[0],
        label=labels[0]
    )
    sns.lineplot(
        x=data["timestamps"],
        y=data["c2"],
        color=colors[1],
        label=labels[1]
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")

    plt.title(title)

    plt.savefig(fileoutput)

    print("Plot saved to",fileoutput)

    if show:
        plt.show()

def main():
    parser = argparse.ArgumentParser(
        prog='Latency Calculator',
        description='Takes raw csv data from the oscilloscope (time, c1, c2) and outputs the latencies between the signals as a json.',
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input CSV file"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output image file (default: input filename with .json)"
    )

    parser.add_argument(
        "-t", "--title",
        help="Graph title"
    )

    parser.add_argument(
        "-d","--domain",
        nargs=2,
        type=float,
        default=[-100000,1000000],
        help="Domain of the data to plot, as seconds from first sample (default: whole window)."
    )

    parser.add_argument(
        "-l","--labels",
        nargs=2,
        default=["Channel 1","Channel 2"],
        help="Input labels (default: Channel 1, Channel 2)"
    )

    parser.add_argument(
        "-c","--colors",
        nargs=2,
        default=["red","blue"],
        help="Input colors (default: red, blue)"
    )

    parser.add_argument(
        "--hide",
        action="store_true",
        help="Hide resulting graph"
    )

    args = parser.parse_args()

    plot_raw(
        args.input,
        args.output or "./exports/"+args.input.stem+"_raw.jpg",
        args.labels,
        args.title,
        args.domain,
        args.colors,
        not args.hide
    )

if __name__ == "__main__":
    main()