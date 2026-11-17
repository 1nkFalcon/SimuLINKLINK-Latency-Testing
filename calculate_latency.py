import csv, os, json

for i in os.listdir():
    splitname = os.path.splitext(i)
    if splitname[-1].lower() == ".csv":
        print(i,"✓" if os.path.exists(splitname[0]+".json") else "X")

file = input("File: ")

filename = os.path.splitext(file)[0]

filejson = filename+".json"

data = []

with open(file, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    c1polarity, c2polarity, triggertime = 0, 0, 0
    triggerwait = False

    n = 0
    for row in csvreader:
        n += 1
        if n < 2:
            continue
        
        time, c1, c2 = [float(i) for i in row]

        c1polarity = c1 > 5
        c2polarity = c2 > 5

        if c1polarity != c2polarity and not triggerwait:
            triggertime = time
            triggerwait = True
        if c1polarity == c2polarity and triggerwait:
            data.append((time-triggertime)*1000)
            triggerwait = False
with open(filejson, "w") as f:
    f.write(json.dumps(data))

print("Finished processing with",len(data),"datapoints. Data saved to ",filejson)