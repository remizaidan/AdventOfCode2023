import regex as re

from common import CodeBase


class Code(CodeBase):
    def __init__(self):
        super().__init__("D1")
        self.digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        self.digits_regex = re.compile(r"\d")
        self.words_regex = re.compile(r"\d|zero|one|two|three|four|five|six|seven|eight|nine")

    def run(self):
        self.greet()

        s_1 = 0
        s_2 = 0
        for line in self.lines:
            s_1 += self.add_first_and_last_digits(line, allowWords=False)
            s_2 += self.add_first_and_last_digits(line, allowWords=True)

        print("The sums are: ", s_1, " - ", s_2)

    def add_first_and_last_digits(self, line, allowWords=False):
        r = self.match_digits(line, allowWords=allowWords)
        if allowWords:
            r = [self.as_digit(d) for d in r]
        if len(r) < 1:
            return 0
        return int(r[0] + r[-1])

    def match_digits(self, line, allowWords=False):
        if allowWords:
            return self.words_regex.findall(line, overlapped=True)
        return self.digits_regex.findall(line)

    def as_digit(self, s):
        try:
            return str(int(s))
        except ValueError:
            return str(self.digits.index(s))


def test():

    code = Code()

    patterns = [
        "1", "one", "one two", "eighttwo", "eightwo", "abc1edf2gh3ij", "1234onetwo"
    ]

    for pattern in patterns:
        print(f"Pattern: {pattern}")
        print(f" - {code.match_digits(pattern)}")
        print(f" - {code.match_digits(pattern, True)}")
        print(f" - {code.add_first_and_last_digits(pattern)}")
        print(f" - {code.add_first_and_last_digits(pattern, True)}")
        print()


if __name__ == '__main__':
    test()

