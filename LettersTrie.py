from __future__ import annotations
import numpy as np

MAX_PENALTY = 1


class TrieNode:
    """
    The class in a Trie's Node.
    """
    def __init__(self, word: str, prev: TrieNode = None):
        self.word = word
        self.children = {}
        self.content = set()
        self.prev = prev
        self.is_common = False


class Trie (object):
    """
    The class is a prefix tree.
    The tree is able to produce words generator that receives a wonted word, and returns each iteration the closest
    word to the received one.
    """
    def __init__(self):
        self.root = TrieNode("")
        self.words_counter = 0

    def insert(self, word, path: int, line: int) -> None:
        """
        The method add the received word into the database so the trie and in the word's node (which created if
        needed), and add it to the nodes content the received file path and line.
        :param word: The word's node needed to insert to.
        :param path: The file's path.
        :param line: The line which the words appears at.
        :return: None
        """
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                self.words_counter += 1
                new_node = TrieNode(node.word + char, self)
                node.children[char] = new_node
                node = new_node
        node.content.add(tuple(np.array([path, line])))
        node.is_common = True

    def dfs_sub_tries(self, node):
        """
        The method is a generator which returns all the received node's sub-trie nodes one by one.
        :param node: The sub trie's root.
        :param pre:
        :return:
        """
        for child in node.children.values():
            for node in self.dfs_sub_tries(child):
                yield node

    def search(self, searched_word, prefix: bool = False, start_node: TrieNode = None, penalty: int = 0):
        """
        The method is a generator which returns each iteration the word in the tree ordered by their lowest penalty
        one by one.
        :param searched_word: The searched word.
        :param prefix: If the searched word could be a words prefix or not.
        :param start_node: The node where the search starts at.
        :param penalty: The penalty of searched word so far.
        :return: Each iteration returns the best word found so its penalty is the lowest.
        """
        node = self.root if start_node is None else start_node

        if searched_word == "":
            if len(node.content) != 0 and searched_word == "":
                yield {(node.word, tuple(node.content))}
            if prefix:
                for curr_node, curr_word_prefix in self.dfs_sub_tries(node, searched_word[:1]):
                    yield {(curr_word_prefix, curr_node.content)}
            return
        if searched_word[0] in node.children:
            for res in self.search(searched_word[1:], prefix, node.children[searched_word[0]], penalty):
                yield res

        if penalty < MAX_PENALTY:
            for word in self.get_penaltied_words(searched_word, prefix, node, penalty):
                yield word

    def get_penaltied_words(self, searched_word: str, prefix: bool, node: TrieNode, penalty: int):
        """
        The method is a generator which returns the best words so the next added character makes a penalty,
        :param searched_word: The searched word.
        :param prefix: If the searched word could be a prefix of other word.
        :param node: The node where the search starts at.
        :param penalty: The calculated word's penalty so far.
        :return: Each iteration returns the best word with the lowest penalty so far (The returned word has a penalty
                 due the search starts at creating a penalty).
        """
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
