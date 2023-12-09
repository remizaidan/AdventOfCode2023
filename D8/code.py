import numpy as np

from common import CodeBase


class Node:

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

    def follow(self, direction):
        if direction == 'L':
            return self.left
        elif direction == 'R':
            return self.right
        else:
            raise ValueError(f'Unknown direction: {direction}')

    def __str__(self):
        return f'{self.name} = ({self.left.name}, {self.right.name})'


class Code(CodeBase):

    def __init__(self):
        super().__init__('D8')
        self.path = ''
        self.nodes = {}
        self.seeds = []

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        print(f'Number of steps: {self.get_n_steps([self.get_node("AAA")], lambda n: n.name == "ZZZ")}')
        print(f'Number (simultaneous) steps: {self.get_n_steps(self.seeds, lambda n: n.name.endswith("Z"))}')

    def process_line(self, line):
        if line.strip() == '':
            return
        if '=' in line:
            self.process_node(line)
        else:
            self.process_path(line)

    def process_path(self, line):
        self.path = line.strip()

    def process_node(self, line):
        tokens = line.split("=")
        node_name = tokens[0].strip()
        lr = tokens[1].strip().strip('()').split(",")
        left = lr[0].strip()
        right = lr[1].strip()
        node = self.get_node(node_name)
        node.left = self.get_node(left)
        node.right = self.get_node(right)
        if node_name.endswith('A'):
            self.seeds.append(node)

    def get_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def follow_path(self, node, stop_condition):
        n_steps = 0
        while not stop_condition(node):
            node = node.follow(self.path[n_steps % len(self.path)])
            n_steps += 1
        return n_steps

    def get_n_steps(self, seeds, stop_condition):
        n_steps = [
            self.follow_path(seed, stop_condition)
            for seed in seeds
        ]
        return np.lcm.reduce(n_steps) if len(n_steps) > 1 else n_steps[0]


def test():

    def test_lines(lines, test_ZZZ=True, test_XYZ=True):
        code = Code()
        for line in lines:
            code.process_line(line)
        print(f'Path: {code.path}')
        print(f'Nodes:')
        for node in code.nodes.values():
            print(f'  {node}')

        if test_ZZZ:
            print(f'Number of steps: {code.get_n_steps([code.get_node("AAA")], lambda n: n.name == "ZZZ")}')
        if test_XYZ:
            print(f'Number (simultaneous) steps: {code.get_n_steps(code.seeds, lambda n: n.name.endswith("Z"))}')

    print("Test 1:")
    test_lines([
        'RL',
        '',
        'AAA = (BBB, CCC)',
        'BBB = (DDD, EEE)',
        'CCC = (ZZZ, GGG)',
        'DDD = (DDD, DDD)',
        'EEE = (EEE, EEE)',
        'GGG = (GGG, GGG)',
        'ZZZ = (ZZZ, ZZZ)',
    ], test_ZZZ=True, test_XYZ=False)

    print("Test 2:")
    test_lines([
        'LLR',
        '',
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ], test_ZZZ=True, test_XYZ=False)

    print("Test 3:")
    test_lines([
        'LR',
        '',
        '11A = (11B, XXX)',
        '11B = (XXX, 11Z)',
        '11Z = (11B, XXX)',
        '22A = (22B, XXX)',
        '22B = (22C, 22C)',
        '22C = (22Z, 22Z)',
        '22Z = (22B, 22B)',
        'XXX = (XXX, XXX)',
    ], test_ZZZ=False, test_XYZ=True)


if __name__ == '__main__':
    test()
