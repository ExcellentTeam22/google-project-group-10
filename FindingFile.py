import re


class Finder:
    def __init__(self, data):
        self.data = data

    def find(self, user_input: str):
        words = re.split(r"[^a-zA-Z]*", user_input)
        res = set.intersection(*[self.data.get(word) for word in words])
        return list(res)[0:5]

