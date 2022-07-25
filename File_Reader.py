import os
import re


path = 'Archive'


class File_Reader():
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.file_content = {}
        self.wordList = {}


    def read_files(self):
        filelist = []
        for root, dirs, files in os.walk(self.folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                filelist.append(file_path)
                self.file_content[file] = self.filesData(file_path)

    def get_file_content(self):
        return self.file_content

    def filesData(self, file_to_read):
        file = open(file_to_read,encoding="utf8")
        file_data = file.readlines()
        file.close()
        return file_data

    def createWordList(self):
        for file in self.file_content:
            for line, line_index in enumerate(file):
                self.wordList = {word: set(file.key, line_index) for word in re.split(r"[^A-Za-z]*", line)}

    def getWordList(self):
        return self.wordList


files = File_Reader('Archive')
files.read_files()
files.createWordList()
for index in range(1, 3):
    print(files.getWordList())



