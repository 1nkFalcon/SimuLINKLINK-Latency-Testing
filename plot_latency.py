import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import os, json, argparse, pandas

from pathlib import Path

def plot_latency(inputfile,outputfile,bins,title,show,graph):
    data = []

    with open(inputfile, "r") as f:
        data = json.load(f)

    # plotting

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    # We can set the number of bins with the *bins* keyword argument.
    match graph:
        case "hist":
            sns.histplot(data["latencies"], bins=bins,stat="percent")
            plt.xlabel("Latency (ms)")
            plt.ylabel("Frequency (Percent)")
        case "line":
            sns.lineplot(x=data["timestamps"],y=data["latencies"],marker="o")
            plt.xlabel("Time (ms)")
            plt.ylabel("Latency (ms)")
        case "box":
            sns.boxplot(x=data["latencies"])
            plt.xlabel("Time (ms)")
        case "none":
            pass
        case _:
            raise Exception(f"Graph type {graph} not supported.")

    plt.title(title)

    if graph != "none":
        plt.savefig(outputfile)

        print("Plot saved to",outputfile)

    if show and graph != "none":
        plt.show()

    print(pandas.Series(data["latencies"],name="Latencies").describe())

def main():
    parser = argparse.ArgumentParser(
        prog='Latency Grapher',
        description='Takes a json of latencies (ms) and plots a graph of the data. Also prints summary statistics of the dataset.',
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
        "-g", "--graph",
        default="hist",
        help="Graph type (hist, line, box, none. default: hist)"
    )

    parser.add_argument(
        "--hide",
        action="store_true",
        help="Hide resulting graph"
    )

    args = parser.parse_args()

    plot_latency(
        args.input,
        args.output or "./exports/"+args.input.stem+"_"+args.graph+".jpg",
        args.bins,
        args.title,
        not args.hide,
        args.graph
    )

if __name__ == "__main__":
    main()