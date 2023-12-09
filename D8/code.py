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

    def run(self):
        self.greet()

        for line in self.lines:
            self.process_line(line)

        print(f'Number of steps: {self.follow_path()}')

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

    def get_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def follow_path(self):
        start = self.get_node('AAA')
        target = self.get_node('ZZZ')
        node = start
        n_steps = 0
        while node.name != target.name:
            node = node.follow(self.path[n_steps % len(self.path)])
            n_steps += 1
        return n_steps


def test():

    def test_lines(lines):
        code = Code()
        for line in lines:
            code.process_line(line)
        print(f'Path: {code.path}')
        print(f'Nodes:')
        for node in code.nodes.values():
            print(f'  {node}')
        print(f'Number of steps: {code.follow_path()}')

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
    ])

    print("Test 2:")
    test_lines([
        'LLR',
        '',
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ])


if __name__ == '__main__':
    test()
