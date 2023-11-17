import trie
import csv
import model
import os
import re
class AngkorSegmentation:
    DELIMITER = '\t'
    
    # init Class_Function class
    def __init__(self, text, trie_model_filename="train_data_set"):
        self.text = text
        self.model = trie.Trie()
        self.model.load_from_pickle(trie_model_filename)
        self.result = []
        self.result_all = []
        self.leftover = []
        self.startIndex = 0

    def isNumber(self, ch):
        # number letter
        return ch in "0123456789០១២៣៤៥៦៧៨៩"

    def parseNumber(self, index):
        result = ""
        while (index < len(self.text)):
            ch = self.text[index]
            if self.isNumber(ch):
                result += ch
                index += 1
            else:
                return result
        return result

    def isEnglish(self, ch):
        return ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def parseEnglish(self, index):
        result = ""
        while (index < len(self.text)):
            ch = self.text[index]
            if (self.isEnglish(ch) or self.isNumber(ch)):
                result += ch
                index += 1
            else:
                return result
        return result

    def parseTrie(self, index):
        word = ''
        foundWord = ''

        while (index < len(self.text)):
            ch = self.text[index]
            word += ch
            if self.model.searchWordPrefix(word):
                if self.model.searchWord(word):
                    foundWord = word
            elif self.model.searchWord(word):
                return word
            else:
                return foundWord

            index += 1

        return ""

    def check_words(self):
        # Read existing words from CSV file and store them in a list
        existing_words = []
        with open('segmented_text.csv', 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            for row in reader:
                existing_words.append(row[0])

        # Define a regular expression pattern for Khmer characters
        khmer_pattern = re.compile(r'[\u1780-\u17FF]+')
        temp = ""
        while(self.startIndex < len(self.text)):
            ch = self.text[self.startIndex]
            word = ''

            if self.isNumber(ch):
                word = self.parseNumber(self.startIndex)
            elif self.isEnglish(ch):
                word = self.parseEnglish(self.startIndex)
            else:
                word = self.parseTrie(self.startIndex)

            length = len(word)
            if length == 0:
                temp += ch
                self.startIndex += 1
                if self.startIndex >= len(self.text):
                    self.result_all.append(temp)
                    temp = ""
                continue
            if len(temp) > 0:
                self.result_all.append(temp)
                temp = ""

            result = {}
            if self.model.searchWord(word) or self.isNumber(ch) or self.isEnglish(ch):
                result = word
            else:
                result = word

            # Append new words to CSV file
            word_str = ''.join(result)
            if word_str.strip() and word_str not in existing_words and khmer_pattern.search(word_str):
                with open('segmented_text.csv', 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([word_str])
                    existing_words.append(word_str)

            self.result_all.append(result)
            self.startIndex += length
        return self.result_all

    def segment(self, text):
        self.result_all = []
        # zero space
        text = text.replace(' ', '')
        text = text.replace('។', '។ ')
        text = text.replace('៛', '៛ ')
        text = text.replace('៕', '៕ ')
        text = text.replace('ៗ', 'ៗ ')
        for i in range(len(text)):
            self.result_all.append(text[i])
        return self.result_all

    def show(self):
        print("Original Text: " + self.text)

        print("Segment:", self.result_all)

        print('ZeroSpace : [' + '​'.join(self.result_all) + ']')

        print("Total Words:", len(self.result_all))

        # Words not in segmented_text.csv
        existing_words = set()
        with open('segmented_text.csv', 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            for row in reader:
                existing_words.add(row[0])

        words_not_in_csv = [word for word in self.result_all if word.strip() and word not in existing_words]
        if words_not_in_csv:
            print("The words can not be segmented:", words_not_in_csv)


    def save_segmented_text(self, filename):
        if not os.path.isfile(filename):
            # file does not exist, create a new file and save the words
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                for word in self.result_all:
                    if word != ' ':  # exclude spaces
                        writer.writerow([word])
        else:
            # file already exists, open in append mode and only append new words
            existing_words = set()
            with open(filename, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for row in reader:
                    existing_words.add(row[0])
            with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                for word in self.result_all:
                    if word != ' ' and word not in existing_words:  # exclude spaces and duplicates
                        writer.writerow([word])
                        existing_words.add(word)
