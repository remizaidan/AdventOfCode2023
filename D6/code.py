from common import CodeBase


class Code(CodeBase):

    def __init__(self):
        super().__init__("D6")

    def run(self):
        self.greet()


def test():
    print("Test")


if __name__ == '__main__':
    test()