import os

from files_Data import filesData
path = 'Archive'


class File_Reader ():
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.file_content = {}

    def read_files(self, folder_name):
        filelist = []
        for root, dirs, files in os.walk (path):
            for file in files:
                filelist.append (os.path.join (root, file))
                self.file_content[os.path.join (root, file)] = filesData(os.path.join (root, file))

    def get_file_content(self):
        return self.file_content
