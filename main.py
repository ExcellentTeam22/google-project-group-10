from functools import reduce
from typing import List

import numpy as np

from AutoCompleteData import AutoCompleteData
from Data import Data
from LettersTrie import Trie
import linecache as lc


def get_best_k_completions(prefix: str, data: Data) -> List[AutoCompleteData]:
    # here we find the 5 completions
    files_hash = data.files_dic
    letter_trie = data.trie
    sentence_word_list = prefix.split()  # split sentence
    findings_list = [letter_trie.search(word) for word in sentence_word_list]
    results = []
    words = [next(gen) for gen in findings_list]
    founds = [list(lst[1]) for lst in words]
    results.extend(intersect([item for item in founds]))  # intersect between results
    fixed_sentence = ' '.join([res[0] for res in words])  # build the new fixed sentence
    final_results = list(find_in_file(results, files_hash, fixed_sentence))  # creates user result list
    return final_results


def intersect(arrays):
    """
        :param arrays: Arrays of word appearance
        :return: intersection of words arrays that appear in same line and file
        """
    array_to_check = np.array(list(arrays[0]))
    nrows, ncols = array_to_check.shape
    dtype = {'names': ['f{}'.format(i) for i in range(ncols)],
             'formats': ncols * [array_to_check.dtype]}
    arrays_to_check = (np.array(list(arr)).view(dtype) for arr in arrays)
    intersected = reduce(np.intersect1d, arrays_to_check)
    return intersected


def find_in_file(res: list, files_hash, fixed_sent: str):
    lst = []

    for item in res:
        no_row = item[1]
        line_to_check = lc.getline(files_hash[item[0]], no_row)
        if line_to_check.find(fixed_sent):
            lst.append(AutoCompleteData(line_to_check, files_hash[item[0]], no_row, 3))
    return lst


if __name__ == "__main__":
    data = Data()
    # here we run the file reader (offline)

    print('The system is ready. Enter your text:')
    sentence = ''
    while True:
        new_input = input(sentence)
        sentence += new_input
        if new_input.strip() != '#':
            completions = get_best_k_completions(sentence, data)
            print('Here are 5 suggestions')
            for i, complete in enumerate(completions, 1):
                print(i, '. ' + complete.completed_sentence,complete.source_text,complete.offset, sep='', end='\n')
                if i > 4:
                    break
        else:
            sentence = ''
