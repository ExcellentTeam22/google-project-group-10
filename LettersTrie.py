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

    def dfs_sub_trie(self, node, pre):
        #if len(node.content) != 0:
        #    yield node, pre + node.char
        for child in node.children.values():
            for node, word in self.dfs_sub_trie(child, pre + node.char):
                yield node, word
        return

    def search(self, searched_word, prefix: bool = False, start_node: TrieNode = None, penalty: int = 0):
        node = self.root if start_node is None else start_node
        ans = []
        if searched_word == "":
            if len(node.content) != 0 and searched_word == "":
                ans += [[node.char, node.content]]
            if prefix:
                for curr_node, curr_word_prefix in self.dfs_sub_trie(node, searched_word[:1]):
                    print(curr_word_prefix)
                    ans.append([curr_word_prefix, curr_node.content])
            return ans
        elif penalty < MAX_PENALTY:
            for node_key in node.children:
                #add char
                ans += self.search(searched_word, prefix, node.children[node_key], penalty + 1)
                if searched_word != "" and node != searched_word[0]:
                    #switch char
                    ans += self.search(searched_word[1:], prefix, node.children[node_key], penalty + 1)
            #del char
            ans += self.search(searched_word[1:], prefix, node, penalty + 1)
        if searched_word[0] in node.children:
            ans += self.search(searched_word[1:], prefix, node.children[searched_word[0]], penalty)
        return ans
