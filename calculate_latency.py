import csv, os, json, argparse
from pathlib import Path

def calculate_latencies(fileinput,fileoutput):
    data = {
        "latencies": [],
        "timestamps": []
    }

    with open(fileinput, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        c1polarity, c2polarity, triggertime = 0, 0, 0
        triggerwait = False

        mintime = 0

        n = 0
        for row in csvreader:
            n += 1
            if n < 2:
                continue
            
            time, c1, c2 = [float(i) for i in row]

            mintime = min(time,mintime)

            c1polarity = c1 > 5
            c2polarity = c2 > 5

            if c1polarity != c2polarity and not triggerwait:
                triggertime = time
                triggerwait = True
            if c1polarity == c2polarity and triggerwait:
                data["latencies"].append((time-triggertime)*1000)
                data["timestamps"].append((time-mintime)*1000)
                triggerwait = False
    with open(fileoutput, "w") as f:
        f.write(json.dumps(data))

    print("Finished processing with",len(data["latencies"]),"datapoints. Data saved to",fileoutput)

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
        help="Output JSON file (default: input filename with .json)"
    )

    args = parser.parse_args()

    calculate_latencies(
        args.input,
        args.output or "./latencies/"+args.input.stem+".json"
    )

if __name__ == "__main__":
    main()