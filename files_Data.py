
class filesData:
    """
    A data of file in list, with search options
    :ivar self.data : list of file data
    :param file_to_read : file to read
    """
    def __init__(self, file_to_read):
        file = open(file_to_read, 'r')
        self.data = file.readline()




