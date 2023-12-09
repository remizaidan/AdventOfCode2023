import numpy as np

from common import CodeBase


class Sequence:

    def __init__(self, values):
        self.values = np.array(values)
        self.predictors = self.compute_predictors()

    def __repr__(self):
        return f'Sequence({self.values})'

    def show_predictors(self):
        indent = ''
        for p in self.predictors:
            print(indent, end='')
            for v in p:
                print(f'{v:4}', end='')
            print()
            indent += '  '

    def predict_next(self):
        return np.sum([p[-1] for p in self.predictors])

    def predict_prev(self):
        return np.sum([p[0] * ((-1) ** i) for i, p in enumerate(self.predictors)])

    def compute_predictors(self):
        predictors = [self.values]
        prev_predictor = self.values
        while True:
            next_predictor = np.diff(prev_predictor)
            predictors.append(next_predictor)
            prev_predictor = next_predictor
            if np.all(next_predictor == 0):
                break
        return predictors


class Code(CodeBase):

    def __init__(self):
        super().__init__('D9')
        self.sequences = []

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        s = np.sum([s.predict_next() for s in self.sequences])
        print(f'Sum of predictions: {s}')
        s = np.sum([s.predict_prev() for s in self.sequences])
        print(f'Sum of predictions: {s}')

    def process_line(self, line):
        values = [int(v.strip()) for v in line.split()]
        self.sequences.append(Sequence(values))


def test():
    print('Test')
    lines = [
        '0 3 6 9 12 15',
        '1 3 6 10 15 21',
        '10 13 16 21 30 45',
    ]

    code = Code()

    for line in lines:
        code.process_line(line)
    print(code.sequences)
    for s in code.sequences:
        s.show_predictors()
        print(f'Predict next: {s.predict_next()}')
        print(f'Predict prev: {s.predict_prev()}')
        print()

    s = np.sum([s.predict_next() for s in code.sequences])
    print(f'Sum of next predictions: {s}')
    s = np.sum([s.predict_prev() for s in code.sequences])
    print(f'Sum of prev predictions: {s}')


if __name__ == '__main__':
    test()
