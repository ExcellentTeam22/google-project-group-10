from __future__ import annotations


class LettersTrie:
    def __init__(self, prev: LettersTrie = None):
        self.next = {}
        self.prev = prev
        self.content = set()

    def insert(self, new_word: LettersTrie, path: str, line: str) -> None:
        if len(new_word) == 0:
            self.content.add(f"{path}\n{line}")
        else:
            if new_word[0] not in self.next:
                self.next[new_word[0]] = LettersTrie(self)
            self.next[new_word[0]].insert(new_word[1:], path, line)

    def get(self, word: str, pre: bool = False) -> set:
        if word == "":
            if pre:
                return self.get_children_contents()
            return self.content
        elif word[0] not in self.next:
            return None
        else:
            return self.next[word[0]].get(word[1:])

    def get_children_contents(self) -> set:
        ans = set()
        for key in self.next:
           ans = ans.union(self.next[key].get_children_contents())
        ans = ans.union(self.content)
        return ans


if __name__ == "__main__":
    data = LettersTrie()
    data.insert("123", "111", "222")
    data.insert("123", "5555", "7777")
    print(data.get("123", True))
