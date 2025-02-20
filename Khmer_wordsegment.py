import trie
import csv
import pandas as pd
import model
import os
import re
import logging
from typing import List, Tuple

class AngkorSegmentation:
    DELIMITER = '\t'
    KHMER_PATTERN = re.compile(r'[\u1780-\u17D3\u17D7\u17E0-\u17E9\u17F0-\u17F9]+')
    
    def __init__(self, text: str, trie_model_filename: str = "train_data_set"):
        self.text = text
        self.model = trie.Trie()
        try:
            self.model.load_from_pickle(trie_model_filename)
        except FileNotFoundError:
            logging.error(f"Pickle file not found: {trie_model_filename}")
            raise
        except Exception as e:
            logging.error(f"Failed to load trie model from {trie_model_filename}: {e}")
            raise
        self.result = []
        self.result_all = []
        self.leftover = []
        self.startIndex = 0

    @staticmethod
    def isNumber(ch: str) -> bool:
        return ch in "0123456789០១២៣៤៥៦៧៨៩" 

    def parseNumber(self, index: int) -> str:
        result = ""
        while index < len(self.text):
            ch = self.text[index]
            if self.isNumber(ch):
                result += ch
                index += 1
            else:
                break
        return result

    @staticmethod
    def isEnglish(ch: str) -> bool:
        return ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()“ ” " " ‘ ’ ' '"

    def parseEnglish(self, index: int) -> str:
        result = ""
        while index < len(self.text):
            ch = self.text[index]
            if self.isEnglish(ch) or self.isNumber(ch):
                result += ch
                index += 1
            else:
                break
        return result

    def parseTrie(self, index: int) -> str:
        word = ''
        foundWord = ''

        while index < len(self.text):
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

        return foundWord

    def check_words(self) -> List[Tuple[str, str]]:
        existing_words = self._load_existing_words()
        temp = ""
        while self.startIndex < len(self.text):
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
                    self._append_result(temp)
                    temp = ""
                continue
            if len(temp) > 0:
                self._append_result(temp)
                temp = ""
            result = word

            word_str = ''.join(result)
            if word_str.strip() and word_str not in existing_words and self.KHMER_PATTERN.search(word_str):
                self._write_to_csv(word_str)
                existing_words.add(word_str)

            self._append_result(result)
            self.startIndex += length
        return self.result_all

    def _load_existing_words(self) -> set:
        existing_words = set()
        try:
            with open('segmented_text.csv', 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    existing_words.add(row[0])
        except FileNotFoundError:
            logging.warning("segmented_text.csv not found. A new file will be created.")
        except Exception as e:
            logging.error(f"Error reading segmented_text.csv: {e}")
        return existing_words

    def _write_to_csv(self, word_str: str):
        try:
            with open('segmented_text.csv', 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([word_str])
        except Exception as e:
            logging.error(f"Error writing to segmented_text.csv: {e}")

    def _append_result(self, word: str):
        pos = self.model.getWordPos(word) or "N/A"
        if word.strip() and self.KHMER_PATTERN.search(word):
            self.result_all.append((word, pos))

    def segment(self, text: str) -> List[str]:
        self.result_all = []
        text = text.replace(' ', '')
        text = text.replace('។', '។ ')
        text = text.replace('៛', '៛ ')
        text = text.replace('៕', '៕ ')
        text = text.replace('ៗ', 'ៗ ')
        text = text.replace('៘', '')
        text = text.replace('៚', '')
        text = text.replace('៙', '')
        text = text.replace('៖', '')
        for i in range(len(text)):
            self.result_all.append(text[i])
        return self.result_all

    def show(self):
        print(f"\033[1mOriginal Text:\033[0m {self.text}")

        # Create a DataFrame from result_all
        df = pd.DataFrame(self.result_all, columns=['Word', 'POS'])
        df['POS'] = df['POS'].apply(lambda pos: f"\033[1m{pos}\033[0m")

        # Display the DataFrame with left alignment
        print("\033[1msegmentation:\033[0m")
        print(df.to_string(index=False, justify='left'))

        zero_space_result = [word for word, pos in self.result_all if word.strip()]
        print(f'\033[1mZeroSpace : \033[0m [{"​".join(zero_space_result)}]')
        print(f"\033[1mTotal Words:\033[0m {len(df)}")

        existing_words = self._load_existing_words()

        words_not_in_csv = [word for word, pos in self.result_all if word not in existing_words]
        if words_not_in_csv:
            print(f"\033[1mThe words can not be segmented:\033[0m {words_not_in_csv}")

        # Check for English words and other non-Khmer words
        non_khmer_words = [word for word, pos in self.result_all if not self.KHMER_PATTERN.search(word)]
        if non_khmer_words:
            print(f"\033[1mNon-Khmer words:\033[0m {non_khmer_words}")

    def save_segmented_text(self, filename: str, **kwargs):
        try:
            # Create a DataFrame from result_all
            df = pd.DataFrame(self.result_all, columns=['Word', 'POS'])

            # Check the file extension and save accordingly
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False, **kwargs)
            elif filename.endswith('.xlsx'):
                df.to_excel(filename, index=False, engine='openpyxl', **kwargs)
            else:
                raise ValueError("Unsupported file extension. Use .csv or .xlsx")
        except Exception as e:
            logging.error(f"Error handling file {filename}: {e}")

    def print_segmented_words(self):
        try:
            with open('segmented_text.csv', 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                print("\033[1mSegmented Words:\033[0m")
                for row in reader:
                    print(row[0])
        except FileNotFoundError:
            logging.warning("segmented_text.csv not found.")
        except Exception as e:
            logging.error(f"Error reading segmented_text.csv: {e}")