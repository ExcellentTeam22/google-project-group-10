import re


class Grader:
    def __init__(self):
        self.graders = [[CONTAINED_GRADE, contained]]

    def grade(self, searched, line):
        grades_sum = 0
        for i in self.graders:
            grades_sum += i[0] * i[1](searched, line)
        return grades_sum


CONTAINED_GRADE = 1


def contained(searched: str, line: str):
    if re.search(searched, line):
        return 1
    return 0


if __name__ == "__main__":
    grader = Grader()
    print(grader.grade("123", "11"))
