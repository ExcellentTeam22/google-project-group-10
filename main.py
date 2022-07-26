from typing import List
from AutoCompleteData import AutoCompleteData


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    # here we find the 5 completions
    return [AutoCompleteData('a', 'b', 1, 2)]


if __name__ == "__main__":

    # here we run the file reader (offline)

    print('The system is ready. Enter your text:')
    sentence = ''
    while True:
        new_input = input(sentence)
        sentence += new_input
        if new_input.strip() != '#':
            completions = get_best_k_completions(sentence)
            print('Here are 5 suggestions')
            for i, complete in enumerate (completions, 1):
                print(i, '. ' + complete.completed_sentence, sep='', end='\n')
        else:
            sentence = ''
