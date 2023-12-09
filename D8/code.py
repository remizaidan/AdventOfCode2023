from common import CodeBase


class Code(CodeBase):

    def __init__(self):
        super().__init__('D8')

    def run(self):
        self.greet()
