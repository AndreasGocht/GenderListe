'''
Created on 23.05.2020

@author: Gocht
'''

import csv
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def parse_list(file_name):
    base_words = set()
    with open(file_name) as csvfile:
        wordlist = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for ind, line in enumerate(wordlist):
            try:
                if " " in line[1]:
                    # check for single word in list 
                    continue 
                search_str =  line[2].lower() #check if we can apply "innen"
                
                if "innen" in search_str:
                    log.debug("\"innnen\": {}, {}".format(line, ind))
                    base_words.add(line[1])
                if "in " in search_str:
                    log.debug("\"in \": {}, {}".format(line, ind))
                    base_words.add(line[1])
            except IndexError:
                raise ValueError("Can not parse line {} : \"{}\"".format(ind + 1, line))
    return base_words

def save_list(file_name, new_word_list):
    with open(file_name, "w", newline='\r\n', encoding="utf-16") as f: #Windos Style line endings, as we target Word for now
        for word in new_word_list:
            f.write(word + "\n")
        

class GenderWords():
    def __init__(self, seperator, camel_case):
        self._seperator = seperator
        self._camel_case = camel_case
    
    def gender_word(self, word):
        if self._camel_case:
            return word + self._seperator + "Innen"
        else:
            return word + self._seperator + "innen"
    
    def gen_list(self, base_words):
        new_word_list = []
        for word in sorted(base_words):
            if word[-2:] == "er": 
                new_word = self.gender_word(word)
                new_word_list.append(new_word)
            else:
                logging.error("Can not gender word: {}".format(word))
        return new_word_list
        
        
        
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
    parser.add_argument("-g", "--gendersperator", type=str, required=True, nargs='?', help = "Genderzeichen")
    parser.add_argument("-b", "--binnen_i", type=str2bool, required=True, nargs='?', help = "Binnen-I, [ja oder nein]")
    args = parser.parse_args()
    
    gender = GenderWords(args.gendersperator, args.binnen_i)
    base_words = parse_list("worttabelle.csv")
    new_word_list = gender.gen_list(base_words)
    save_list("gender_liste.dic", new_word_list)
    
    
    
    
    