import numpy as np

from common import CodeBase


class Code(CodeBase):

    def __init__(self):
        super().__init__('D6')
        self.times = []
        self.distances = []
        self.time = 0
        self.distance = 0

    def run(self):
        self.greet()

        for line in self.lines:
            self.parse_line(line)

        n = 1
        for t, d in zip(self.times, self.distances):
            n *= self.get_n_ways_to_win(t, d)

        n_mega = self.get_n_ways_to_win(self.time, self.distance)

        print(f'# ways to win = {n}')
        print(f'For the mega race: {n_mega}')

    def parse_line(self, line):
        tokens = line.split(':')
        values = [x.strip() for x in tokens[1].strip().split()]
        key = tokens[0].strip()
        if key == 'Time':
            self.times = [int(x) for x in values]
            self.time = int("".join(values))
        elif key == 'Distance':
            self.distances = [int(x) for x in values]
            self.distance = int("".join(values))

    @staticmethod
    def get_n_ways_to_win(t, d):
        # Find the zeros:
        #  tb * (t - tb) - d = 0
        #  tb^2 - tb * t + d = 0
        #  tb = (t +- sqrt(t^2 - 4d)) / 2
        disc = t * t - 4 * d
        eps = 0.001  # Deal with cases where the solutions are exact integers: we want to win, not equalize...
        t1 = np.ceil((t - np.sqrt(disc)) / 2 + eps)
        t2 = np.floor((t + np.sqrt(disc)) / 2 - eps)
        return int(t2 - t1 + 1)


def test():
    lines = [
        'Time:      7  15   30',
        'Distance:  9  40  200',
    ]

    code = Code()
    for line in lines:
        code.parse_line(line)

    print(code.times)
    print(code.distances)

    n = 1
    for t, d in zip(code.times, code.distances):
        nw = code.get_n_ways_to_win(t, d)
        n *= nw
        print(f'For t={t}, d={d}, # ways to win = {nw}')
    print(f'# ways to win = {n}')

    n_mega = code.get_n_ways_to_win(code.time, code.distance)
    print(f'For the mega race: {n_mega}')


if __name__ == '__main__':
    test()
