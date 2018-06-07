import csv
import sys

def main():

    myfile = sys.argv[1]
    us_file = sys.argv[2]
    nonus_file = sys.argv[3]
    accent_file = sys.argv[4]
    us_accent = ""
    non_us = ""
    us_utterances = ""
    non_us_utterances = ""
    accent_lines = ""

    with open(myfile, newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='|', lineterminator=',,,,')
        rows = 0
        for row in my_reader:
            full_file = row[0]
            if rows == 0:
                rows += 1
                continue
            filename = full_file.split("/")[1].split(".")[0]
            utterance = row[1]
            accent = row[6]
            #print(accent)
            if accent == "us":
                us_accent = us_accent + "{}: {}\n".format(filename, utterance)
                us_utterances = us_utterances + utterance + "\n"
            elif accent:
                non_us = non_us + "{}: {}\n".format(filename, utterance)
                accent_lines = accent_lines + filename + " " + accent + "\n"
                non_us_utterances = non_us_utterances + utterance + "\n"
            rows += 1

    with open(accent_file, 'w') as accentf:
        accentf.write(accent_lines)

    with open(us_file, "w") as f:
        f.write(us_accent)

    with open(nonus_file, "w") as nonu:
        nonu.write(non_us)

if __name__ == "__main__":
    main()