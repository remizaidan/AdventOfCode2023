from common import CodeBase


class Code(CodeBase):

    def __init__(self):
        super().__init__('D7')

    def run(self):
        self.greet()


def test():
    print("No tests for this problem")


if __name__ == '__main__':
    test()
