import trie
import model

class AngkorSegmentation:
# init Class_Function class
  def __init__(self, text):
    self.text = text#.decode('utf-8')
    self.model = trie.Trie()
    self.model.load_from_pickle("train_data_set")
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
      ch = ch#.encode('utf-8')
      if self.isNumber(ch):
        result += self.text[index]
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
      ch = ch#.encode('utf-8')
      if (self.isEnglish(ch) or self.isNumber(ch)):
        result += ch;
        index += 1
      else:
        return result
    return result

  def parseTrie(self, index):
    word = ''
    foundWord = ''

    while (index < len(self.text)):
      ch = self.text[index]
      ch = ch#.encode('utf-8')
      word += ch
      if self.model.searchWordPrefix(word):
        if self.model.searchWord(word):
          foundWord = word
      elif self.model.searchWord(word):
        return word
      else:
        return foundWord;

      index += 1

    return ""

  def check_words(self):
    temp = ""
    while(self.startIndex < len(self.text)):
      ch = self.text[self.startIndex]
      ch = ch#.encode('utf-8')
      word = ''

      if self.isNumber(ch):
        word = self.parseNumber(self.startIndex)#.encode('utf-8')
      elif self.isEnglish(ch):
        word = self.parseEnglish(self.startIndex)#.encode('utf-8')
      else:
        word = self.parseTrie(self.startIndex)

      length = len(word)#.decode('utf-8'))
      if length == 0:
        temp += ch
#         self.result_all.append(ch)#.decode('utf-8'))
        self.startIndex += 1
        if self.startIndex >= len(self.text):
            self.result_all.append(temp)
            temp = ""
        continue
        if len(temp) > 0:
            self.resulf_all.append(temp)
            temp = ""

      result = {}
      if self.model.searchWord(word) or self.isNumber(ch) or self.isEnglish(ch):
        #self.result_all.append()
        result = word#.decode('utf-8')
      else:
        result = word#.decode('utf-8')

      self.result_all.append(result)
      self.startIndex += length
    return(self.result_all)
  
  def show(self):
    print("Original Text: " + self.text)
    print("Segment:",self.result_all)
    print ('ZeroSpace : [' + '​'.join(self.result_all) + ']') # add zero space
    #print ('After check : [' +' '.join(self.result_all) + ']')
    print("Total Words:" , len(self.result_all))
    
  


 
