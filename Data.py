import os
import re
from LettersTrie import Trie

DIR_PATH = 'Test'


class Data:
    """
    class that reads data from files and builds the
    Trie data Struct
    """
    def __init__(self,):
        self.trie = Trie()
        self.files_dic = {}

        self.read_data()

    def read_data(self):
        """
        function that walks over the main directory to read data from files,
        also it save the paths of all files.
        :return: None
        """
        for root, dirs, contents in os.walk(DIR_PATH):
            for file in contents:
                with open(os.path.join(root, file), encoding="utf8") as file_reader:
                    self.read_file(file_reader, os.path.join(root, file))

    def read_file(self, file, path:str):
        """
        function to read the file and split into words
        then insert the word into the trie
        :param file: the file.
        :param path: the path of the file to store in the dicitionay
        :return: None
        """
        for i, line in enumerate(file):
            #for word in re.sub(r"[^a-zA-Z ]", "", line).split():
            for word in re.split(r"[^a-zA-Z]+", line):
                if word != '' and self.word_longer_than_k(2, word):
                    hash_path = hash(path)
                    self.files_dic[hash_path] = path
                    self.trie.insert(word, hash_path, i+1)

    def word_longer_than_k(self, length: int, word:str) -> bool:
        """
        function that checks the words length to decide whether to store it
        in the trie
        :param length: the defined lengthE
        :param word: word to check its length
        :return: true if word is longer than the passed length
        """
        return len(word) > length

