'''
Created on 23.05.2020

@author: Gocht
'''

import csv
import logging

log = logging.getLogger(__name__)


def parse_gendering_wortkatalog_wien(file_name):
    """
    Pases the "corected" "Gendering-Wortkatalog Wien" list from:
    https://www.data.gv.at/katalog/dataset/stadt-wien_genderingwortkatalogderstadtwien
    corected: e.g. randon " removed.
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
    with open(file_name) as f:
        for line in f:
            word = line[:line.find("#")]  # look for comment
            word = word.strip()
            base_words.add(word)
    return base_words


def save_list(file_name, new_word_list):
    with open(file_name, "w", newline='\r\n', encoding="utf-16") as f:  # Windos Style line endings, as we target Word for now
        for word in new_word_list:
            f.write(word + "\n")


def save_failed_list(file_name, failed_words):
    with open(file_name, "w") as f:  # What ever the system understands
        for word in failed_words:
            f.write(word + "\n")


class GenderWords():
    def __init__(self, seperator, camel_case, ignore_words):
        self._seperator = seperator
        self._camel_case = camel_case
        self._ignore_words = ignore_words

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
            if word in self._ignore_words:
                continue
            if word[-2:] == "er":
                new_word = self.gender_word(word)
                self.word_list.add(new_word)
                self.sucessfull_words += 1
            elif word[-1:] == "e":  # risky, but works with ignore-list:
                new_word = self.gender_word(word[:-1])
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
    parser = argparse.ArgumentParser(description='Ließt Gendering-Wortkatalog Wien, und schreibt ein Wordwörterbuch.')
    parser.add_argument("-g", "--gendersperator", type=str, required=True, nargs='?', help="Genderzeichen")
    parser.add_argument("-b", "--binnen_i", type=str2bool, required=True, nargs='?', help="Binnen-I, [ja oder nein]")
    
    parser.add_argument(
        "-o",
        "--gendering-wortkatalog-wien",
        type=str,
        required=False,
        nargs='?',
        help="Gendering-Wortkatalog Wien")
    parser.add_argument(
        "-l",
        "--liste",
        type=str,
        required=False,
        nargs='?',
        help="Zusätzliche Liste mit Wörtern, die zu gendern sind, ein Wort pro Zeile")
    parser.add_argument(
        "-i",
        "--ignore-liste",
        type=str,
        required=False,
        nargs='?',
        help="Liste mit Wörtern, die zu ignorieren sind, ein Wort pro Zeile")
    parser.add_argument(
        "-w",
        "--woerterbuch",
        type=str,
        required=False,
        nargs='?',
        default="gender_liste.dic",
        help="Wörterbuch Name zum Speichern")
    parser.add_argument(
        "-f",
        "--fehler-woerterbuch",
        type=str,
        required=False,
        nargs='?',
        default=None,
        help="Wörterbuch mit Wörtern, die nicht verarbeitet werden können")
    
    parser.add_argument("-v", "--verbose", type=str, required=False, nargs='?', help="LogLevel [DEBUG|INFO|WARNING|ERROR|CRITICAL]")

    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=args.verbose.upper())

    if args.gendering_wortkatalog_wien:
        if not args.ignore_liste:
            raise RuntimeError("\"Gendering-Wortkatalog Wien needs\" --ignore-liste")

    if args.ignore_liste:
        ignore_words = parse_list(args.ignore_liste)
    else:
        ignore_words = []

    gender = GenderWords(args.gendersperator, args.binnen_i, ignore_words)

    if args.gendering_wortkatalog_wien:
        base_words, parsed_lines, skipped_lines = parse_gendering_wortkatalog_wien(args.gendering_wortkatalog_wien)
        print("{} geparste Zeilen. {} übersprungene Zeilen.".format(parsed_lines, skipped_lines))
        gender.gen_list(base_words)

    if args.liste:
        words = parse_list(args.liste)
        gender.gen_list(words)

    save_list(args.woerterbuch, sorted(gender.word_list))
    
    if args.fehler_woerterbuch:
        save_failed_list(args.fehler_woerterbuch, sorted(gender.failed_word_list))

    print("{} Wörter erfolgreich verarbeitet. {} Fehler. {} österreichischer Dialekt".format(
        gender.sucessfull_words, gender.failed_words, gender.dialect_words))
