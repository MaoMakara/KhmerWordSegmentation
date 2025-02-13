from trie import Trie
import logging
import csv
import pickle

def train_model(input_file_path, output_model_path):
    model = Trie()
    
    try:
        with open(input_file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            words = [(row[0], row[1]) for row in reader if row]  # Read word and POS
    except FileNotFoundError:
        logging.error(f"File not found: {input_file_path}")
        return
    except Exception as e:
        logging.error(f"Error reading file {input_file_path}: {e}")
        return

    print("Training Words ...")

    for word, pos in words:
        if word.strip():
            model.insertWord(word, pos)  # Insert word with POS

    try:
        model.save_to_pickle(output_model_path)  # Save the Trie structure
    except Exception as e:
        logging.error(f"Error saving model to {output_model_path}: {e}")
        return

    print("Training Words Successful !!")

if __name__ == "__main__":
    input_file_path = "data/khmer_dictionary.csv"
    output_model_path = "train_data_set"
    train_model(input_file_path, output_model_path)