from sys import argv, exit
import csv
import re


def main():
    # check Command-line arguments
    if len(argv) != 3:
        exit("Usage: python dna.py database.csv sequence.txt")

    patterns = {}
    persons = {}
    # open database file
    with open(argv[1]) as dbfile:
        dbreader = csv.reader(dbfile)
        for i, row in enumerate(dbreader):
            # get pattern
            if i == 0:
                header = row
                # open sequence file
                with open(argv[2], "r") as sqfile:
                    line = next(sqfile)
                    # get each of pattern sequence
                    for j in range(1, len(row)):
                        matches = list(re.finditer(row[j], line))
                        # Get Maximun repeating
                        if len(matches) > 0:
                            arr = []
                            count = 1
                            next_start = matches[0].end()
                            for match in matches[1:]:
                                if next_start == match.start():
                                    count += 1
                                else:
                                    arr.append(count)
                                    count = 1
                                next_start = match.end()
                            arr.append(count)
                            patterns[row[j]] = max(arr)
                        else:
                            patterns[row[j]] = 0
            # get person STRs
            else:
                person = {}
                for j in range(1, len(row)):
                    # convert string array to int
                    person[header[j]] = int(row[j])
                persons[row[0]] = person

    # print result
    for person in sorted(persons):
        if all([persons[person][pattern] == patterns[pattern] for pattern in sorted(patterns)]):
            print(f"{person}")
            exit(0)
    print("No match")


if __name__ == "__main__":
    main()
