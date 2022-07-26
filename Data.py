import os
import re
from LettersTrie import LettersTrie

DIR_PATH = 'Test'


class Data:
    def __init__(self,):
        self.root = LettersTrie()
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
                    self.root.insert(word, path, i)


if __name__ == "__main__":
    data = Data()
    print("done")
    print(data.root.get("hello"))

