import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import os, json, argparse

from pathlib import Path

def plot_latency(inputfile,outputfile,bins,title,show,line):
    data = []

    with open(inputfile, "r") as f:
        data = json.load(f)

    # plotting

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    # We can set the number of bins with the *bins* keyword argument.
    if line:
        axs.plot(data["timestamps"],data["latencies"],marker="o")
        plt.xlabel("Time (ms)")
        plt.ylabel("Latency (ms)")
    else:
        axs.hist(data["latencies"], bins=bins)
        plt.xlabel("Latency (ms)")
        plt.ylabel("Frequency")

    plt.title(title)

    plt.savefig(outputfile)

    print("Plot saved to",outputfile)

    if show:
        plt.show()

def main():
    parser = argparse.ArgumentParser(
        prog='Latency Grapher',
        description='Takes a json of latencies (ms) and plots a histogram.',
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input json file"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output jpg file (default: input filename with .jpg)"
    )

    parser.add_argument(
        "-b", "--bins",
        type=int,
        default=20,
        help="Number of bins (default: 20)"
    )

    parser.add_argument(
        "-t", "--title",
        help="Title for the graph"
    )

    parser.add_argument(
        "-l", "--line",
        action="store_true",
        help="Use a line graph instead of a histogram"
    )

    parser.add_argument(
        "--hide",
        action="store_true",
        help="Hide resulting graph"
    )

    args = parser.parse_args()

    plot_latency(
        args.input,
        args.output or "./exports/"+args.input.stem+("_line" if args.line else "_hist")+".jpg",
        args.bins,
        args.title,
        not args.hide,
        args.line
    )

if __name__ == "__main__":
    main()