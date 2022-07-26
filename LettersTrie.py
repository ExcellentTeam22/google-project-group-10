from __future__ import annotations
import numpy as np


class TrieNode:
    def __init__(self, char: str, prev:TrieNode = None):
        self.char = char
        self.is_end = False
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
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.content.add(tuple(np.array([path, line])))
        node.is_end = True
        if len(node.content) > int(np.sqrt(self.words_counter)):
            node.is_common = True

    def dfs(self, node, pre):
        if node.is_end:
            self.output.append([(pre + node.char), node.content])
        for child in node.children.values():
            self.dfs(child, pre + node.char)

    def search(self, searched_word):
        node = self.root
        for char in searched_word:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        self.output = []
        self.dfs(node, searched_word[:-1])
        return self.output

    def search_exact_word(self, word: str) -> tuple:
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        return word, node.content

    def get_bfs_start(self, word: str) -> TrieNode:
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node

    def bfs(self):
        node = self.get_bfs_start()
        ans = set((node))
