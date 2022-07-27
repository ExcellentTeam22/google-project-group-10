from __future__ import annotations
import numpy as np

MAX_PENALTY = 1


class TrieNode:
    def __init__(self, char: str, prev:TrieNode = None):
        self.char = char
        self.children = {}
        self.content = set()
        self.prev = prev
        self.is_common = False


class Trie (object):
    def __init__(self):
        self.root = TrieNode("")
        self.words_counter = 0

    def insert(self, word, path: int, line: int) -> None:
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                self.words_counter += 1
                new_node = TrieNode(node.char + char, self)
                node.children[char] = new_node
                node = new_node
        node.content.add(tuple(np.array([path, line])))
        node.is_common = True

    def dfs_sub_tries(self, node, pre):
        for child in node.children.values():
            for node, word in self.dfs_sub_tries(child, pre + node.char):
                return node, word

    def search(self, searched_word, prefix: bool = False, start_node: TrieNode = None, penalty: int = 0):
        node = self.root if start_node is None else start_node
        ans = set()

        if searched_word == "":
            if len(node.content) != 0 and searched_word == "":
                return {(node.char, tuple(node.content))}
            if prefix:
                for curr_node, curr_word_prefix in self.dfs_sub_tries(node, searched_word[:1]):
                    return {(curr_word_prefix, curr_node.content)}
            return ans
        if searched_word[0] in node.children:
            for res in self.search(searched_word[1:], prefix, node.children[searched_word[0]], penalty):
                return res

        if penalty < MAX_PENALTY:
            for word in self.get_penaltied_words(searched_word, prefix, node, penalty):
                return word

    def get_penaltied_words(self, searched_word: str, prefix: bool, node: TrieNode, penalty: int):
        ans = set()
        for node_key in node.children:
            if searched_word != "" and node != searched_word[0]:
                # switch char
                for word in self.search(searched_word[1:], prefix, node.children[node_key], penalty + 1):
                    yield word
            # add char
            for word in self.search(searched_word, prefix, node.children[node_key], penalty + 1):
                yield word
        # del char
        for word in self.search(searched_word[1:], prefix, node, penalty + 1):
            yield word
