import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import os, json, argparse

from pathlib import Path

def plot_latencies(inputfiles,labels,colors,outputfile,title,show,line):
    data = []

    for i in inputfiles:
        with open(i, "r") as f:
            data.append(json.load(f))

    # plotting

    if line:
        for i in range(len(inputfiles)):
            sns.lineplot(
                x=data[i]["timestamps"],
                y=data[i]["latencies"],
                color=colors[i],
                alpha=0.5,
                label=labels[i],
                marker="o"
            )

        plt.xlabel('Timestamp (ms)')
        plt.ylabel('Latency')
    else:
        for i in range(len(inputfiles)):
            sns.histplot(
                data=data[i]["latencies"],
                color=colors[i],
                alpha=0.5,
                label=labels[i],
                binrange=(0,50),
                binwidth=2,
                kde=True
            )

        plt.xlabel('Latency (ms)')
        plt.ylabel('Frequency')

    # Adding labels and legend
    plt.title(title)
    plt.legend()

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
        "-i","--inputs",
        type=Path,
        nargs="+",
        help="Input json files (ordered)"
    )

    parser.add_argument(
        "-l","--labels",
        nargs="+",
        help="Input labels (ordered)"
    )

    parser.add_argument(
        "-c","--colors",
        nargs="+",
        help="Input colors (ordered, default: red, orange, yellow, green, blue, purple)"
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
        "--line",
        action="store_true",
        help="Use a line graph instead of a histogram"
    )

    parser.add_argument(
        "--hide",
        action="store_true",
        help="Hide resulting graph"
    )

    args = parser.parse_args()

    plot_latencies(
        args.inputs,
        args.labels,
        args.colors or [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple"
        ],
        args.output or "./exports/"+"_".join(args.labels)+".jpg",
        args.title,
        not args.hide,
        args.line
    )

if __name__ == "__main__":
    main()