from __future__ import annotations


class LettersTrie:
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


if __name__ == "__main__":
    data = LettersTrie()
    data.append("123", "111", "222")
    data.append("123", "5555", "7777")
    print(data.get("123"))
