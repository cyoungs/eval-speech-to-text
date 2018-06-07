import sys
from difflib import SequenceMatcher
import numpy


def main():
    parsed_sentences = sys.argv[1]
    gold_standard = sys.argv[2]
    output_file = sys.argv[3]

    gold_dict = {}
    parsed_dict = {}

    # split on colon
    # first one, compare, if same: compare
    # if

    #a = "The quick brown fox jumped over the lazy brown dog"
    #b = "The quick brown fox jumped over the lazy brown cat"


    with open(gold_standard, 'r') as gold:
        for line in gold:
            filename, text = line.split(":")
            filename = filename.split(".")[0]
            gold_dict[filename.strip()] = cleanText(text.strip())

    with open(parsed_sentences, 'r') as parsed:
        total_count = 0
        incorrect_count_sentences = 0
        perfect_count = 0
        unparseable = 0
        wer_total = 0
        with open(output_file, 'w') as f:
            for linep in parsed:
                filenamep, text_init = linep.split(":")
                textp = cleanText(text_init.strip())
                filenamep = filenamep.split(".")[0]
                if filenamep in gold_dict:
                    total_count += 1
                    if textp == "google speech didn't recognize this file":
                        unparseable += 1
                        f.write("gold: {}: {}\n".format(filenamep, textp))
                        f.write("parsed: {}: {}\n\n".format(filenamep, gold_text))
                        continue
                    gold_text = gold_dict[filenamep]
                    ratio = SequenceMatcher(None, textp, gold_text).ratio()
                    wer = int(werCalc(linep.strip().split(), gold_text.strip().split()))
                    wer_total += wer
                    print(ratio)
                    parsed_dict[filenamep] = [textp, ratio]
                    if ratio < 1:
                        f.write("\n{}\n".format(ratio))
                        f.write("parsed: {}: {}\n".format(filenamep, textp))
                        f.write("gold: {}: {}\n\n".format(filenamep, gold_text))
                        correct_count, incorrect_count, incorrect_gold, incorrect_token = compareTokens(gold_text, textp)
                        f.write("wer: {}\n".format(str(wer)))
                        f.write("correct: {}, incorrect: {}\n\n".format(correct_count, incorrect_count))
                        f.write("incorrect tokens, gold vs parsed: \n{} \n{}\n\n".format(incorrect_gold, incorrect_token))
                        incorrect_count_sentences += 1

                    else:
                        perfect_count += 1

            f.write("ratio: {}\n".format(1-(perfect_count/(total_count))))
            f.write("average wer: {}\n".format(wer_total/(total_count)))
            f.write("total parsed: {}\n".format(total_count-unparseable))
            f.write("right: {}\n".format(perfect_count))
            f.write("unparsed: {}\n".format(unparseable))
            f.write("incorrect sentences: {}\n".format(incorrect_count_sentences))
            f.write("total utterances: {}\n".format(total_count))


            #parsed_dict[filenamep.strip()] = textp.strip()


    print("NO")

def cleanText(text_str):
    tokens = text_str.strip().split()
    new_tokens = ""
    for token in tokens:
        token = token.lower()
        new_tokens = new_tokens + token + " "

    return new_tokens.strip()

def compareTokens(goldstr1, tokenstr2):
    goldtokens = goldstr1.strip().split()
    tokens2 = tokenstr2.strip().split()
    correct_count = 0
    incorrect_count = 0
    incorrect_gold = []
    incorrect_tok = []

    iter_index = 0
    while iter_index < len(goldtokens):
        gt = goldtokens[iter_index]
        try:
            t2 = tokens2[iter_index]
        except:
            return correct_count, incorrect_count, incorrect_gold, incorrect_tok
        if gt == t2:
            correct_count += 1
        else:
            incorrect_count += 1
            incorrect_gold.append(gt)
            incorrect_tok.append(t2)
        iter_index += 1

    return correct_count, incorrect_count, incorrect_gold, incorrect_tok


def werCalc(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """

    # initialisation
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()