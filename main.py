from functools import reduce
from typing import List

import numpy as np

from AutoCompleteData import AutoCompleteData
from Data import Data
import linecache as lc
import re

def get_best_k_completions(prefix: str, data: Data) -> List[AutoCompleteData]:
    """ Get the best completions of a sentence that the user entered.
    :param prefix: User sentence
    :param data: The data structure of sources
    :return: List of AutoComplete object that represent the completions
    """
    # here we find the 5 completions
    files_hash = data.files_dic
    letter_trie = data.trie
    sentence_word_list = prefix.split()  # split sentence
    findings_list = [letter_trie.search(word) for word in sentence_word_list]
    results = []

    words = [next(gen) for gen in findings_list]

    for i, gen in enumerate(findings_list):
        if i > 0:
            words[-1 - i] = next(letter_trie.search(sentence_word_list[-1 - i]))
        for generated_word in gen:
            words[i] = generated_word
            founds = [list(lst[1]) for lst in words]
            results.extend(intersect([item for item in founds]))  # intersect between results
            if len (results) > 5:
                break
    fixed_sentence = ' '.join([res[0] for res in words])  # build the new fixed sentence
    final_results = list(find_in_file(results, files_hash, fixed_sentence))  # creates user result list
    return final_results


def intersect(arrays):
    """ Intersect arrays of the results
    :param arrays: Arrays of word appearance
    :return: intersection of words arrays that appear in same line and file
    """
    array_to_check = np.array(list(arrays[0]))
    n_rows, n_cols = array_to_check.shape
    d_type = {'names': ['f{}'.format(i) for i in range(n_cols)],
             'formats': n_cols * [array_to_check.dtype]}
    arrays_to_check = (np.array(list(arr)).view(d_type) for arr in arrays)
    intersected = reduce(np.intersect1d, arrays_to_check)
    return intersected


def find_in_file(res: list, files_hash, fixed_sent: str):
    """
    Find user fixed sentence with the results.
    :param res: List of result for user sentence
    :param files_hash: Dictionary of all the files
    :param fixed_sent: user fixed sentence
    :return:
    """
    list_of_results = []


    for item in res:
        no_row = item[1]
        line_to_check = lc.getline(files_hash[item[0]], no_row)
        if line_to_check.find(fixed_sent):
            list_of_results.append(AutoCompleteData(line_to_check, files_hash[item[0]], no_row, 0))
    return list_of_results


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
            for index, complete in enumerate(completions, 1):
                print(index, '. ' + complete.completed_sentence, sep='', end='\n')
                if index > 4:

                    break
        else:
            sentence = ''
