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
    findings_list = [letter_trie.searchExactWord(word) for word in sentence_word_list]
    # findings_list = [letter_trie.searchExactWord(word) for index, word in enumerate(sentence_word_list)
    #                 if index < len(sentence_word_list)-1]  # find each word in the trie
    # findings_list.append(letter_trie.search(sentence_word_list[-1]))
    results = intersect([lst[1] for lst in findings_list if lst[1]])  # intersect between results
    fixed_sentence = ' '.join([res[0] for res in findings_list])  # build the new fixed sentence
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
        i = item[1]
        line_to_check = lc.getline(files_hash[item[0]], i)
        if line_to_check.find(fixed_sent):
            lst.append(AutoCompleteData(line_to_check, files_hash[item[0]], item[1], 3))
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
        else:
            sentence = ''
