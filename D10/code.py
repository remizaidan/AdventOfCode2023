import numpy as np

from common import CodeBase


class Tile:

    def __init__(self, pos, char):
        self.pos = pos
        self.char = char
        self.neighbors = self.get_neighbors()
        self.rank = -1

    def __repr__(self):
        return self.char

    def __str__(self):
        return f'{self.pos} [{self.char}]'

    def get_neighbors(self):
        y, x = self.pos
        dxy = {
            'J': [(-1, 0), (0, -1)],
            'L': [(0, 1), (-1, 0)],
            'F': [(1, 0), (0, 1)],
            '|': [(0, 0), (-1, 1)],
            '-': [(-1, 1), (0, 0)],
            '7': [(-1, 0), (0, 1)],
            'S': [None, None],
            '.': [None, None],
        }
        if self.char in dxy:
            dx, dy = dxy[self.char]
        else:
            raise ValueError(f'Unknown tile: {self.char}')
        if dx is not None:
            neighbors = [(y + dy[i], x + dx[i]) for i in range(len(dx))]
        else:
            neighbors = [(y + _dy, x + _dx) for _dx in range(-1, 2) for _dy in range(-1, 2) if _dx != 0 or _dy != 0]
        return neighbors


class Code(CodeBase):

    def __init__(self):
        super().__init__('D10')
        self.grid = None
        self.start_pos = None

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        n = self.navigate()
        print(f'Number of steps: {n}')

    def process_line(self, line):
        row = len(self.grid) if self.grid is not None else 0
        line = list(line)
        if 'S' in line:
            if self.start_pos is not None:
                raise ValueError('Multiple start positions')
            self.start_pos = (row, line.index('S'))
        line = [Tile((row, i), c) for i, c in enumerate(line)]
        if self.grid is None:
            self.grid = np.array(line).reshape(1, -1)
        else:
            self.grid = np.vstack((self.grid, line))

    def navigate(self):
        tiles = [self.start_pos]
        self.grid[self.start_pos].rank = 0
        n_steps = 0
        while True:
            new_tiles = []
            for tile in tiles:
                for neighbor in self.grid[tile].neighbors:
                    if neighbor is None:
                        continue
                    if neighbor[0] < 0 or neighbor[0] >= self.grid.shape[0]:
                        continue
                    if neighbor[1] < 0 or neighbor[1] >= self.grid.shape[1]:
                        continue
                    neighbor_tile = self.grid[neighbor]
                    if neighbor_tile.char == '.':
                        continue
                    if neighbor_tile.rank != -1:
                        continue
                    if tile not in neighbor_tile.neighbors:
                        continue
                    self.grid[neighbor].rank = n_steps + 1
                    new_tiles.append(neighbor)
            if len(new_tiles) == 0:
                break
            tiles = new_tiles
            n_steps += 1
        return n_steps


def test():

    lines = [
        '7-F7-',
        '.FJ|7',
        'SJLL7',
        '|F--J',
        'LJ.LJ',
    ]

    code = Code()
    for line in lines:
        code.process_line(line)
    print(code.grid)
    print(f'Start: {code.start_pos}')
    # for row in code.grid:
    #     for tile in row:
    #         print(f'{tile}:')
    #         for neighbor in tile.neighbors:
    #             print(f' -> {neighbor}')
    print()
    n = code.navigate()
    for row in code.grid:
        for tile in row:
            print(f'{tile.rank:3d}', end='')
        print()

    print(f'Number of steps: {n}')



if __name__ == '__main__':
    test()
