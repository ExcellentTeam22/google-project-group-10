from __future__ import annotations
import numpy as np

"""class LettersTrie:
    def __init__(self, prev: LettersTrie = None):
        self.next = {}
        self.prev = prev
        self.content = set()

    def append(self, new_word: LettersTrie, path: str, line: str) -> None:
        if len(new_word) == 0:
            self.content.add(f"{path} \n {line}")
        else:
            if new_word[0] not in self.next:
                self.next[new_word[0]] = LettersTrie(self)
            self.next[new_word[0]].append(new_word[1:], path, line)

    def get(self, word: str, distance: int = 0) -> list:
        if word == "":
            return self.content
        if word[0] not in self.next:
            return None
        else:
            return self.next[word[0]].get(word[1:])
"""
"""
if __name__ == "__main__":
    data = LettersTrie()
    data.append("123", "111", "222")
    data.append("123", "5555", "7777")
    print(data.get("12"))"""


class TrieNode:

    def __init__(self, char):
        self.char = char

        self.is_end = False

        self.children = {}
        self.content = set()


class Trie(object):

    def __init__(self):

        self.root = TrieNode("")

    def insert(self, word, path: int, line: int) -> None:

        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.content.add(tuple(np.array([path, line], dtype='int64')))
        node.is_end = True

    def dfs(self, node, pre):

        if node.is_end:
            self.output.append([(pre + node.char), node.content])

        for child in node.children.values():
            self.dfs(child, pre + node.char)

    def search(self, x):

        node = self.root

        for char in x:
            if char in node.children:
                node = node.children[char]
            else:

                return []

        self.output = []
        self.dfs(node, x[:-1])

        return self.output

    def searchExactWord(self, x):

        node = self.root

        for char in x:
            if char in node.children:
                node = node.children[char]
            else:

                return []

        return (x, node.content)
