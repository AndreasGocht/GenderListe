'''
Created on 23.05.2020

@author: Gocht
'''

import csv
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def parse_list_oesterreich(file_name):
    """
    Pases the "corected" list from:
    https://www.data.gv.at/katalog/dataset/stadt-wien_genderingwortkatalogderstadtwien
    e.g. randon " removed
    """
    base_words = set()
    parsed_lines = 0
    skipped_lines = 0
    with open(file_name) as csvfile:
        wordlist = csv.reader(csvfile, delimiter=',', quotechar="\"")
        next(wordlist)
        for ind, line in enumerate(wordlist):
            try:
                if " " in line[1]:
                    # check for single word in list
                    skipped_lines += 1
                    continue

                parsed_lines += 1
                search_str = line[2].lower()  # check if we can apply "innen"

                if "innen" in search_str:
                    log.debug("\"innnen\": {}, {}".format(line, ind))
                    base_words.add(line[1])
                elif "in " in search_str:
                    log.debug("\"in \": {}, {}".format(line, ind))
                    base_words.add(line[1])
                else:
                    skipped_lines += 1
            except IndexError:
                raise ValueError("Can not parse line {} : \"{}\"".format(ind + 1, line))
    return base_words, parsed_lines, skipped_lines


def parse_list(file_name):
    """
    Pases any list, one word per line
    """
    base_words = set()
    with open(file_name) as csvfile:
        word = csvfile.readline().strip()
        base_words.add(word)
    return word


def save_list(file_name, new_word_list):
    with open(file_name, "w", newline='\r\n', encoding="utf-16") as f:  # Windos Style line endings, as we target Word for now
        for word in new_word_list:
            f.write(word + "\n")


def save_failed_list(file_name, failed_words):
    with open(file_name, "w") as f:  # What ever the system understands
        for word in failed_words:
            f.write(word + "\n")


class GenderWords():
    def __init__(self, seperator, camel_case):
        self._seperator = seperator
        self._camel_case = camel_case
        self.sucessfull_words = 0
        self.failed_words = 0
        self.dialect_words = 0
        self.word_list = set()
        self.failed_word_list = set()

    def gender_word(self, word):
        if self._camel_case:
            return word + self._seperator + "Innen"
        else:
            return word + self._seperator + "innen"

    def gen_list(self, base_words):
        for word in sorted(base_words):
            if word[-2:] == "er":
                new_word = self.gender_word(word)
                self.word_list.add(new_word)
                self.sucessfull_words += 1
            elif word[-3:] == "ern":
                logging.warning("Dialact word: {}, skip".format(word))
                self.dialect_words += 1
            else:
                self.failed_words += 1
                self.failed_word_list.add(word)


if __name__ == "__main__":

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('ja', 'yes', 'true', 'j', 't', 'y', '1'):
            return True
        elif v.lower() in ('nein', 'no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    import argparse
    parser = argparse.ArgumentParser(description='Ließt Österreichische Genderliste, und schreibt ein Worddictonary.')
    parser.add_argument("-g", "--gendersperator", type=str, required=True, nargs='?', help="Genderzeichen")
    parser.add_argument("-b", "--binnen_i", type=str2bool, required=True, nargs='?', help="Binnen-I, [ja oder nein]")

    parser.add_argument(
        "-o",
        "--oesterreich_gernder_liste",
        type=str,
        required=False,
        nargs='?',
        help="Österreichische Genderliste")
    parser.add_argument(
        "-l",
        "--liste",
        type=str,
        required=False,
        nargs='?',
        help="Liste mit Wörtern, die zu Gendern sind")
    parser.add_argument(
        "-w",
        "--woerterbuch",
        type=str,
        required=False,
        nargs='?',
        default="gender_liste.dic",
        help="Wöterbuch Name zum Speichern")
    parser.add_argument(
        "-f",
        "--fehler-woerterbuch",
        type=str,
        required=False,
        nargs='?',
        default="fehler_woerter.txt",
        help="Wöterbuch mit Wörtern, die nicht verarbeitet werden können")

    args = parser.parse_args()

    gender = GenderWords(args.gendersperator, args.binnen_i)

    if args.oesterreich_gernder_liste:
        base_words, parsed_lines, skipped_lines = parse_list_oesterreich(args.oesterreich_gernder_liste)
        print("{} Geparste Zeilen. {} Übersprungene Zeilen.".format(parsed_lines, skipped_lines))
        gender.gen_list(base_words)

    if args.liste:
        words = parse_list(args.liste)
        gender.gen_list(words)

    save_list(args.woerterbuch, gender.word_list)
    save_failed_list(args.fehler_woerterbuch, gender.failed_word_list)

    print("{} Wörter erfolgreich verarbeitet. {} Fehler. {} Österreichischer Dialekt".format(
        gender.sucessfull_words, gender.failed_words, gender.dialect_words))
