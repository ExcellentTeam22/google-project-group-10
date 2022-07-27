import os
import re
from LettersTrie import Trie

DIR_PATH = 'Test'


class Data:
    def __init__(self,):
        self.trie = Trie()
        self.files_dic = {}

        self.read_data()

    def read_data(self):
        for root, dirs, contents in os.walk(DIR_PATH):
            for file in contents:
                with open(os.path.join(root, file), encoding="utf8") as file_reader:
                    self.read_file(file_reader, os.path.join(root, file))

    def read_file(self, file, path:str):
        for i, line in enumerate(file):
            for word in re.split(r"[^a-zA-Z]+", line):
                if word != '':
                    hash_path = hash(path)
                    self.files_dic[hash_path] = path
                    self.trie.insert(word, hash_path, i)


#def get_hashed(lst):


if __name__ == "__main__":
    data = Data()
    print("done")
    tr = data.trie
    #print (tr.search ("here"))
    for res in tr.search("here"):
        print(res)
    #print(tr.search("hello"))

