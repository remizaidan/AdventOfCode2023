

class CodeBase:

    def __init__(self, name):
        self.name = name
        file_name = f'{name}/input.txt'
        with open(file_name) as f:
            self.lines = [l.rstrip("\n\r") for l in f.readlines()]

    def greet(self):
        print(f'Hello {self.name}!')
