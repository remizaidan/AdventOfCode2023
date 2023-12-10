from common import CodeBase


class Code(CodeBase):

    def __init__(self):
        super().__init__('D@DAY@')

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

    def process_line(self, line):
        print(f'Processing line: {line}')


def test():
    print("Testing...")


if __name__ == '__main__':
    test()
