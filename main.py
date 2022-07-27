from functools import reduce
from typing import List

import numpy as np

import IntersectionArrays
from AutoCompleteData import AutoCompleteData
from Data import Data
from LettersTrie import Trie
from IntersectionArrays import IntersectionArray
import linecache as lc


def get_best_k_completions(prefix: str, data: Data) -> List[AutoCompleteData]:
    # here we find the 5 completions
    files_hash = data.files_dic
    letter_trie = data.trie

    sentence_word_list = prefix.split()  # split sentence
    print(sentence_word_list)
    findings_list = [letter_trie.searchExactWord(word) for word in sentence_word_list]
    # findings_list = [letter_trie.searchExactWord(word) for index, word in enumerate(sentence_word_list)
    #                 if index < len(sentence_word_list)-1]  # find each word in the trie
    # findings_list.append(letter_trie.search(sentence_word_list[-1]))
    print(findings_list)
    results = intersect(findings_list)  # intersect between results
    fixed_sentence = ' '.join([res[0] for res in findings_list])  # build the new fixed sentence
    final_results = list(map(find_in_file, (results[0], files_hash, fixed_sentence)))  # creates user result list
    return final_results


def intersect(arrays):
    """
        :param arrays: Arrays of word appearance
        :return: intersection of words arrays that appear in same line and file
        """
    print(arrays)
    nrows, ncols = np.array(arrays[0]).shape
    dtype = {'names': ['f{}'.format(i) for i in range(ncols)],
             'formats': ncols * [arrays[0].dtype]}
    arrays_to_check = (arr.view(dtype) for arr in arrays)
    intersected = reduce(np.intersect1d, arrays_to_check)
    return intersected


def find_in_file(res: list, files_hash: dict, fixed_sent: str):
    line_to_check = lc.getline(files_hash.files_dic[res[0]], res[1])
    if line_to_check.find(fixed_sent):
        return AutoCompleteData(line_to_check, files_hash[res[0]], res[1], 3)
    return


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
                print(i, '. ' + complete.completed_sentence, sep='', end='\n')
        else:
            sentence = ''
