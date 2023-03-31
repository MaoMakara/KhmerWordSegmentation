import trie
model=trie.Trie()
input_file_path = "data/khmerwords.csv"
with open(input_file_path, "r",encoding="'utf-8-sig") as f:
  words = f.read().split("\n")
  f.close()
#print("Training Words ...")


for word in words:
  if not bool(word.strip()):
    continue
  model.insertWord(word)
model.save_to_pickle("train_data_set")

#print("Training Words Successful !!")
