import pandas as pd
import nltk
import nltk.data
nltk.download('punkt')
from nltk.tokenize import word_tokenize
sno = nltk.stem.SnowballStemmer('english')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

class Extractor:

  def __init__(self):
    self.KeyWordsFile = None
    self.RawTextFile = None
    self.Data = []
    self.MetaData = {}
    self.ExtractedData = {}

  def get_files(self):
    try:
      self.KeyWordsFile = open(r"C:\ExtractIt\KeyWords.txt")
      self.RawTextFile = open(r"C:\ExtractIt\raw_data.txt")
    except FileNotFoundError:
      print("We could not find the required Files(KeyWords.txt and raw_data.txt) in the C:\ExtractIt\ directory, so you can mention the whole path of the raw_data and KeyWords file here. Please do keep both of them in the same directory in .txt format and then give the path of the directory. I can wait")
      basePath = input("Enter directory path : ")
      self.KeyWordsFile = open(basePath + r"\KeyWords.txt")
      self.RawTextFile = open(basePath + r"\raw_data.txt")
  
  def get_sentences(self):
    with self.RawTextFile as f:
      content = f.read()
    
    for sentences in tokenizer.tokenize(content):
      self.Data.append(sentences)
  
  def get_stemmed_keys(self):
    
    with self.KeyWordsFile as f:
      for line in f.read().splitlines():
        for words in word_tokenize(line):
          self.MetaData[sno.stem(words)] = line
  
  def extract(self):
    for sentence in self.Data:
      for word in word_tokenize(sentence):
        if sno.stem(word) in self.MetaData:
          self.ExtractedData[sentence] = self.MetaData[sno.stem(word)] + "--->" + word
  
  def output(self):
    all_tuples = []
    for key, value in self.ExtractedData.items():
      all_tuples.append(tuple((key,value)))
    extracted_df = pd.DataFrame(all_tuples, columns = ["DATA", "CLAUSE"], index = [i for i in range(len(self.ExtractedData))])
    extracted_df.to_excel(r"C:\ExtractIt\raw_output.xlsx")
  
  def run(self):
    self.get_files()
    self.get_sentences()
    self.get_stemmed_keys()
    self.extract()
    self.output()

Extractor = Extractor()
Extractor.run()
  

      



