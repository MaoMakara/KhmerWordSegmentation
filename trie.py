import pickle
import json
import logging

class Trie:
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return {"isEndOfWord": False, "children": {}}

    def insertWord(self, word):
        current = self.root
        for ch in word:
            if ch not in current["children"]:
                current["children"][ch] = self.getNode()
            current = current["children"][ch]
        current["isEndOfWord"] = True

    def searchWord(self, word):
        current = self.root
        for ch in word:
            if ch not in current["children"]:
                return False
            current = current["children"][ch]
        return current["isEndOfWord"]

    def searchWordPrefix(self, word):
        current = self.root
        for ch in word:
            if ch not in current["children"]:
                return False
            current = current["children"][ch]
        return bool(current["children"])

    def deleteWord(self, word):
        self._delete(self.root, word, 0)

    def _delete(self, current, word, index):
        if index == len(word):
            if not current["isEndOfWord"]:
                return False
            current["isEndOfWord"] = False
            return len(current["children"]) == 0

        ch = word[index]
        if ch not in current["children"]:
            return False
        node = current["children"][ch]

        should_delete_current_node = self._delete(node, word, index + 1)

        if should_delete_current_node:
            del current["children"][ch]
            return len(current["children"]) == 0

        return False

    def save_to_pickle(self, file_name):
        try:
            with open(file_name + ".pkl", "wb") as f:
                pickle.dump(self.root, f)
        except Exception as e:
            logging.error(f"Error saving to pickle file {file_name}: {e}")

    def load_from_pickle(self, file_name):
        try:
            with open(file_name + ".pkl", "rb") as f:
                self.root = pickle.load(f)
        except FileNotFoundError:
            logging.error(f"Pickle file not found: {file_name}")
        except Exception as e:
            logging.error(f"Error loading from pickle file {file_name}: {e}")

    def save_to_json(self, file_name):
        try:
            with open(file_name + ".json", "w") as f:
                json.dump(self.root, f)
        except Exception as e:
            logging.error(f"Error saving to JSON file {file_name}: {e}")

    def load_from_json(self, file_name):
        try:
            with open(file_name + ".json", "r") as f:
                self.root = json.load(f)
        except FileNotFoundError:
            logging.error(f"JSON file not found: {file_name}")
        except Exception as e:
            logging.error(f"Error loading from JSON file {file_name}: {e}")